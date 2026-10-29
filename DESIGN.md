# Provenance Guard — Milestone 1 design

Written before any of `/submit`, `/appeal`, `stylometry.py` or `scoring.py` was
built. This is the contract the rest of the build has to keep.

---

## 1. The path a submission takes

1. **The writer's client sends `POST /submit`** with a JSON body
   `{"text": ..., "creator_id": ...}`. *Adds:* the raw words and who claims them.

2. **The route in `app.py` checks the input.** Is the body JSON, is `text` a
   string, is it long enough to score (≥ 20 words) and short enough to score in
   reasonable time (≤ 20,000 characters), is `creator_id` present? Bad input is
   refused with a 4xx *and* written to the log with `audit.log_rejection`.
   *Adds:* a guarantee that every later stage receives text it can actually
   measure, and a `content_id` (a fresh UUID) that names this submission from
   here on.

3. **Signal one — `detector.model_signal(text)`.** gpt2 reads the text locally
   and measures how predictable it is (perplexity), squashed onto 0–1.
   *Adds:* `model_score` — higher means more AI-like.

4. **Signal two — `stylometry.style_signal(text)`.** Measures the shape of the
   text without reading it: sentence-length spread, type–token ratio,
   punctuation density, each normalised and flipped so higher means more AI.
   *Adds:* `style_score` — higher means more AI-like.

5. **The combining rule — `scoring.combine_signals(model_score, style_score)`.**
   Merges the two into one 0–1 number. *Adds:* `combined_score`, the single
   number the decision is made on.

6. **The label mapping — `scoring.score_to_label(combined_score)`.** Compares
   the score against `HUMAN_THRESHOLD` and `AI_THRESHOLD` in `config.py`.
   *Adds:* `guess` (`human` / `unsure` / `ai`), `confidence`, and the plain
   sentence a reader sees.

7. **The audit log, then the response.** `audit.log_decision(...)` writes all
   nine fields (timestamp, content_id, creator_id, guess, model_score,
   style_score, combined_score, label, status=`decided`) to
   `logs/audit.jsonl`; the route returns the response below. *Adds:* a
   permanent record the writer can appeal against, and the label on screen.

If the writer disagrees, a second, shorter path starts: `POST /appeal` →
check the `content_id` exists in the log → `audit.log_appeal(...)` appends an
`under_review` entry beside the original (nothing is overwritten) → confirm to
the writer.

---

## 2. The two signals

### Signal one — the model signal (`detector.py`, given)

- **What it measures:** perplexity — how surprised gpt2 is by each next word,
  averaged over the first 400 tokens, turned into a 0–1 score with a logistic
  around perplexity 45. Low perplexity → high score → "AI".
- **Why it might differ:** a language model writes by repeatedly picking a
  likely next word, so its output is text a model finds easy to predict.
  Humans make odd word choices, take abrupt turns, and name specific things,
  which a model can't anticipate.
- **What it can't see:** *who chose the words.* It measures predictability,
  not authorship. Plain writing — short sentences, common vocabulary — is
  predictable whoever wrote it, so second-language writers, younger writers and
  people writing simply on purpose score as AI. The reverse also fails: AI text
  prompted to use rare or ornate vocabulary, or AI text with a few unusual
  words swapped in, becomes "surprising" and reads as human. It also knows
  nothing past 400 tokens, and its reading drifts with topic (technical topics
  full of jargon read as surprising).

### Signal two — the style signal (`stylometry.py`, mine)

- **What it measures:** the shape of the text as a sequence of characters,
  without understanding it:
  - *sentence-length spread* — coefficient of variation (stdev / mean) of
    words per sentence. Low spread → more AI.
  - *type–token ratio* — unique words / total words, over a fixed-size window
    so length doesn't dominate. Low variety → more AI.
  - *punctuation density* — semicolons, dashes, colons, parentheses,
    exclamation and question marks per sentence (not full stops, which every
    writer uses). Low/uniform → more AI.

  Each is normalised to 0–1, flipped so higher = more AI, and averaged.
- **Why it might differ:** "most likely next word" produces even, mid-length
  sentences and a narrower band of vocabulary on average. Human writing is
  lumpier: a three-word sentence next to a forty-word one, an aside in
  parentheses, a dash where a comma would do.
- **What it can't see:** *anything the text says.* Only the surface shape
  moves it, so anything that changes the shape without changing the substance
  fools it: adding typos (raises word variety), chopping or merging sentences
  (raises spread), sprinkling in dashes or a pasted quotation. That's cheap to
  do on purpose. It is also unreliable on short text — one or two sentences
  have no spread to measure — and it penalises disciplined human writers who
  keep sentences even (technical writing, legal writing, anyone taught a
  house style).

**Why two signals and not one:** they fail differently. Signal one is fooled by
word choice, signal two by structure. An attacker has to beat both, and when
they disagree that disagreement is itself information (see §3).

---

## 3. Tracing the false positive

**Who:** Amira learned English as an adult. She writes a 250-word personal essay
about her first winter in a new city herself, with no AI. She deliberately
sticks to words she's sure of and short, clear sentences, because that's how
she was taught to avoid mistakes.

**Through the service:**

| Stage | What happens to Amira's essay |
|---|---|
| Route | Valid — 250 words, has a creator_id. Gets `content_id` `c-…`. |
| Signal one | Common words, simple grammar → gpt2 finds it very predictable. Perplexity ≈ 25 → `model_score` ≈ **0.72**. |
| Signal two | Sentences are all 8–14 words, vocabulary repeats, almost no punctuation beyond full stops → `style_score` ≈ **0.70**. |
| Combine | Both signals point the same wrong way, so an average gives ≈ **0.71**. |
| Label | Over the placeholder `AI_THRESHOLD` of 0.65 → **high-confidence AI**. |

