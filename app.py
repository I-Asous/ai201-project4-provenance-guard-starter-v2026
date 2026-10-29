#!/usr/bin/env python3
"""
Provenance Guard — the web service.

    python app.py

Then, in another terminal:

    curl -X POST http://127.0.0.1:5000/ping \
      -H "Content-Type: application/json" \
      -d '{"message": "hello"}'

That's the example route. It works right now, before you've written anything.
**Leave it alone** — it's your control. When something breaks later, check that
`/ping` still answers: if it does, the problem is in your handler; if it
doesn't, it's the service itself.

Routes:

    POST /ping        the worked example. Already works. Don't edit it
    POST /submit      check a piece of writing, log the decision
    POST /appeal      contest a decision; moves it to under_review
    GET  /log         the audit log. Already works
    GET  /health      is the service up, and is the model loaded
"""

import uuid

from flask import Flask, jsonify, request

import audit
import config
import detector
import scoring
import stylometry

app = Flask(__name__)


# ── Rate limiting — UNIT 8 ────────────────────────────────────────────────────
# Off until you turn it on. In unit 8, Milestone 1:
#
#   1. Set RATE_LIMITING_ENABLED = True in config.py (or AI201_RATE_LIMITS=1)
#   2. Choose your numbers there
#   3. Uncomment the @limiter.limit(...) line on /submit below
#
# The order doesn't matter. While limiting is off, that decorator is a no-op
# that quietly does nothing, so uncommenting it early costs you nothing — but
# it also means no 429 until you've done step 1.
#
# The storage backend is preconfigured, which stops Flask-Limiter printing a
# warning on every start. In-memory is right for one laptop and wrong for
# anything real — a restart forgets every count.

class _LimiterOff:
    """
    Stands in for the real limiter while rate limiting is off.

    It makes @limiter.limit(...) a decorator that returns the route
    untouched, so uncommenting the line before you flip the setting is
    harmless instead of a crash on startup.
    """

    def limit(self, *args, **kwargs):
        return lambda view: view


limiter = _LimiterOff()
if config.RATE_LIMITING_ENABLED:
    from flask_limiter import Limiter
    from flask_limiter.util import get_remote_address

    def rate_limit_key():
        """
        Who a request counts against.

        Falling back to the caller's address is the easy version. Unit 8's
        stretch asks about per-creator limits instead — and the difference
        matters: one script can look like a thousand callers, and one household
        can look like one.
        """
        payload = request.get_json(silent=True)
        # A body that parses as JSON but isn't an object — a bare list or
        # string — has no .get. Without this guard the key function raises
        # BEFORE the route runs, and a malformed request becomes a 500 that
        # looks like your handler crashed when your handler never ran.
        if not isinstance(payload, dict):
            return get_remote_address()
        creator = payload.get("creator_id")
        return creator if isinstance(creator, str) and creator.strip() else get_remote_address()

    limiter = Limiter(
        key_func=rate_limit_key,
        app=app,
        storage_uri=config.RATE_LIMIT_STORAGE,
        default_limits=[],
    )

    @app.errorhandler(429)
    def rate_limited(exc):
        """
        A rejected request still leaves a trace.

        ⚠️ An attack that shows up only as an absence is one you'll never find.
        """
        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            payload = {}
        audit.log_rejection(
            creator_id=payload.get("creator_id", "unknown"),
            reason="rate_limited",
            limit=str(exc.description),
        )
        return jsonify({
            "error": "rate_limited",
            "message": "Too many submissions. Try again shortly.",
            "limit": str(exc.description),
        }), 429


# ── The worked example. Already works. Don't edit. ────────────────────────────

@app.post("/ping")
def ping():
    """
    Everything a route needs, in six lines.

    JSON arrives as a dict. You pull things out of it. You return a dict and
    the framework turns it into a response. That's the whole idea.
    """
    payload = request.get_json(silent=True) or {}
    return jsonify({
        "ok": True,
        "you_sent": payload.get("message"),
        "service": "provenance-guard",
    })


@app.get("/health")
def health():
    """Is the service up, and has the model been downloaded yet?"""
    import detector

    loaded = detector._model is not None
    return jsonify({
        "ok": True,
        "detector_model": config.DETECTOR_MODEL,
        "detector_loaded": loaded,
        "rate_limiting": config.RATE_LIMITING_ENABLED,
        "log_entries": len(audit.read_entries()),
    })


# ── YOU BUILD THIS ────────────────────────────────────────────────────────────

