#!/usr/bin/env python3
"""
Run your five criteria three times each.  <- UNIT 8, MILESTONE 3

    python app.py                              # in one terminal
    python run_eval.py --label before          # in another
    python run_eval.py --label after

The attack set tests what staff thought to test. This tests what *you* thought
to test, and the two rarely overlap much. Both count.

Fill in `scenarios.py` first — that's where you say what each criterion needs
run against it. A criterion about false positives needs your own writing. One
about label coverage needs inputs across the score range.

!! Three trials, and **your first signal runs a model, so identical input can
score differently twice.** That's exactly why repeats matter here.

This does the sending and the recording. It does not decide whether a trial
passed — that depends on the criterion you wrote, so the Verdict column comes
back blank.

Extended for this project's criteria 4 and 5, which sending text alone can't
check:

    "appeals"     submit each text, appeal the content_id that came back, and
                  read /log to see what the appeal left there. Then appeal ids
                  that were never issued. (`appeal_trial`)
    "check_log"   after each request, record the newest /log entry, so a
                  refusal can be matched to the `rejected` line it wrote.
    "ping_after"  after each trial, POST /ping to show the service is still up.

Every request also records how long it took (`elapsed_s`), and a /submit
response keeps `combined_score`, `error` and `message`, not just the guess.
"""

import argparse
import datetime as dt
import json
import sys
import time
import uuid
from pathlib import Path

import config

# Windows consoles often run a codepage that can't print every character in
# this file's help text. Without this, `--help` ends in a UnicodeEncodeError
# traceback instead of the help — which is a miserable first thing to hit.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(errors="replace")
    except (AttributeError, ValueError):  # not a normal text stream
        pass


DEFAULT_URL = f"http://{config.HOST}:{config.PORT}"

# What a /submit response is reduced to in the report, in this order. A field
# the response didn't carry is left out rather than shown as null.
SUBMIT_FIELDS = ("content_id", "guess", "confidence", "model_score", "style_score",
                 "combined_score", "label", "error", "message")


def bodies_for(scenario):
    """
    The request bodies one scenario sends.

    A "texts" scenario gets a creator_id made up for it. A "bodies" scenario is
    sent exactly as written, which is how a bad-input criterion says things a
    string can't — no `text` field, a null, something enormous.
    """
    if scenario.get("bodies"):
        return list(scenario["bodies"])
    return [
        {"text": text, "creator_id": f"eval_{scenario['name'][:12]}_{i}"}
        for i, text in enumerate(scenario["texts"], 1)
    ]


def describe(body):
    """A short, readable note of what was sent — for the report."""
    if (isinstance(body, dict) and set(body) == {"text", "creator_id"}
            and isinstance(body.get("text"), str)):
        text = body["text"]
        if not text:
            return "(empty text)"
        if len(text) > 70:
            return f"{text[:70]}… ({len(text):,} characters)"
        return text
    return json.dumps(body)[:120]


def send(http, method, url, body=None, timeout=90.0):
    """
    One request. Returns (record, payload) and never raises.

    A response that isn't JSON comes back as status null with a
    JSONDecodeError. That's almost always Flask's HTML error page, which means
    the route crashed: look for a traceback in the terminal running app.py.
    """
    started = time.perf_counter()
    try:
        response = http.request(method, url, json=body, timeout=timeout)
        payload = response.json() if response.content else {}
    except Exception as exc:  # noqa: BLE001
        return {"status": None, "error": f"{type(exc).__name__}: {exc}"}, {}
    if not isinstance(payload, dict):
        payload = {"body": payload}
    return {"status": response.status_code,
            "elapsed_s": round(time.perf_counter() - started, 3)}, payload


def read_log(http, args):
    """The whole audit log, oldest first."""
    _, payload = send(http, "GET", f"{args.url}/log", timeout=args.timeout)
    return payload.get("entries", [])