**What the label said to her:** with the placeholder thresholds, a sentence
telling her the essay was most likely machine-written, about work she wrote
every word of. On a writing site that is an accusation, and it lands on the
person with the least room to argue back in fluent English.

**What she can do about it:** the response gives her a `content_id` and the
label tells her she can appeal. She sends `POST /appeal` with that id and a
sentence of reasoning. The service appends an `under_review` entry next to the
original decision (the original stays in the log, unaltered), and replies with
a confirmation she can keep. It doesn't automatically re-score: a person reviews
it.

**What this decides about thresholds:** her case is the reason the bands are
lopsided. Both of my signals reward exactly the features her writing has, so
when the signals *agree* at ~0.7 that isn't strong evidence; it's two
measures of "plain". So:

- the **AI threshold goes high** (target ~0.80, final number set in Milestone 4
  from the calibration inputs, including a plain human paragraph). An AI label
  should need both signals strongly agreeing;
- the **unsure band is wide** and its label must not read as an accusation;
- **when the signals split** (one says AI, one says human) the result lands in
  *unsure*, never *AI*;
- **every label, including AI, tells the reader they can appeal and how.**

The cost: more lightly-edited AI text will land in "unsure" instead of "AI". A
missed detection costs the site a little; a wrong accusation costs Amira a lot.
I'm choosing the first.

---

## 4. Endpoint contracts

All requests and responses are JSON (`Content-Type: application/json`). Every
error response has the same shape: `{"error": "<machine_code>", "message":
"<sentence a person can read>"}`.

### `POST /submit`

**Request**

| Field | Type | Required | Rules |
|---|---|---|---|
| `text` | string | yes | 20+ words after trimming whitespace; at most 20,000 characters |
| `creator_id` | string | yes | non-empty; identifies the writer, used for appeals and (unit 8) rate limits |

Extra fields are ignored.

**Response — `200 OK`**

| Field | Type | Meaning |
|---|---|---|
| `content_id` | string (UUID4) | Names this submission. Needed for `/appeal`. |
| `creator_id` | string | Echoed back from the request. |
| `guess` | `"human"` \| `"unsure"` \| `"ai"` | Machine-readable verdict. |
| `confidence` | float 0.5–1 | How far the score leans away from a coin flip: `max(combined_score, 1 − combined_score)`. So it equals `combined_score` for an `ai` guess and `1 − combined_score` for a `human` guess; near 0.5 means the service really doesn't know. |
| `label` | string | The full sentence a reader sees, plain English, no numbers. |
| `model_score` | float 0–1 | Signal one. Higher = more AI-like. |
| `style_score` | float 0–1 | Signal two. Higher = more AI-like. |
| `combined_score` | float 0–1 | Output of `scoring.combine_signals`. Higher = more AI-like. |
| `status` | `"decided"` | Lifecycle state; becomes `under_review` after an appeal. |

Example:

```json
{
  "content_id": "3f2a9c1e-8b4d-4e2a-9f61-0c7d5b8a2e14",
  "creator_id": "amira",
  "guess": "unsure",
  "confidence": 0.71,
  "label": "We can't tell whether this was written by a person or with AI help. ...",
  "model_score": 0.72,
  "style_score": 0.70,
  "combined_score": 0.71,
  "status": "decided"
}
```

**Errors** (each also written to the log with `audit.log_rejection`)

| Status | `error` | When |
|---|---|---|
| 400 | `invalid_json` | body missing, not JSON, or not a JSON object |
| 400 | `missing_text` | `text` absent, not a string, or empty/whitespace |
| 400 | `missing_creator_id` | `creator_id` absent, not a string, or empty |
| 400 | `text_too_short` | fewer than 20 words |
| 413 | `text_too_long` | more than 20,000 characters |
| 429 | `rate_limited` | over the rate limit (unit 8; handler already in `app.py`) |
| 503 | `detector_unavailable` | the model couldn't be loaded |

### `POST /appeal`

**Request**

| Field | Type | Required | Rules |
|---|---|---|---|
| `content_id` | string | yes | must match a `content_id` already in the audit log |
| `reasoning` | string | yes | non-empty; the writer's explanation, stored verbatim |

The `creator_id` for the log entry is taken from the original decision, not
from the request, so nobody can appeal under someone else's name by typing it.

**Response — `200 OK`**

| Field | Type | Meaning |
|---|---|---|
| `content_id` | string | Echoed back. |
| `status` | `"under_review"` | New lifecycle state. |
| `message` | string | Plain-English confirmation, e.g. "Thanks — your appeal is recorded and a person will review this decision. The original result is on hold until then." |
| `original_label` | string | The label being appealed, so the writer sees what they're contesting. |

Appealing twice is allowed; each appeal is appended and the status stays
`under_review`.

**Errors**

| Status | `error` | When |
|---|---|---|
| 400 | `invalid_json` | body missing, not JSON, or not a JSON object |
| 400 | `missing_content_id` | `content_id` absent or empty |
| 400 | `missing_reasoning` | `reasoning` absent or empty |
| 404 | `unknown_content_id` | no decision in the log has that id |

### Read-back check

Could someone build a client against this without asking me a question?
Every field has a type, a direction (all scores: higher = more AI), and an
allowed set of values; every failure has a status code and a fixed error
code; the appeal says where `creator_id` comes from. The one thing left
open on purpose is the exact label wording and the threshold numbers, which
are Milestone 4/5 decisions, and a client shouldn't depend on them; it should
branch on `guess`, not parse `label`.