@app.post("/submit")
# @limiter.limit(f"{config.RATE_LIMIT_PER_MINUTE}/minute;{config.RATE_LIMIT_PER_DAY}/day")
def submit():
    """
    Take a piece of text, decide about it, log the decision, answer.

    Expects JSON:
        {"text": "...", "creator_id": "..."}

    Returns JSON (DESIGN.md §4 is the full contract):
        {"content_id", "creator_id", "guess", "confidence", "label",
         "model_score", "style_score", "combined_score", "status"}

    Bad input never reaches the model. It gets a 4xx with
    {"error": <code>, "message": <sentence>} and a `rejected` log entry:
    400 invalid_json / missing_text / missing_creator_id / text_too_short,
    413 text_too_long, 503 detector_unavailable.
    """
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return _reject("unknown", 400, "invalid_json",
                       "Send a JSON object like {\"text\": \"...\", \"creator_id\": \"...\"}.")

    creator_id = payload.get("creator_id")
    creator_for_log = creator_id if isinstance(creator_id, str) and creator_id.strip() else "unknown"
    text = payload.get("text")

    # Size first, before anything that costs time — and before the model.
    if isinstance(text, str) and len(text) > MAX_TEXT_CHARS:
        return _reject(creator_for_log, 413, "text_too_long",
                       f"That's {len(text):,} characters. The limit is {MAX_TEXT_CHARS:,}.",
                       text_length=len(text))
    if not isinstance(text, str) or not text.strip():
        return _reject(creator_for_log, 400, "missing_text",
                       "Include the writing to check, as a non-empty string in \"text\".")
    if creator_for_log == "unknown":
        return _reject(creator_for_log, 400, "missing_creator_id",
                       "Include who wrote this, as a non-empty string in \"creator_id\".")
    n_words = len(stylometry.words(text))
    if n_words < MIN_TEXT_WORDS:
        return _reject(creator_for_log, 400, "text_too_short",
                       f"That's {n_words} words. We need at least {MIN_TEXT_WORDS} to say anything useful.",
                       text_length=len(text))

    try:
        model_score = detector.model_signal(text)
    except (detector.DetectorUnavailable, ValueError) as exc:
        return _reject(creator_id, 503, "detector_unavailable",
                       "The checker isn't available right now. Please try again shortly.",
                       detail=str(exc)[:200])
    style_score = stylometry.style_signal(text)
    combined = scoring.combine_signals(model_score, style_score)
    guess, label = scoring.score_to_label(combined)

    content_id = str(uuid.uuid4())
    audit.log_decision(
        content_id=content_id,
        creator_id=creator_id,
        guess=guess,
        model_score=model_score,
        style_score=style_score,
        combined_score=combined,
        label=label,
        status="decided",
    )
    return jsonify({
        "content_id": content_id,
        "creator_id": creator_id,
        "guess": guess,
        "confidence": scoring.confidence(combined),
        "label": label,
        "model_score": model_score,
        "style_score": style_score,
        "combined_score": combined,
        "status": "decided",
    })


# The bounds from DESIGN.md §4. Twenty words is about where both signals stop
# being noise; twenty thousand characters is well past what the model reads
# (400 tokens) and keeps an enormous body from tying up the service.
MIN_TEXT_WORDS = 20
MAX_TEXT_CHARS = 20_000


def _reject(creator_id, status_code, error, message, **extra):
    """Refuse a request, and leave a trace of it in the log."""
    audit.log_rejection(creator_id=creator_id, reason=error, http_status=status_code, **extra)
    return jsonify({"error": error, "message": message}), status_code


@app.post("/appeal")
def appeal():
    """
    A writer says you got it wrong.

    Expects JSON:
        {"content_id": "...", "reasoning": "..."}

    Checks the content_id has a decision in the log (404 if not), appends an
    `under_review` appeal entry beside it — the original stays untouched —
    and confirms to the writer. No automatic re-scoring; a person reviews it.

    This is the smallest endpoint in the project and the one that matters most
    to the person on the other end.
    """
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify({"error": "invalid_json",
                        "message": "Send a JSON object like {\"content_id\": \"...\", \"reasoning\": \"...\"}."}), 400

    content_id = payload.get("content_id")
    reasoning = payload.get("reasoning")
    if not isinstance(content_id, str) or not content_id.strip():
        return jsonify({"error": "missing_content_id",
                        "message": "Include the content_id you got back when you submitted."}), 400
    if not isinstance(reasoning, str) or not reasoning.strip():
        return jsonify({"error": "missing_reasoning",
                        "message": "Tell us briefly why you think the result is wrong."}), 400

    content_id = content_id.strip()
    decisions = [e for e in audit.entries_for(content_id) if e.get("status") == "decided"]
    if not decisions:
        return jsonify({"error": "unknown_content_id",
                        "message": f"We couldn't find a submission with id {content_id}. "
                                   "Check it matches the one you were given."}), 404

    # The creator comes from the original decision, not the request, so nobody
    # can file an appeal under someone else's name.
    original = decisions[0]
    audit.log_appeal(content_id=content_id, creator_id=original["creator_id"], reasoning=reasoning)
    return jsonify({
        "content_id": content_id,
        "status": "under_review",
        "message": "Thanks. Your appeal is recorded and a person will review this "
                   "decision. The original result is on hold until then.",
        "original_label": original.get("label"),
    })


# ── Already works ─────────────────────────────────────────────────────────────

@app.get("/log")
def get_log():
    """
    The audit log, most recent last.

        curl "http://127.0.0.1:5000/log?limit=10"

    You need this in unit 8 to paste entries into your README, and you need it
    now to see whether your logging is actually working.
    """
    limit = request.args.get("limit", type=int)
    entries = audit.read_entries(limit=limit)
    return jsonify({"count": len(entries), "entries": entries})


def main():
    print(f"Provenance Guard on http://{config.HOST}:{config.PORT}")
    print(f"  detector model:  {config.DETECTOR_MODEL}")
    print(f"  rate limiting:   {'ON' if config.RATE_LIMITING_ENABLED else 'off (unit 8)'}")
    print(f"  audit log:       {config.AUDIT_LOG}")
    print()
    print("Check it's alive:")
    print(f'  curl -X POST http://{config.HOST}:{config.PORT}/ping \\')
    print('    -H "Content-Type: application/json" \\')
    print("    -d '{\"message\": \"hello\"}'")
    print()
    # debug=True hands out an interactive debugger, so it's local-only — see config.py
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)


if __name__ == "__main__":
    main()
