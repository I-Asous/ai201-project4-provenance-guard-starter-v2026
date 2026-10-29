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
