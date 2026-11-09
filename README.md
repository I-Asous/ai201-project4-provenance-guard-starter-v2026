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

**Run on its own before wiring it in (Milestone 3):**

```
$ python detector.py "Artificial intelligence is transforming the way we live and work. From healthcare to education, ..."
perplexity     12.2
model_signal   0.8579   (higher = more likely AI)

$ python detector.py "Okay so the bus was late again. Third time this week! I stood there in the rain like an idiot, ..."
perplexity     52.9
model_signal   0.1330   (higher = more likely AI)

$ python detector.py "Remote work has changed a lot about how teams operate, honestly more than most of us expected. ..."
perplexity     37.0
model_signal   0.2732   (higher = more likely AI)
```

Sure-AI, sure-human, in-between. It puts them in the right order, but the in-between one (AI text with a few human touches) already leans human, at 0.27. A couple of short sentences and an "honestly" were enough to move it. These runs use the recalibrated curve (midpoint 25), described under The combining rule.

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

**Signal two on its own, from a terminal (Milestone 4):**

```
$ python stylometry.py "Artificial intelligence is transforming the way we live and work. From healthcare to education, AI technologies are being used to improve efficiency and enhance outcomes. However, it is important to consider the ethical implications of these advancements."
3 sentences, 37 words

sentence_length_spread   0.204
type_token_ratio         0.8649
punctuation_density      0.0
style_signal             0.8   (higher = more likely AI)
```

**Both signals over the same pieces.** These are the three Milestone 3 pieces, plus the formal-human input the brief asks for. I used two public-domain formal texts.

| Input | words | model_score | style_score | combined | label |
|---|---|---|---|---|---|
| M3 sure-AI | 37 | 0.86 | 0.80 | 0.83 | ai |
| M3 sure-human | 35 | 0.13 | 0.10 | 0.12 | human |
| M3 in-between (lightly edited AI) | 37 | 0.27 | 0.30 | 0.28 | human |
| Formal human: *Federalist No. 1*, opening | 133 | 0.36 | **0.78** | 0.53 | unsure |
| Formal human: Darwin, *Origin*, introduction | 107 | 0.43 | 0.58 | 0.49 | unsure |

- **They agree on the clear cases.** Both say AI on the sure-AI piece and human on the sure-human one, so clear AI and clear human score 0.71 apart.
- **They agree on the in-between piece too, and both are wrong.** Two short sentences and an "honestly" moved *both* signals, so the rule had nothing to resolve. Lightly edited AI comes through as human. That's the miss I expect unit 8 to hit hardest.
- **They split on formal human writing.** The case is below.

**A case where my two signals split, and what my rule does with it:**

*Federalist No. 1*, written by a person in 1787:

- `model_score` **0.36**. Signal one leans human. Words like "inefficacy" and "subsisting" are hard for gpt2 to predict.
- `style_score` **0.78**. Signal two leans AI. Looking at its three measures:
  - Sentence-length spread is 0.37. The sentences are all long, so they look even.
  - Type–token ratio is 0.75. "The" and "of" repeat across the long sentences.
  - Expressive punctuation is 0.75 per 100 words. It's written in commas, which I deliberately don't count.
- They differ by 0.42, which is past the 0.4 gap, so the cap applies. The weighted average is already 0.53, so the result is **unsure**.

The writer isn't accused. That's what the cap is for: one signal alone can't put a real person in the AI band. But they don't get "human" either, so formal writing pays a cost in this system.

The other direction exists too. An AI-style paragraph in ornate vocabulary ("The crepuscular cityscape exudes an ineffable melancholy…") scores model **0.16**, style **0.80**, and combined **0.42 → human**. The rule trusts the human-leaning signal, and here that signal is the one being fooled. That's the trade from DESIGN.md §3: a miss rather than an accusation.

**Findings to carry into unit 8:**

- **Type–token ratio doesn't discriminate the way I expected.** It scored 0.00 AI-ness on every AI text (generated prose is varied enough at 40–100 words). It only pushed toward AI on human text: plain (1.00), formal (0.70–0.77) and Thoreau (0.44). It's kept at weight 0.20 so I can measure it in unit 8, but on this evidence it adds false-positive pressure and catches nothing.
- **Signal two reads formal human prose as AI-leaning**, for the three reasons in the Federalist breakdown above. If my own writing is formal, criterion 1's "at least 5 of 10 human" is at risk.
- **The log records all three numbers.** Every `decided` entry has `model_score`, `style_score` and `combined_score`, as the Sample Run's log output shows.

---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00 – 0.45 (below 0.45) | This reads like it was written by a person. Nothing in it looked machine-generated to us. |
| unsure | 0.45 – 0.75 (from 0.45, below 0.75) | We couldn't tell from this piece how it was written, so we're not making a call. A lot of writing by real people lands here, especially very plain or very formal writing. Nothing has been flagged and nothing changes for you. If you'd still like a person to look at it, you can ask for a review. |
| high-confidence AI | 0.75 – 1.00 (0.75 and up) | This looks like it was probably written with an AI tool. That's our best guess, not a finding about you, and it can be wrong. If you wrote this yourself, ask for a review and a person will look at it. |

All three are reachable, as the calibration table above and the Sample Run show. The text lives in `scoring.py` (`LABEL_HUMAN`, `LABEL_UNSURE`, `LABEL_AI`).

**Why I worded the "unsure" one this way:**
<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->

The people who land in "unsure" are mostly real writers: the plain writer from DESIGN.md §3 (0.67) and formal writers like *Federalist No. 1* (0.53). The label is written for them:

- **"We couldn't tell from this piece how it was written"** puts the uncertainty on us and on this one piece, not on the writer.
- **"A lot of writing by real people lands here, especially very plain or very formal writing"** says why, with both of the causes I actually observed. It reassures without assuming anything about this writer's style.
- **"Nothing has been flagged and nothing changes for you"** answers the first worry.
- **"If you'd still like a person to look at it"** offers the appeal without implying they need one.

It avoids "AI", "detected", "score" and "confidence".

**Reader check (Milestone 5).** Working alone, I read all three labels as the writer: what does this say about me, and what would I do next? Here's what that turned up:

| Label | What the writer heard | What they'd do |
|---|---|---|
| human | "They checked me for cheating, but I passed." | Nothing. |
| unsure (v1) | "Plain, clear writing often looks like this" = *they think my writing is simple*. That's wrong and stings for a formal writer. "Many people write this way **themselves**" sounds like they're defending me against a suspicion, which raises it. "Nothing has been flagged" next to "ask for a review" leaves them asking what there is to review. | Ignore it uneasily, or appeal just to clear their name. |
| AI (v1) | "Both of our checks pointed the same way" sounds like the evidence is piling up. "Nothing is final until then" makes them ask what becomes final, and implies a penalty. | Appeal anxiously, believing something bad happens if they don't. |

