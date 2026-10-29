# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- The path a submission takes, from arriving to the label a reader sees.
     Six or seven steps — this is the trace you wrote in Milestone 1. -->

1. **`POST /submit` arrives** with `{"text", "creator_id"}`: the raw words and who claims them.
2. **The route checks the input.** It needs valid JSON, 20+ words, at most 20,000 characters, and a creator_id. Bad input gets a 4xx and a `rejected` log entry. Good input gets a fresh `content_id`.
3. **Signal one, `detector.model_signal`:** gpt2 measures how predictable the text is and returns `model_score` (0–1, higher = more AI).
4. **Signal two, `stylometry.style_signal`:** measures sentence-length spread, vocabulary variety and punctuation, and returns `style_score` (0–1, higher = more AI).
5. **`scoring.combine_signals`** merges them into one `combined_score`.
6. **`scoring.score_to_label`** turns that score into a `guess`, a `confidence` and the plain-English label a reader sees.
7. **`audit.log_decision`** writes all nine fields to `logs/audit.jsonl`, and the service returns the label to the writer. They can contest it with `POST /appeal`, which appends an `under_review` entry next to the original.

Full trace, false-positive walk-through and endpoint contracts: [DESIGN.md](DESIGN.md).



---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:** Perplexity: how surprised gpt2 is by each next word in the first 400 tokens, mapped to 0–1. Low perplexity gives a high score, which means "AI".

**Why that might differ between human and AI writing:** A language model writes by picking likely next words, so its output is easy for a model to predict. People make odd choices, take abrupt turns and name specific things.

**What it can't see:** Who chose the words. It measures predictability, not authorship. Plain writing (short sentences, common vocabulary) is predictable whoever wrote it, so second-language writers, younger writers and deliberately plain writers score as AI. It also fails the other way: AI text with rare or ornate words swapped in reads as surprising, so it reads as human. It sees nothing past 400 tokens, and jargon-heavy topics push the score toward human.

### Signal two — the style signal

**What it measures:** The surface shape of the text, without reading it. That means sentence-length spread (stdev / mean of words per sentence), type–token ratio over a fixed window, and the density of "expressive" punctuation (; — : ( ) ! ?). Each is normalised and flipped so that higher = more AI, then averaged.

**Why that might differ between human and AI writing:** "Most likely next word" produces even, mid-length sentences and a narrower vocabulary. Human writing is lumpier: a three-word sentence next to a forty-word one, an aside in parentheses, a dash where a comma would do.

**What it can't see:** What the text says. Anything that changes the shape without changing the substance moves it. Typos raise word variety, chopped or merged sentences raise spread, and sprinkled dashes or a pasted quotation add punctuation. All of that is cheap to do on purpose. It is unreliable on one or two sentences. It also penalises disciplined human writers who keep sentences even, such as technical, legal or house-style writing.

### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:** Take a weighted average that leans on the model signal, because the style signal is the cheaper one to fool. If the two signals disagree by a lot, the score can't go above the top of the unsure band. A "probably AI" label needs both checks to agree. The cap only pushes down: disagreement can turn a would-be AI label into "unsure", but it never pulls a human-leaning score up into "unsure".

**The numbers:**

| Setting | Value | Where |
|---|---|---|
| Model signal weight | 0.6 | `config.WEIGHT_MODEL_SIGNAL` |
| Style signal weight | 0.4 | `config.WEIGHT_STYLE_SIGNAL` |
| Disagreement gap that triggers the cap | 0.4 | `config.DISAGREEMENT_GAP` |
| Cap when triggered | `AI_THRESHOLD − 0.01` = 0.74 | `scoring.combine_signals` |
| Human / AI thresholds | 0.45 / 0.75 | `config.HUMAN_THRESHOLD`, `config.AI_THRESHOLD` |

Two scoring changes made during calibration (Milestone 4):

- **Signal one's curve moved.** The midpoint went from perplexity 45 to 25 and the steepness from 1.6 to 2.5 (`detector.model_signal`). At 45, my clearly-human calibration texts (perplexity 26–46) scored 0.49–0.70, on the AI side of a coin flip.
- **Signal two has a plain-writing guard.** Even sentence lengths only count as AI evidence in proportion to average sentence length: not at all at 7 words or fewer, fully at 12 or more (`stylometry.PLAIN_GUARD_WORDS`). Before the guard, my plain-writer stand-in scored a perfect 1.0 on the style signal. The cost is a new blind spot: AI text told to "write in short sentences" slips under it.