def submit_one(http, args, body, check_log=False):
    """Send one body to /submit and keep what came back."""
    record, payload = send(http, "POST", f"{args.url}/submit", body, args.timeout)
    record.update({k: payload[k] for k in SUBMIT_FIELDS if payload.get(k) is not None})
    record["sent"] = describe(body)

    if check_log and record["status"] is not None:
        entries = read_log(http, args)
        newest = entries[-1] if entries else None
        record["log_entry"] = newest
        # A refusal should have written a `rejected` line naming the same
        # reason and status the caller was given.
        record["log_matches"] = bool(
            newest
            and newest.get("status") == "rejected"
            and newest.get("reason") == record.get("error")
            and newest.get("http_status") == record["status"]
        )
    return record


def ping_record(http, args):
    """Is the service still answering after everything the trial threw at it?"""
    record, payload = send(http, "POST", f"{args.url}/ping",
                           {"message": "still there?"}, args.timeout)
    record["ok"] = payload.get("ok")
    record["sent"] = "POST /ping, after the trial"
    return record


def made_up_ids(real_ids, trial):
    """
    Three content_ids that were never issued, of the kinds a writer could
    really send: a one-character typo of a real id, a well-formed id nobody was
    given, and a plain guess.
    """
    ids = []
    if real_ids:
        real = real_ids[0]
        ids.append(real[:-1] + ("0" if real[-1] != "0" else "1"))
    ids.append(str(uuid.uuid4()))
    ids.append(f"my-essay-{trial}")
    return ids


def appeal_trial(http, args, scenario, trial):
    """
    Criterion 4. For each text: submit it, appeal the content_id that came
    back, then read /log and check what the appeal left there. Then appeal
    content_ids that were never issued, which should be refused and leave no
    appeal entry.
    """
    spec = scenario["appeals"]
    reasoning = spec["reasoning"]
    results, real_ids = [], []

    for i, text in enumerate(spec["texts"], 1):
        creator = f"eval_appeal_{i}"
        sub, sub_payload = send(http, "POST", f"{args.url}/submit",
                                {"text": text, "creator_id": creator}, args.timeout)
        content_id = sub_payload.get("content_id")
        record = {"sent": f"submit as {creator}, then appeal its content_id",
                  "submit_status": sub["status"],
                  "submit_guess": sub_payload.get("guess"),
                  "content_id": content_id}
        if not content_id:
            record["error"] = f"submit gave no content_id: {sub_payload or sub}"
            results.append(record)
            continue
        real_ids.append(content_id)

        def decisions(entries):
            return [e for e in entries
                    if e.get("content_id") == content_id and e.get("status") == "decided"]

        decision_before = decisions(read_log(http, args))
        ap, ap_payload = send(http, "POST", f"{args.url}/appeal",
                              {"content_id": content_id, "reasoning": reasoning},
                              args.timeout)
        after = read_log(http, args)
        appeals = [e for e in after
                   if e.get("content_id") == content_id and e.get("event") == "appeal"]
        one = appeals[0] if len(appeals) == 1 else None

        record.update({
            "status": ap["status"],
            "response_status": ap_payload.get("status"),
            "appeal_entries": len(appeals),
            "reasoning_word_for_word": bool(one) and one.get("reasoning") == reasoning,
            "creator_copied": bool(one) and bool(decision_before)
                              and one.get("creator_id") == decision_before[0].get("creator_id"),
            "decision_unchanged": bool(decision_before) and decisions(after) == decision_before,
            "appeal_entry": appeals[-1] if appeals else None,
        })
        results.append(record)

    for fake in made_up_ids(real_ids, trial):
        ap, ap_payload = send(http, "POST", f"{args.url}/appeal",
                              {"content_id": fake, "reasoning": reasoning}, args.timeout)
        appeals = [e for e in read_log(http, args)
                   if e.get("content_id") == fake and e.get("event") == "appeal"]
        results.append({
            "sent": f"appeal against made-up content_id {fake}",
            "status": ap["status"],
            "error": ap_payload.get("error"),
            "message": ap_payload.get("message"),
            "appeal_entries": len(appeals),
        })

    return results