What I changed:

- **Unsure:** dropped "plain, clear" (formal writers land here too) and "themselves", and named both causes I'd observed.
- **AI:** replaced "both of our checks" with "our best guess, not a finding about you", and removed "nothing is final until then". This service doesn't penalise anyone, so the label shouldn't suggest it might.

The v1 wording:

> *unsure v1:* We can't tell either way, so we're not making a call on this one. Plain, clear writing often looks like this, and many people write this way themselves. Nothing has been flagged and nothing changes for you. If you'd like a person to take a look, you can ask for a review.
>
> *AI v1:* This looks like it was probably written with an AI tool. Both of our checks pointed the same way, but they can be wrong. If you wrote this yourself, ask for a review and a person will look at it. Nothing is final until then.

---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission.** I ran one for each label to show all three are reachable. These are test inputs: generic AI text, my plain-writer stand-in from DESIGN.md §3, and a casual human-style paragraph.

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. -->

*High-confidence AI*

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "Regular exercise offers numerous benefits for both physical and mental health. It helps to strengthen the heart, improve circulation, and maintain a healthy weight. In addition, exercise can reduce stress and improve overall mood. Many experts recommend at least thirty minutes of moderate activity each day. It is also important to choose activities that you enjoy, as this makes it easier to stay consistent. Overall, incorporating exercise into your daily routine is one of the best ways to improve your quality of life.", "creator_id": "islam"}'
```

```json
{
  "combined_score": 0.8606,
  "confidence": 0.8606,
  "content_id": "12398bcc-0729-4957-8727-a0db5ee06490",
  "creator_id": "islam",
  "guess": "ai",
  "label": "This looks like it was probably written with an AI tool. That's our best guess, not a finding about you, and it can be wrong. If you wrote this yourself, ask for a review and a person will look at it.",
  "model_score": 0.9194,
  "status": "decided",
  "style_score": 0.7724
}
```

*Unsure*

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "I moved to this city in November. It was very cold. I did not have a good coat. My neighbor gave me her old coat. It was too big but I wore it every day. I took the bus to my English class. The class was in the morning. My teacher was kind. She helped me with my writing. I wrote about my family and my country. I miss my mother and my sisters. We talk on the phone on Sundays. Now it is spring and the weather is better. I am happy that I came here.", "creator_id": "islam"}'
```

```json
{
  "combined_score": 0.6676,
  "confidence": 0.6676,
  "content_id": "556dbdf9-0516-4750-82be-904398d93485",
  "creator_id": "islam",
  "guess": "unsure",
  "label": "We couldn't tell from this piece how it was written, so we're not making a call. A lot of writing by real people lands here, especially very plain or very formal writing. Nothing has been flagged and nothing changes for you. If you'd still like a person to look at it, you can ask for a review.",
  "model_score": 0.7793,
  "status": "decided",
  "style_score": 0.5
}
```

*High-confidence human*

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "Okay so the bus was late again. Third time this week! I stood there in the rain like an idiot, checking the app every thirty seconds, and it kept saying two minutes for about twenty. When it finally came the driver just shrugged. Fine. Whatever. I got to work soaked, my boss gave me that look (you know the one), and the coffee machine was broken.", "creator_id": "islam"}'
```

```json
{
  "combined_score": 0.0977,
  "confidence": 0.9023,
  "content_id": "f99e3d3e-eb94-4be2-a5c6-7058a92eb526",
  "creator_id": "islam",
  "guess": "human",
  "label": "This reads like it was written by a person. Nothing in it looked machine-generated to us.",
  "model_score": 0.1629,
  "status": "decided",
  "style_score": 0.0
}
```

**An appeal** against the AI-labelled submission above, using its real `content_id`:

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "12398bcc-0729-4957-8727-a0db5ee06490", "reasoning": "Testing the appeal path: contesting this AI label to check it moves to under_review."}'
```

```json
{
  "content_id": "12398bcc-0729-4957-8727-a0db5ee06490",
  "message": "Thanks. Your appeal is recorded and a person will review this decision. The original result is on hold until then.",
  "original_label": "This looks like it was probably written with an AI tool. That's our best guess, not a finding about you, and it can be wrong. If you wrote this yourself, ask for a review and a person will look at it.",
  "status": "under_review"
}
```

An appeal against an id that doesn't exist returns HTTP 404, and nothing is written to the log:

```json
{"error": "unknown_content_id", "message": "We couldn't find a submission with id not-a-real-id. Check it matches the one you were given."}
```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=4"
```

```json
{
  "count": 4,
  "entries": [
    {
      "combined_score": 0.8606,
      "content_id": "12398bcc-0729-4957-8727-a0db5ee06490",
      "creator_id": "islam",
      "guess": "ai",
      "label": "This looks like it was probably written with an AI tool. That's our best guess, not a finding about you, and it can be wrong. If you wrote this yourself, ask for a review and a person will look at it.",
      "model_score": 0.9194,
      "status": "decided",
      "style_score": 0.7724,
      "timestamp": "2026-10-29T01:50:12+00:00"
    },
    {
      "combined_score": 0.6676,
      "content_id": "556dbdf9-0516-4750-82be-904398d93485",
      "creator_id": "islam",
      "guess": "unsure",
      "label": "We couldn't tell from this piece how it was written, so we're not making a call. A lot of writing by real people lands here, especially very plain or very formal writing. Nothing has been flagged and nothing changes for you. If you'd still like a person to look at it, you can ask for a review.",
      "model_score": 0.7793,
      "status": "decided",
      "style_score": 0.5,
      "timestamp": "2026-10-29T01:50:12+00:00"
    },
    {
      "combined_score": 0.0977,
      "content_id": "f99e3d3e-eb94-4be2-a5c6-7058a92eb526",
      "creator_id": "islam",
      "guess": "human",
      "label": "This reads like it was written by a person. Nothing in it looked machine-generated to us.",
      "model_score": 0.1629,
      "status": "decided",
      "style_score": 0.0,
      "timestamp": "2026-10-29T01:50:12+00:00"
    },
    {
      "content_id": "12398bcc-0729-4957-8727-a0db5ee06490",
      "creator_id": "islam",
      "event": "appeal",
      "reasoning": "Testing the appeal path: contesting this AI label to check it moves to under_review.",
      "status": "under_review",
      "timestamp": "2026-10-29T01:50:12+00:00"
    }
  ]
}
```

The first entry is the original AI decision, with `status: decided`. The last is the appeal against the same `content_id`, with `status: under_review`. The log is append-only, so the decision isn't overwritten: the appeal sits next to it, and the item's current status is that of its latest entry. The appeal's `creator_id` is copied from the decision, not taken from the request.

Refused input leaves a trace too. Here's a 250,000-character body, answered with a 413 before the model ran:

```json
{"timestamp": "2026-10-29T00:27:21+00:00", "creator_id": "b6", "event": "rejected", "status": "rejected", "reason": "text_too_long", "http_status": 413, "text_length": 250000}
```

---

## How I Used AI

**Moment 1**

- *What I asked for:* I pasted the Milestone 1 brief into Claude Code and asked it to complete the trace, both signals' blind spots, the false-positive walk-through and the two endpoint contracts.
- *What came back:* DESIGN.md. Its first draft defined `confidence` in a self-contradicting sentence. Claude caught that and rewrote it as `max(score, 1 − score)`. It also picked concrete bounds (20 words minimum, 20,000 characters maximum) and a target AI threshold of ~0.80 that I hadn't specified.
- *What I changed:* Nothing in the text. I read DESIGN.md against the brief and kept it as written, including the bounds and the ~0.80 threshold target it chose. My decision was to treat it as the contract: everything I asked for afterwards had to match DESIGN.md §4, rather than letting the code redefine the endpoints.

**Moment 2**

- *What I asked for:* "Fill out everything necessary": build the style signal, the scoring, both routes, and the README.
- *What came back:* Before choosing any weights, Claude ran both signals on calibration text. The results changed the design:
  - Type–token ratio barely separated AI from human, so it got the lowest weight.
  - The plain-writer stand-in scored a perfect 1.0 on the style signal. That led to the plain-writing guard.
  - Signal one's midpoint of 45 put human essays on the AI side, so it moved to 25.

  With the original numbers, the person in my false-positive trace would have been labelled AI.
- *What I changed:* I kept the code, weights and thresholds as they came back. What I controlled was the process. I ran the milestones one at a time and had each one checked against its own "before you move on" list. I also declined to let Claude push to GitHub and pushed myself. I'm knowingly accepting two of its trades: lightly edited AI gets labelled human, and the calibration "human" texts are stand-ins. Unit 8's run against my own writing (criterion 1) is where I'll find out whether accepting them was right.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** 5 per minute, 50 per day

**Why those numbers and not others:**

- **The writer.** Someone checking their own work submits a piece, edits a paragraph, and checks again. That's one submission every minute or two. Five a minute leaves room for a quick burst of revisions. On a heavy writing day they might check 10–20 times, so 50 a day is well above what a real person needs. If they do hit the minute limit, they wait under a minute. Nothing is lost.
- **The script.** Mapping my thresholds means sending hundreds or thousands of small variations and watching where the label flips. At 50 a day, 1,000 variations take 20 days on one creator_id. At 5 a minute, it can't fire off a quick burst either. Each submission also runs the language model for a second or two, so the per-minute limit protects the service, not just the thresholds.
- **Why not tighter.** At 2 or 3 a minute, a writer pasting in a few short pieces back to back would hit the limit during normal use. Below about 30 a day, one long editing session could use up the whole day's allowance.

**What a caller counts as:** the `creator_id` in the request body, falling back to the caller's address when there isn't one (`rate_limit_key` in `app.py`). This is fair to a household or classroom behind one address, because each writer gets their own count. The weakness is that `creator_id` is self-reported. A script that invents a new `creator_id` on every request is a new caller each time and never hits a limit. That's how the attack set gets through (every row is `attacker_<id>`). Per-creator limits stop a careless flood. They don't stop someone who reads the API. Closing that gap needs a second limit keyed on address, or a `creator_id` the service issues itself.

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```
200 200 200 200 200 429 429 429 429 429 429 429 429 429 429
```

All ten 429s are in `logs/audit.jsonl` as `rejected` entries with `"reason": "rate_limited"`, `"limit": "5 per 1 minute"` and `"counted_as": "flood_tester"`. Every log line (decision, appeal or rejection) carries the same nine fields: `timestamp`, `content_id`, `creator_id`, `guess`, `model_score`, `style_score`, `combined_score`, `label`, `status`. A field that doesn't apply is `null`, not missing. Rejections from `/submit` and `/appeal` record `reason`, `http_status` and `route`. Appeals copy the contested decision's scores and label, so the appeal line shows what was challenged without looking up the original.

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->

Produced by `python run_attacks.py --set attack_set --label before`, against the service on port 5055. Raw output: [results/attack_run_2026-11-08_1530_before.md](results/attack_run_2026-11-08_1530_before.md). The runner only marks crashes, and there were none (no 5xx in 56), so every verdict below is mine.

**How I called held or broke.** An attack held if the service did what it should with that input:

- **evasion** (AI text in disguise) held only if it was labelled AI. Unsure counts as broke, because "unsure" flags nothing, so the disguise worked.
- **false_positive** (real human writing that looks machine-made) held unless it was labelled AI. Unsure and a refusal both hold, because nobody was accused.
- **prompt_injection** held if the injected text didn't get what it aimed at: a human label for AI text, a changed label, or a corrupted log line.
- **malformed** and **flood** held if refused with an accurate 4xx and logged. A crash, or a refusal that gives a false reason, broke.

`Combined` is the score the thresholds apply to (human below 0.45, AI from 0.75), read from each attack's log line. For a refused request, `Result` is the error code from the log.

| ID | Family | Targeting | Status | Result | Combined | Verdict | Why |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | human | 0.331 | **BROKE** | typos sent signal one from 0.41 to 0.02 |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | human | 0.201 | **BROKE** | sentence fragments sent signal two from 0.80 to 0.06 |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | human | 0.369 | **BROKE** | the quotation sent signal two from 0.80 to 0.32 |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | unsure | 0.511 | **BROKE** | unsure, not AI: rare words sent signal one from 0.41 to 0.32 |
| EV05 | evasion | both signals: heavy human editing pass | 200 | human | 0.136 | **BROKE** | rewritten so heavily both signals read human |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | human | 0.286 | **BROKE** | uneven sentences sent signal two from 0.80 to 0.32 |
| EV07 | evasion | signal two: padding with punctuation | 200 | human | 0.279 | **BROKE** | extra punctuation sent signal two from 0.80 to 0.27 |
| EV08 | evasion | signal one: text below the token window | 400 | `text_too_short` | — | **HELD** | refused: under 20 words, never scored |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | unsure | 0.494 | **BROKE** | unsure, not AI: the human opening lowered signal two |
| EV10 | evasion | signal two: repeated stanza structure | 200 | ai | 0.922 | **HELD** | labelled AI |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | human | 0.443 | **HELD** | labelled human |
| FP02 | false_positive | human writing in a formal register | 200 | unsure | 0.649 | **HELD** | unsure, so nobody accused |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | unsure | 0.707 | **HELD** | unsure, so nobody accused |
| FP04 | false_positive | a student essay written to a rubric | 200 | unsure | 0.628 | **HELD** | unsure, so nobody accused |
| FP05 | false_positive | technical documentation written by a person | 200 | unsure | 0.713 | **HELD** | unsure, but only 0.04 below the AI line |
| FP06 | false_positive | a person imitating a formal template | 200 | unsure | 0.732 | **HELD** | unsure, but only 0.02 below the AI line |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | unsure | 0.705 | **HELD** | unsure, so nobody accused |
| FP08 | false_positive | very short genuine human submission | 400 | `text_too_short` | — | **HELD** | refused (8 words), so nobody accused |
| PI01 | prompt_injection | instruction to ignore the check | 200 | human | 0.212 | **BROKE** | AI text labelled human: the instruction's odd wording raised perplexity |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | human | 0.077 | **BROKE** | AI text labelled human: the instruction's odd wording raised perplexity |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | human | 0.330 | **BROKE** | AI text labelled human: the instruction's odd wording raised perplexity |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | human | 0.241 | **HELD** | label is fixed text; real human text labelled human |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | human | 0.317 | **HELD** | text is never logged; the log line is intact |
| PI06 | prompt_injection | instruction plus real human text | 200 | human | 0.399 | **HELD** | real human text labelled human |
| MF01 | malformed | text is only whitespace | 400 | `missing_text` | — | **HELD** | refused cleanly |
| MF02 | malformed | text is a single character | 400 | `text_too_short` | — | **HELD** | refused cleanly |
| MF03 | malformed | text is control characters | 400 | `text_too_short` | — | **HELD** | refused cleanly |
| MF04 | malformed | text is only punctuation | 400 | `text_too_short` | — | **HELD** | refused cleanly |
| MF05 | malformed | text is a very long single word | 400 | `text_too_short` | — | **HELD** | refused cleanly |
| MF06 | malformed | text is emoji only | 400 | `text_too_short` | — | **HELD** | refused cleanly |
| MF07 | malformed | text is right-to-left script | 400 | `text_too_short` | — | **BROKE** | Arabic counted as 0 words, so refused with a false reason |
| MF08 | malformed | text is 60,000 characters | 413 | `text_too_long` | — | **HELD** | refused cleanly |
| RQ01 | malformed | no text field at all | 400 | `missing_text` | — | **HELD** | refused cleanly |
| RQ02 | malformed | no creator_id | 400 | `missing_creator_id` | — | **HELD** | refused cleanly |
| RQ03 | malformed | text is a number | 400 | `missing_text` | — | **HELD** | refused cleanly |
| RQ04 | malformed | text is a list | 400 | `missing_text` | — | **HELD** | refused cleanly |
| RQ05 | malformed | text is null | 400 | `missing_text` | — | **HELD** | refused cleanly |
| RQ06 | malformed | creator_id is an object | 400 | `missing_creator_id` | — | **HELD** | refused cleanly |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `invalid_json` | — | **HELD** | refused cleanly |
| RQ08 | malformed | body is unparseable JSON | 400 | `invalid_json` | — | **HELD** | refused cleanly |
| RQ09 | malformed | body is empty | 400 | `invalid_json` | — | **HELD** | refused cleanly |
| RQ10 | malformed | body is form-encoded, not JSON | 429 | `rate_limited` | — | **HELD** | 429 from the shared per-address count; sent alone it's 400 invalid_json |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | `rate_limited` | — | **HELD** | 429 from the shared per-address count; sent alone it's 400 invalid_json |
| RQ12 | malformed | deeply nested JSON | 400 | `missing_text` | — | **HELD** | refused cleanly |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 400 | `text_too_short` | — | **HELD** | refused (9 words), and counted toward the limit |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 400 | `text_too_short` | — | **HELD** | refused (9 words), and counted toward the limit |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 400 | `text_too_short` | — | **HELD** | refused (9 words), and counted toward the limit |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 400 | `text_too_short` | — | **HELD** | refused (9 words), and counted toward the limit |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 400 | `text_too_short` | — | **HELD** | refused (9 words), and counted toward the limit |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 429 | `rate_limited` | — | **HELD** | rate limited |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | `rate_limited` | — | **HELD** | rate limited |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | `rate_limited` | — | **HELD** | rate limited |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `rate_limited` | — | **HELD** | rate limited |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `rate_limited` | — | **HELD** | rate limited |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `rate_limited` | — | **HELD** | rate limited |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `rate_limited` | — | **HELD** | rate limited |

| Family | Attacks | Held | Broke |
|---|---|---|---|
| `evasion` | 10 | 2 | 8 |
| `false_positive` | 8 | 8 | 0 |
| `prompt_injection` | 6 | 3 | 3 |
| `malformed` | 20 | 19 | 1 |
| `flood_same_creator` | 12 | 12 | 0 |
| **all** | **56** | **44** | **12** |

**12 of 56 broke:** 8 evasion, 3 prompt injection and 1 malformed. Nothing crashed, no real writer was labelled AI, and the rate limit held. Eleven of the twelve are AI text that wasn't flagged; the twelfth is a writer refused for a false reason. The diagnoses are under Run Log and Verdicts.

Two follow-ups beyond the table:

- **RQ10 and RQ11 were stopped by the rate limiter before the route saw them.** Neither body has a `creator_id` the limiter can read, so both counted against the shared address, which five earlier malformed requests had already used up. Sent again on their own, both get a `400 invalid_json` ([recheck RQ10](results/attack_run_2026-11-08_2135_recheck_RQ10.md), [recheck RQ11](results/attack_run_2026-11-08_2135_recheck_RQ11.md)). They held either way, but the first answer, "Too many submissions", was the wrong reason.
- **The flood's first five requests were refused as too short** (9 words), and they still counted toward the limit, so the 429 arrived on the sixth. The Milestone 1 flood, using text long enough to score, showed the same cut-off: 200 ×5, then 429.

**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

These are verbatim lines from `logs/audit.jsonl`, in this order:

1. EV01: AI text labelled human through signal one
2. PI02: AI text labelled human through signal one
3. EV02: AI text labelled human through signal two
4. EV10: the one evasion caught
5. FP06: a real writer close to an accusation
6. FP05: a real writer close to an accusation
7. MF07: Arabic refused as "0 words"
8. RQ10: a malformed body rate-limited by the shared address count
9. FL01_06: the flood's first 429
10. PI05: a log-injection attempt that left the line intact

```json
{"timestamp": "2026-11-08T20:30:52+00:00", "content_id": "5ca18720-d84c-4e66-98b4-f77fecdd8fbd", "creator_id": "attacker_EV01", "guess": "human", "model_score": 0.0176, "style_score": 0.8, "combined_score": 0.3306, "label": "This reads like it was written by a person. Nothing in it looked machine-generated to us.", "status": "decided"}
{"timestamp": "2026-11-08T20:30:52+00:00", "content_id": "ca098b3b-b290-4b1e-b154-1070ffff77c4", "creator_id": "attacker_PI02", "guess": "human", "model_score": 0.0268, "style_score": 0.1524, "combined_score": 0.077, "label": "This reads like it was written by a person. Nothing in it looked machine-generated to us.", "status": "decided"}
{"timestamp": "2026-11-08T20:30:52+00:00", "content_id": "c460145b-5df6-49dc-bfc8-0b88ad4ac3c7", "creator_id": "attacker_EV02", "guess": "human", "model_score": 0.2946, "style_score": 0.0603, "combined_score": 0.2009, "label": "This reads like it was written by a person. Nothing in it looked machine-generated to us.", "status": "decided"}
{"timestamp": "2026-11-08T20:30:52+00:00", "content_id": "789489e8-a4cc-435e-b4fa-6edd00a45f51", "creator_id": "attacker_EV10", "guess": "ai", "model_score": 0.9895, "style_score": 0.8201, "combined_score": 0.9217, "label": "This looks like it was probably written with an AI tool. That's our best guess, not a finding about you, and it can be wrong. If you wrote this yourself, ask for a review and a person will look at it.", "status": "decided"}
{"timestamp": "2026-11-08T20:30:52+00:00", "content_id": "64a7b27a-8799-489c-8d26-2c3c9844bd96", "creator_id": "attacker_FP06", "guess": "unsure", "model_score": 0.8409, "style_score": 0.5685, "combined_score": 0.7319, "label": "We couldn't tell from this piece how it was written, so we're not making a call. A lot of writing by real people lands here, especially very plain or very formal writing. Nothing has been flagged and nothing changes for you. If you'd still like a person to look at it, you can ask for a review.", "status": "decided"}
{"timestamp": "2026-11-08T20:30:52+00:00", "content_id": "5c8e3488-ade2-436d-a470-f500b52bc6c6", "creator_id": "attacker_FP05", "guess": "unsure", "model_score": 0.6686, "style_score": 0.7798, "combined_score": 0.7131, "label": "We couldn't tell from this piece how it was written, so we're not making a call. A lot of writing by real people lands here, especially very plain or very formal writing. Nothing has been flagged and nothing changes for you. If you'd still like a person to look at it, you can ask for a review.", "status": "decided"}
{"timestamp": "2026-11-08T20:30:53+00:00", "content_id": null, "creator_id": "attacker_MF07", "guess": null, "model_score": null, "style_score": null, "combined_score": null, "label": null, "status": "rejected", "event": "rejected", "reason": "text_too_short", "http_status": 400, "route": "/submit", "text_length": 105}
{"timestamp": "2026-11-08T20:30:53+00:00", "content_id": null, "creator_id": "unknown", "guess": null, "model_score": null, "style_score": null, "combined_score": null, "label": null, "status": "rejected", "event": "rejected", "reason": "rate_limited", "http_status": 429, "route": "/submit", "limit": "5 per 1 minute", "counted_as": "127.0.0.1"}
{"timestamp": "2026-11-08T20:30:53+00:00", "content_id": null, "creator_id": "attacker_flood", "guess": null, "model_score": null, "style_score": null, "combined_score": null, "label": null, "status": "rejected", "event": "rejected", "reason": "rate_limited", "http_status": 429, "route": "/submit", "limit": "5 per 1 minute", "counted_as": "attacker_flood"}
{"timestamp": "2026-11-08T20:30:53+00:00", "content_id": "09841089-0a95-4f77-95ba-9227154f86a3", "creator_id": "attacker_PI05", "guess": "human", "model_score": 0.3614, "style_score": 0.25, "combined_score": 0.3168, "label": "This reads like it was written by a person. Nothing in it looked machine-generated to us.", "status": "decided"}
```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:

**MF07, the Arabic text.** The service told the writer "That's 0 words. We need at least 20 to say anything useful." The text has 17 words, and its length isn't the problem. The route counts words with `stylometry.words()`, which matches only `[a-z0-9']`, so Arabic counts as zero words at any length. A 204-word version still counts as 0 ([results/diagnosis_2026-11-08_2137.md](results/diagnosis_2026-11-08_2137.md), section 4).

Anyone writing in Arabic, Chinese, Russian or any other non-Latin script can never get a decision, and the reason they're given is untrue. The evasion breaks are misses I accepted on purpose in DESIGN.md §3. This one shuts a real writer out and tells them something false about their own writing.

The closest call on an accusation was FP06, a cover letter written to a template, which scored 0.732: 0.018 below the AI line.


---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

Produced by `python run_eval.py --label before`, against the service on port 5055. Full output: [results/run_2026-11-08_1555_before.md](results/run_2026-11-08_1555_before.md).

> ⚠️ **Criterion 1 ran on stand-ins, not my own writing.** No real writing was supplied for this run. The ten "my own writing" pieces in `scenarios.py` (`MY_WRITING`) were written by Claude in the style of ordinary personal writing: three plain on purpose, seven looser. Two of the seven also stand in for "my own non-plain writing" in criterion 2's human set. A MET on criterion 1 here shows how the service treats human-*style* text from a model. It says nothing about how it treats mine.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. My own writing is never called AI *(stand-ins)* | 0 of 10 AI **and** ≥ 5 of 10 human | 0 AI, 8 human | 0 AI, 8 human | 0 AI, 8 human | MET (on stand-ins) |
| 2. Clearly-AI and clearly-human text score far apart | AI mean ≥ 0.30 above human mean **and** ≥ 4 of 5 AI above the top human | gap 0.43, 4 of 5 | gap 0.43, 4 of 5 | gap 0.43, 4 of 5 | MET |
| 3. All three labels reachable, borderline lands in unsure | 3 of 3 labels, ≥ 2 of 3 borderline unsure, 0 split inputs labelled AI | 3 of 3, 3 of 3, 0 | 3 of 3, 3 of 3, 0 | 3 of 3, 3 of 3, 0 | MET (revised criterion: also MET) |
| 4. Every appeal changes status and is recorded | 10 of 10 real appeals **and** 3 of 3 made-up ids refused | 10/10, 3/3 | 10/10, 3/3 | 10/10, 3/3 | MET |
| 5. Bad input is refused cleanly, never crashes | 7 of 7 4xx with error + message, 7 of 7 logged, huge one < 2 s, /ping answers | 7/7, 7/7, 0.001 s, 200 | 7/7, 7/7, 0.001 s, 200 | 7/7, 7/7, 0.001 s, 200 | MET |

**How I called each verdict.** Each target had to hold in all three trials, and every part of a criterion joined by "and" had to hold too.

1. **MET, on stand-ins only.** Both halves held every time: 0 AI (the target is 0) and 8 human (the target is at least 5). The criterion is about pieces *I wrote myself*, and none of these were, so as written it is untested. The verdict covers the stand-ins and nothing more.
2. **MET.** The gap was 0.43 against a 0.30 target. Exactly 4 of the 5 AI texts scored above the top human text (0.4713) in every trial, which is the minimum. The fifth, at 0.4649, is the one miss the target allows.
3. **MET as written, and MET as revised.** All three labels appeared in every trial, all three borderline inputs were unsure, and both inputs that split by 0.4 or more were unsure. As written, though, I couldn't fix which inputs counted as "borderline" until after the run. That made it a broken criterion, not a missed one, so I revised it in `criteria.md` (original kept, revision underneath). Under the revision, the three fixed borderline inputs went 3 of 3 unsure.
4. **MET.** An appeal counted only if all five checks were true at once: a 200 with `under_review`, exactly one appeal entry, the reasoning identical, the creator copied, and the decision unchanged. That held for 10 of 10 real appeals, and 3 of 3 made-up ids were refused, in every trial.
5. **MET.** In every trial, 7 of 7 got a 4xx with both `error` and `message`, and 7 of 7 had a matching `rejected` log line. The huge body took 0.001 s, and `/ping` returned 200 afterwards.

**Arguing against my own verdicts.** I argued the opposite verdict as hard as I could on the two closest calls, then went looking for evidence that would settle each.

- **Criterion 1 should not count as MET.** The criterion names "pieces I wrote myself", and the run used none. The argument is right, and the table says so. *What would settle it:* ten real pieces, run three times. That evidence isn't in this repo.
- **Criterion 2 only passed by luck.** 4 of 5 is the minimum, and the fifth AI text sits 0.006 below the top human. If the pass depends on this exact set of AI texts, the margin means nothing. *What would settle it:* a second set of five unedited AI texts against the same five humans. I ran one ([results/diagnosis_2026-11-08_2137.md](results/diagnosis_2026-11-08_2137.md), section 5). The gap was 0.50, and **5 of 5** scored above the top human. The verdict stands. The reading-benefits text in the first set is a hard case, not evidence that the separation is luck.

**What's behind each row**

- **All three trials are identical**, to four decimal places, on every input. gpt2 runs in eval mode under `no_grad` with no sampling (`detector.py`), and the style signal is arithmetic, so a stable pipeline should look exactly like this.
- **Criterion 1.** No piece came near AI; the highest scored 0.60. The plain pieces did worst, as DESIGN.md §3 predicted. Two of the three landed unsure (0.60 and 0.51), and the third got "human" by 0.004 (0.4463 against the 0.45 line). All seven looser pieces were human (0.11–0.40).
- **Criterion 2** passed its overlap check with no room to spare. The reading-benefits AI text scored 0.4649, just *below* Hazlitt's essay at 0.4713, so it is the one AI text that doesn't clear the top human. Hazlitt scores that high because his signals split: model 0.24, style 0.82. The criterion doesn't count this, but only 3 of the 5 unedited AI texts were labelled AI. The other two landed unsure (0.71 and 0.46).
- **Criterion 3.** Two inputs split by 0.4 or more: Hazlitt (0.58) and *Federalist No. 1* (0.47). Both were labelled unsure, never AI. The ornate AI text was included as borderline because a similar paragraph split 0.16 / 0.80 in Milestone 4. This one scored 0.42 / 0.79, a 0.36 gap, so it didn't split, though it still landed unsure. The lightly edited AI text landed unsure at 0.4688, only 0.019 above the human line. In Milestone 4 a different light edit of the same kind of paragraph scored 0.28, which is human, so this pass is fragile.
- **Criterion 4 was tested by script, not by hand** as `criteria.md` planned. I extended `run_eval.py` with `appeal_trial`. It submits each of ten texts (covering all three labels), appeals the returned `content_id` and reads `/log`. Then it appeals three ids that were never issued: a one-character typo of a real id, a fresh UUID, and `my-essay-<n>`. That's 39 appeals across three trials, all handled correctly.
- **Criterion 5.** The 250,000-character body was refused in about a millisecond, so the size check runs before the model. Every refusal's `rejected` log line names the same reason and status the caller got (`log_matches`). One weakness the criterion doesn't measure: five of the seven get the same `missing_text` code and message, whether the caller sent nothing, whitespace, `null` or the number 12345.

**Real output from trial 1**, pasted verbatim from `results/run_2026-11-08_1555_before.md`. It was produced by `run_eval.py::main` (criterion 4 by `run_eval.py::appeal_trial`) from the responses of `app.py::submit` and `app.py::appeal`. `sent` is `run_eval.py`'s short note of what it sent; the full texts are in `scenarios.py`.

**Criterion 1**: the three plain stand-ins, which are the riskiest of the ten (entries 1–3 of 10).

```json
[
  {
    "status": 200,
    "elapsed_s": 3.515,
    "content_id": "3d508644-1417-4f77-a3ea-f11b26d986e2",
    "guess": "human",
    "confidence": 0.5537,
    "model_score": 0.4169,
    "style_score": 0.4904,
    "combined_score": 0.4463,
    "label": "This reads like it was written by a person. Nothing in it looked machine-generated to us.",
    "sent": "I work at a grocery store on weekends. I mostly stock shelves. Sometim… (567 characters)"
  },
  {
    "status": 200,
    "elapsed_s": 0.058,
    "content_id": "0bb3e847-41e5-4c0f-b7c6-aff97b059769",
    "guess": "unsure",
    "confidence": 0.5999,
    "model_score": 0.6576,
    "style_score": 0.5134,
    "combined_score": 0.5999,
    "label": "We couldn't tell from this piece how it was written, so we're not making a call. A lot of writing by real people lands here, especially very plain or very formal writing. Nothing has been flagged and nothing changes for you. If you'd still like a person to look at it, you can ask for a review.",
    "sent": "My brother and I fixed his bike on Sunday. The chain kept falling off.… (544 characters)"
  },
  {
    "status": 200,
    "elapsed_s": 0.054,
    "content_id": "e9a68d6d-9688-4a40-ad9c-73a4f605dabc",
    "guess": "unsure",
    "confidence": 0.5067,
    "model_score": 0.5448,
    "style_score": 0.4495,
    "combined_score": 0.5067,
    "label": "We couldn't tell from this piece how it was written, so we're not making a call. A lot of writing by real people lands here, especially very plain or very formal writing. Nothing has been flagged and nothing changes for you. If you'd still like a person to look at it, you can ask for a review.",
    "sent": "Last winter our heater stopped working. It was a Tuesday in January. W… (528 characters)"
  }
]
```

**Criterion 2**: the lowest-scoring AI text and the highest-scoring human text, the pair that decides the overlap check (entries 5 and 8 of 10).

```json
[
  {
    "status": 200,
    "elapsed_s": 0.053,
    "content_id": "e772dc87-5307-4c18-b212-f3724f20d8fc",
    "guess": "unsure",
    "confidence": 0.5351,
    "model_score": 0.5404,
    "style_score": 0.3516,
    "combined_score": 0.4649,
    "label": "We couldn't tell from this piece how it was written, so we're not making a call. A lot of writing by real people lands here, especially very plain or very formal writing. Nothing has been flagged and nothing changes for you. If you'd still like a person to look at it, you can ask for a review.",
    "sent": "Reading regularly provides numerous benefits for personal growth and d… (672 characters)"
  },
  {
    "status": 200,
    "elapsed_s": 0.061,
    "content_id": "fe2ef0e4-9d75-47ea-a83e-1f5831e54702",
    "guess": "unsure",
    "confidence": 0.5287,
    "model_score": 0.2411,
    "style_score": 0.8167,
    "combined_score": 0.4713,
    "label": "We couldn't tell from this piece how it was written, so we're not making a call. A lot of writing by real people lands here, especially very plain or very formal writing. Nothing has been flagged and nothing changes for you. If you'd still like a person to look at it, you can ask for a review.",
    "sent": "One of the pleasantest things in the world is going a journey; but I l… (605 characters)"
  }
]
```

**Criterion 3**: the three borderline inputs (entries 7–9 of 9).

```json
[
  {
    "status": 200,
    "elapsed_s": 0.062,
    "content_id": "415c71a0-3f31-4a52-8e7b-c13288dcc7a6",
    "guess": "unsure",
    "confidence": 0.5004,
    "model_score": 0.3144,
    "style_score": 0.7794,
    "combined_score": 0.5004,
    "label": "We couldn't tell from this piece how it was written, so we're not making a call. A lot of writing by real people lands here, especially very plain or very formal writing. Nothing has been flagged and nothing changes for you. If you'd still like a person to look at it, you can ask for a review.",
    "sent": "After an unequivocal experience of the inefficacy of the subsisting fe… (809 characters)"
  },
  {
    "status": 200,
    "elapsed_s": 0.062,
    "content_id": "af555af1-ba06-4c04-bf00-c06e17fde06f",
    "guess": "unsure",
    "confidence": 0.5685,
    "model_score": 0.4229,
    "style_score": 0.7868,
    "combined_score": 0.5685,
    "label": "We couldn't tell from this piece how it was written, so we're not making a call. A lot of writing by real people lands here, especially very plain or very formal writing. Nothing has been flagged and nothing changes for you. If you'd still like a person to look at it, you can ask for a review.",
    "sent": "The crepuscular cityscape exudes an ineffable melancholy as the last v… (664 characters)"
  },
  {
    "status": 200,
    "elapsed_s": 0.048,
    "content_id": "dee0d4ef-695c-45d6-b62d-769794d43e90",
    "guess": "unsure",
    "confidence": 0.5312,
    "model_score": 0.3112,
    "style_score": 0.7053,
    "combined_score": 0.4688,
    "label": "We couldn't tell from this piece how it was written, so we're not making a call. A lot of writing by real people lands here, especially very plain or very formal writing. Nothing has been flagged and nothing changes for you. If you'd still like a person to look at it, you can ask for a review.",
    "sent": "Remote work has changed a lot about how teams operate, honestly more t… (509 characters)"
  }
]
```

**Criterion 4**: an appeal against a real AI decision, and one against a one-character typo of a real id (entries 1 and 11 of 13).

```json
[
  {
    "sent": "submit as eval_appeal_1, then appeal its content_id",
    "submit_status": 200,
    "submit_guess": "ai",
    "content_id": "da10c95b-07d5-4a42-86e2-740d00769929",
    "status": 200,
    "response_status": "under_review",
    "appeal_entries": 1,
    "reasoning_word_for_word": true,
    "creator_copied": true,
    "decision_unchanged": true,
    "appeal_entry": {
      "combined_score": 0.7523,
      "content_id": "da10c95b-07d5-4a42-86e2-740d00769929",
      "creator_id": "eval_appeal_1",
      "decided_at": "2026-11-08T20:55:32+00:00",
      "event": "appeal",
      "guess": "ai",
      "label": "This looks like it was probably written with an AI tool. That's our best guess, not a finding about you, and it can be wrong. If you wrote this yourself, ask for a review and a person will look at it.",
      "model_score": 0.7205,
      "reasoning": "I wrote every word of this myself — it's from my notebook, the part about my grandmother's café. I'd like a person to read it again, please.",
      "status": "under_review",
      "style_score": 0.8,
      "timestamp": "2026-11-08T20:55:32+00:00"
    }
  },
  {
    "sent": "appeal against made-up content_id da10c95b-07d5-4a42-86e2-740d00769920",
    "status": 404,
    "error": "unknown_content_id",
    "message": "We couldn't find a submission with id da10c95b-07d5-4a42-86e2-740d00769920. Check it matches the one you were given.",
    "appeal_entries": 0
  }
]
```

**Criterion 5**: the 250,000-character body, the JSON list, and the /ping afterwards (entries 6–8 of 8).

```json
[
  {
    "status": 413,
    "elapsed_s": 0.001,
    "error": "text_too_long",
    "message": "That's 250,000 characters. The limit is 20,000.",
    "sent": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx… (250,000 characters)",
    "log_entry": {
      "combined_score": null,
      "content_id": null,
      "creator_id": "eval_bad_huge",
      "event": "rejected",
      "guess": null,
      "http_status": 413,
      "label": null,
      "model_score": null,
      "reason": "text_too_long",
      "route": "/submit",
      "status": "rejected",
      "style_score": null,
      "text_length": 250000,
      "timestamp": "2026-11-08T20:55:34+00:00"
    },
    "log_matches": true
  },
  {
    "status": 400,
    "elapsed_s": 0.001,
    "error": "invalid_json",
    "message": "Send a JSON object like {\"text\": \"...\", \"creator_id\": \"...\"}.",
    "sent": "[\"text\", \"creator_id\"]",
    "log_entry": {
      "combined_score": null,
      "content_id": null,
      "creator_id": "unknown",
      "event": "rejected",
      "guess": null,
      "http_status": 400,
      "label": null,
      "model_score": null,
      "reason": "invalid_json",
      "route": "/submit",
      "status": "rejected",
      "style_score": null,
      "timestamp": "2026-11-08T20:55:34+00:00"
    },
    "log_matches": true
  },
  {
    "status": 200,
    "elapsed_s": 0.001,
    "ok": true,
    "sent": "POST /ping, after the trial"
  }
]
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

The numbers below come from the attack run and from [results/diagnosis_2026-11-08_2137.md](results/diagnosis_2026-11-08_2137.md). That file is produced by `python diagnose.py`, which scores text with the same functions `/submit` calls.

**Criteria: no misses, and my targets were too low.** All five held in all three trials, so no criterion miss needs diagnosing. Here is why that result is weaker than it looks:

- **Criteria 4 and 5 test plumbing I'd already built to pass them.** Criterion 5's 2-second bound was beaten about 2,000 times over.
- **Criterion 3's last clause can't fail.** `combine_signals` caps any score whose signals differ by 0.4 or more at 0.74, which is below the AI line. The check confirms the code does what it says. It doesn't test whether the design is right.
- **Criterion 1 ran on stand-ins easier than the people it's meant to protect.** My stand-ins got 8 of 10 human. The attack set's false-positive family got 1 of 7 human and 6 unsure. That family covers plain, formal, non-native, rubric-written, technical, template and deliberately repetitive writing. Run against those seven, the "at least 5 human" half of criterion 1 would have missed.
- **Nothing measures whether AI text gets caught.** I made the criteria one-sided on purpose, because an accusation costs more than a miss. That left the service's biggest weakness outside every target. Two of my five unedited AI texts weren't labelled AI, and neither was the attack set's AI paragraph before any attack touched it.

**The criterion I'd tighten is 2.** I'd add: *at least 4 of the 5 unedited AI texts are labelled high-confidence AI in every trial.* This run would miss it at 3 of 5. That's the point of adding it: it's the one number that would have shown the evasion failures coming.

**Broken attacks: 12, from three problems.**

**Problem 1: the AI text started in "unsure" before any attack (stage: signal one).** Most evasion and injection attacks are built from one generic AI paragraph about workplace communication; EV09's second paragraph is that paragraph, untouched.

- **Scored on its own, the paragraph lands in unsure.** Its perplexity is 29.0. Signal one maps perplexity to a score with its midpoint at 25 (`detector.model_signal`), so 29.0 gives **0.41**, on the human side. Combined with style 0.80, that's **0.5655, unsure**.
- **The midpoint is mine.** I moved it from 45 to 25 in Milestone 4 so that human essays would stop scoring as AI. My calibration AI texts sat at perplexity 7–14; this paragraph sits at 29.
- **The same thing caught criterion 2.** Its reading-benefits AI text (perplexity 23.4, model 0.54) landed unsure the same way.
- **So the attacks only needed a small push.** None had to carry AI text from "AI" to "human"; each only had to move it from 0.57 to below 0.45.

**Problem 2: one fooled signal is enough (stage: the combining rule).** The combined score is 0.6 × model + 0.4 × style, and the disagreement cap only ever pulls a score down. That has two consequences:

- **A near-zero model score guarantees "human".** The combined score can be at most 0.40, below the 0.45 line, whatever signal two says.
- **A near-zero style score rules out "AI".** The combined score can be at most 0.60, below the 0.75 line.

Neither signal can hold a score up when the other is fooled. Each attack below fooled one signal and got through.

*Through signal one: rare tokens raise perplexity.* (EV01, EV04, EV05, PI01–PI03)

- **EV01 (typos).** Perplexity went from 29.0 to 124.8, and the model score from 0.41 to **0.02**. Misspellings like "poistioned" and "thsi" split into rare word pieces gpt2 can't predict. Signal two didn't move at all (0.80 before and after). The attack set aimed this one at signal two, but in my service the stage is signal one. Combined 0.33, human.
- **PI01–PI03 (injected instructions).** Nothing in the service reads instructions, so none were obeyed. The instructions worked as *unusual text*. PI02's "SYSTEM: …" line raised perplexity from 22.3 (the AI part alone) to 105.2, and the model score fell from 0.57 to 0.03. With the instruction cut off, all three AI fragments score unsure (0.46–0.59); with it, they score human (0.08–0.33). That makes this the same mechanism as the typos.
- **EV04 (rare words like "desiderata").** Perplexity went from 29.0 to 33.9 and the model score from 0.41 to 0.32. It was a smaller push and stopped at unsure (0.51).
- **EV05 (heavy human edit).** Model 0.07, style 0.24, combined 0.14. After an edit that heavy, a person has largely rewritten the text. This is the one break I'd accept.

*Through signal two: sentence shape.* (EV02, EV03, EV06, EV07, EV09)

Signal two measures sentence-length spread, word variety and expressive punctuation. The paragraph's even, mid-length sentences score 0.80. Each of these edits raises spread or punctuation without changing a word of the argument:

- EV02, sentences broken into fragments: 0.06
- EV06, one very long sentence next to a very short one: 0.32
- EV03, a pasted quotation: 0.32
- EV07, sprinkled dashes and brackets: 0.27
- EV09, a human opening paragraph: 0.53

Signal one was already at 0.27–0.47 on these, and problem 2 did the rest: four labelled human, and EV09 unsure.

**Problem 3: MF07 (stage: the route).** `/submit` counts words with `stylometry.words()`, which matches only `[a-z0-9']`. Arabic, or any other non-Latin script, counts as zero words, so the route refuses it as `text_too_short` and says "That's 0 words". A 204-word Arabic text still counts as 0. The same regex also splits accented words ("café" becomes "caf"), which changes the word-variety measure for French or Spanish writing.

**The pattern.** Problems 1 and 2 account for 11 of the 12 breaks, and they're the same design choice seen from two sides. I tuned the service so that every error falls toward "human", which is DESIGN.md §3's trade: a miss rather than an accusation. The attack run shows how little push it takes to get there: one fooled signal, starting from a paragraph that was already in unsure. The false-positive family shows the other side of that trade. No real writer was accused, but four of them sat within 0.05 of the AI line, so the margin protecting them is thin as well.

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