Calibration, after both changes. The "clearly human" texts are a Thoreau excerpt and two paragraphs written in casual and personal-essay styles. The plain-writer text is a stand-in in the style of the person in DESIGN.md §3. Criterion 1 needs your own writing.

| Input | model | style | combined | label |
|---|---|---|---|---|
| Generic AI (AI ethics) | 0.81 | 0.80 | 0.81 | ai |
| Generic AI (exercise) | 0.92 | 0.77 | 0.86 | ai |
| Generic AI (climate) | 0.96 | 0.80 | 0.90 | ai |
| Thoreau, *Walden* opening | 0.47 | 0.39 | 0.44 | human |
| Casual human (late bus) | 0.24 | 0.00 | 0.14 | human |
| Personal essay (button jar) | 0.18 | 0.31 | 0.23 | human |
| **Plain human writer** | 0.78 | 0.50 | **0.67** | **unsure** |
| Lightly edited AI | 0.27 | 0.30 | 0.28 | human ← a miss |

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**A case where my two signals split, and what my rule does with it:**

An AI-style paragraph written in ornate, rare vocabulary ("The crepuscular cityscape exudes an ineffable melancholy…"), with five even, mid-length sentences:

- `model_score` **0.16**. Rare words are exactly what gpt2 can't predict, so it reads as very human. This is signal one's blind spot.
- `style_score` **0.80**. Sentences march in step and there's no expressive punctuation, so it looks AI.
- They differ by 0.64, so the cap applies, but the weighted average is already only 0.42. The result is **0.42 → human**.

The rule did what it was designed to do: it didn't accuse anyone on half the evidence. But in this case the half it trusted was the half being fooled, so AI text got through. That's the trade I chose in DESIGN.md §3. A missed detection costs the site a little; a wrong accusation costs a writer a lot. Unit 8 will tell me how many of these get through.


---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00 – 0.45 (below 0.45) | This reads like it was written by a person. Nothing in it looked machine-generated to us. |
| unsure | 0.45 – 0.75 (from 0.45, below 0.75) | We can't tell either way, so we're not making a call on this one. Plain, clear writing often looks like this, and many people write this way themselves. Nothing has been flagged and nothing changes for you. If you'd like a person to take a look, you can ask for a review. |
| high-confidence AI | 0.75 – 1.00 (0.75 and up) | This looks like it was probably written with an AI tool. Both of our checks pointed the same way, but they can be wrong. If you wrote this yourself, ask for a review and a person will look at it. Nothing is final until then. |

All three are reachable, as the calibration table above and the Sample Run show. The text lives in `scoring.py` (`LABEL_HUMAN`, `LABEL_UNSURE`, `LABEL_AI`).

**Why I worded the "unsure" one this way:**
<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->

The person most likely to get "unsure" is the plain writer from DESIGN.md §3. In calibration, that's exactly where she landed. So the label is written for her:

- **"We can't tell either way"** says the uncertainty is ours, not something wrong with her writing.
- **"Plain, clear writing often looks like this, and many people write this way themselves"** tells her *why* we couldn't tell, and that it isn't a mark against her. Without that, "unsure" reads as "suspected".
- **"Nothing has been flagged and nothing changes for you"** answers the first thing she'd worry about.
- **"If you'd like a person to take a look"** offers the appeal without implying she needs one.

It avoids "AI", "detected", "score" and "confidence". None of those words help someone who has never heard of a threshold.



---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

A test input: generic AI-generated text about exercise.

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "Regular exercise offers numerous benefits for both physical and mental health. It helps to strengthen the heart, improve circulation, and maintain a healthy weight. In addition, exercise can reduce stress and improve overall mood. Many experts recommend at least thirty minutes of moderate activity each day. It is also important to choose activities that you enjoy, as this makes it easier to stay consistent. Overall, incorporating exercise into your daily routine is one of the best ways to improve your quality of life.", "creator_id": "islam"}'
```

```json
{
  "combined_score": 0.8606,
  "confidence": 0.8606,
  "content_id": "0e30ed66-6666-4fdf-bd67-b5ad42028eb1",
  "creator_id": "islam",
  "guess": "ai",
  "label": "This looks like it was probably written with an AI tool. Both of our checks pointed the same way, but they can be wrong. If you wrote this yourself, ask for a review and a person will look at it. Nothing is final until then.",
  "model_score": 0.9194,
  "status": "decided",
  "style_score": 0.7724
}
```

**An appeal**

The appeal's reasoning is role-played test input, to exercise the path.

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "0e30ed66-6666-4fdf-bd67-b5ad42028eb1", "reasoning": "I wrote this for a health class handout. It sounds generic because the assignment asked for a neutral summary."}'
```