def summarise(results):
    """One short token per request, for the terminal."""
    return ", ".join(str(r.get("guess") or r.get("status") or "—") for r in results)


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--trials", type=int, default=3)
    parser.add_argument("--label", default="")
    parser.add_argument("--url", default=DEFAULT_URL)
    parser.add_argument("--timeout", type=float, default=90.0)
    args = parser.parse_args()

    try:
        import requests
    except ImportError:
        print("The `requests` package isn't installed.\n"
              "Run: pip install -r requirements.txt", file=sys.stderr)
        sys.exit(1)

    try:
        import scenarios
    except ImportError:
        print("No scenarios.py found. Milestone 3 starts by filling it in.",
              file=sys.stderr)
        sys.exit(1)

    problems = scenarios.validate()
    if problems:
        print("scenarios.py has problems:\n", file=sys.stderr)
        for problem in problems:
            print(f"  - {problem}", file=sys.stderr)
        sys.exit(1)

    try:
        requests.get(f"{args.url}/health", timeout=5)
    except Exception:  # noqa: BLE001
        print(f"Nothing answering at {args.url}. Start it:  python app.py",
              file=sys.stderr)
        sys.exit(1)

    if args.trials < 3:
        print(f"!! {args.trials} trial(s). The submission asks for three.\n")

    http = requests.Session()
    rows = []
    for scenario in scenarios.SCENARIOS:
        print(f"\n{scenario['name']}  (criterion {scenario.get('criterion') or '—'})")

        trials = []
        for trial in range(1, args.trials + 1):
            if scenario.get("appeals"):
                results = appeal_trial(http, args, scenario, trial)
            else:
                results = [submit_one(http, args, body, scenario.get("check_log"))
                           for body in bodies_for(scenario)]
                if scenario.get("ping_after"):
                    results.append(ping_record(http, args))

            trials.append(results)
            print(f"  trial {trial}: {summarise(results)}")

        rows.append({"scenario": scenario, "trials": trials})

    write_report(rows, args)


def write_report(rows, args):
    config.RESULTS_DIR.mkdir(exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    label = f"_{args.label}" if args.label else ""
    path = config.RESULTS_DIR / f"run_{stamp}{label}.md"

    n = args.trials
    headers = " | ".join(f"Run {i}" for i in range(1, n + 1))
    divider = "|".join(["---"] * n)

    lines = [
        f"# Run log{f' — {args.label}' if args.label else ''}",
        "",
        "- Produced by: `run_eval.py::main` (criterion 4: `run_eval.py::appeal_trial`)",
        "- Service: `app.py::submit`, `app.py::appeal` · scoring: `scoring.py::combine_signals`",
        f"- {n} trials per criterion · {dt.datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "Fill in Target from `criteria.md`, and Run and Verdict from the output",
        "underneath. Whether a trial passed depends on the criterion you wrote.",
        "",
        f"| Criterion | Target | {headers} | Verdict |",
        f"|---|---|{divider}|---|",
    ]

    for row in rows:
        scenario = row["scenario"]
        number = scenario.get("criterion")
        name = f"{number}. {scenario['name']}" if number else scenario["name"]
        lines.append(f"| {name} |  | {' | '.join([' '] * n)} |  |")

    lines += ["", "---", "", "## What actually came back", "",
              "Real output. Paste the relevant parts into your README — the rubric",
              "asks for the actual JSON, not a description of it.", ""]

    for row in rows:
        scenario = row["scenario"]
        lines += [f"### {scenario['name']}", ""]
        for trial_number, results in enumerate(row["trials"], 1):
            lines += [f"**Trial {trial_number}**", "", "```json",
                      json.dumps(results, indent=2, ensure_ascii=False), "```", ""]

    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWrote {path.relative_to(config.ROOT)}")
    print("Commit it. It's the evidence the test actually happened.")


if __name__ == "__main__":
    main()