```json
{
  "content_id": "0e30ed66-6666-4fdf-bd67-b5ad42028eb1",
  "message": "Thanks. Your appeal is recorded and a person will review this decision. The original result is on hold until then.",
  "original_label": "This looks like it was probably written with an AI tool. Both of our checks pointed the same way, but they can be wrong. If you wrote this yourself, ask for a review and a person will look at it. Nothing is final until then.",
  "status": "under_review"
}
```

An appeal against an id that doesn't exist:

```json
{"error": "unknown_content_id", "message": "We couldn't find a submission with id not-a-real-id. Check it matches the one you were given."}
```
(HTTP 404; nothing is written to the log.)

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=3"
```

```json
{
  "count": 3,
  "entries": [
    {
      "content_id": "7f11a761-51db-45df-871a-eed8e6a0a8b4",
      "creator_id": "islam",
      "event": "appeal",
      "reasoning": "I wrote this myself for my English class. I keep my sentences simple on purpose.",
      "status": "under_review",
      "timestamp": "2026-10-29T00:27:21+00:00"
    },
    {
      "combined_score": 0.8606,
      "content_id": "0e30ed66-6666-4fdf-bd67-b5ad42028eb1",
      "creator_id": "islam",
      "guess": "ai",
      "label": "This looks like it was probably written with an AI tool. Both of our checks pointed the same way, but they can be wrong. If you wrote this yourself, ask for a review and a person will look at it. Nothing is final until then.",
      "model_score": 0.9194,
      "status": "decided",
      "style_score": 0.7724,
      "timestamp": "2026-10-29T00:27:30+00:00"
    },
    {
      "content_id": "0e30ed66-6666-4fdf-bd67-b5ad42028eb1",
      "creator_id": "islam",
      "event": "appeal",
      "reasoning": "I wrote this for a health class handout. It sounds generic because the assignment asked for a neutral summary.",
      "status": "under_review",
      "timestamp": "2026-10-29T00:27:30+00:00"
    }
  ]
}
```

The original decision is still there, unchanged. The appeal sits after it, and the `creator_id` on the appeal comes from the decision, not from the request. The first entry is an appeal from an earlier test submission.

Refused input leaves a trace too. Here's the 250,000-character body, answered with a 413 before the model ran:

```json
{"timestamp": "2026-10-29T00:27:21+00:00", "creator_id": "b6", "event": "rejected", "status": "rejected", "reason": "text_too_long", "http_status": 413, "text_length": 250000}
```

---

## How I Used AI

**Moment 1**

- *What I asked for:* I pasted the Milestone 1 brief into Claude Code and asked it to complete the trace, both signals' blind spots, the false-positive walk-through and the two endpoint contracts.
- *What came back:* DESIGN.md. Its first draft defined `confidence` in a self-contradicting sentence. Claude caught that and rewrote it as `max(score, 1 − score)`. It also picked concrete bounds (20 words minimum, 20,000 characters maximum) and a target AI threshold of ~0.80 that I hadn't specified.
- *What I changed:* <!-- TODO (you): what you kept, rejected or rewrote, in your own words -->

**Moment 2**

- *What I asked for:* "Fill out everything necessary": build the style signal, the scoring, both routes, and the README.
- *What came back:* Before choosing any weights, Claude ran both signals on calibration text. The results changed the design:
  - Type–token ratio barely separated AI from human, so it got the lowest weight.
  - The plain-writer stand-in scored a perfect 1.0 on the style signal. That led to the plain-writing guard.
  - Signal one's midpoint of 45 put human essays on the AI side, so it moved to 25.

  With the original numbers, the person in my false-positive trace would have been labelled AI.
- *What I changed:* <!-- TODO (you): e.g. whether you agree with the guard's trade, replaced the stand-in calibration text with your own writing, reworded a label -->

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
