# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---
## 1. My own writing is never called AI

Of 10 pieces I wrote myself, **0** are labelled high-confidence AI in **every
one of the three trials**, and **at least 5 of 10** are labelled
high-confidence human. At least 3 of the 10 are written plainly on purpose:
short sentences, everyday words, no flourishes.

**Why this target:** On a writing site a wrong accusation costs the writer far
more than a missed detection costs the site. I designed the AI label to need
both signals strongly agreeing, so a single accusation of my own work means
that design failed. The "at least 5 human" half stops me passing by shoving
everything into "unsure", which would accuse nobody and tell nobody anything.
The plain pieces are there because plain writing is what signal one is known
to misread (see DESIGN.md §3), so a test without them would be too easy.

---

## 2. Clearly-AI and clearly-human text score far apart

Across 5 texts I'm confident are AI-generated (unedited model output) and 5
I'm confident are human (my own non-plain writing plus published personal
essays), the **mean `combined_score` of the AI set is at least 0.30 higher than
the mean of the human set** in every trial. **At least 4 of the 5 AI texts
score above the highest-scoring human text.**

**Why this target:** If the clear cases don't separate, no choice of
thresholds can fix it, and the labels are just noise. 0.30 is the width of my
planned unsure band (roughly 0.45–0.80), so a smaller gap means even the easy
cases could end up on the wrong side of it. The overlap check catches a mean
being dragged up by one extreme text while the rest overlap.

---

## 3. All three labels are reachable, and borderline text lands in "unsure"

Of 9 inputs (3 clearly AI, 3 clearly human, 3 borderline: lightly hand-edited
AI text, or text where `model_score` and `style_score` differ by 0.4 or more),
**each of the three labels is produced at least once in every trial**, and
**at least 2 of the 3 borderline inputs are labelled unsure** in every trial.
**No input whose two signals differ by 0.4 or more is ever labelled
high-confidence AI.**

**Why this target:** A label nobody can reach is a gap in the ranges, and a
service that only ever says "unsure" is useless. Two signals disagreeing is
exactly the uncertainty the unsure label exists for, so calling a split case AI
would be accusing someone on half the evidence.

---

## 4. Every appeal changes status and is recorded

For **10 of 10** appeals against real `content_id`s: the response is `200` with
`"status": "under_review"`, `/log` gains **exactly one** appeal entry with that
`content_id`, the writer's reasoning stored word for word, and the
`creator_id` copied from the original decision, and the original decision entry
is **still there, unchanged**. For **3 of 3** appeals with a made-up
`content_id`, the response is `404` with `"error": "unknown_content_id"` and
**no** appeal entry is written.

**Why this target:** The appeal is the only thing between a wrong accusation
and nothing at all, so it has to work every time; 9 of 10 means one writer's
appeal vanished. The made-up-id half checks the most common silent failure: a
typo'd id that "succeeds" while recording nothing anyone can find. This one is
tested by hand (submit, then appeal with the returned id), because
`run_eval.py` only sends submissions.

---

## 5. Bad input is refused cleanly, never crashes

Of 7 malformed `/submit` requests (empty `text`, whitespace-only `text`, no
`text` field, `"text": null`, `"text": 12345`, a 250,000-character text, and a
body that is a JSON list instead of an object), **7 of 7** return a `4xx` (never
a `500`) with an `error` code and a readable `message`, **7 of 7** leave a
`rejected` entry in the audit log, the enormous one gets its response **in
under 2 seconds**, and `/ping` still answers afterwards.

**Why this target:** A crash on malformed input is one of the most common real
failures, and a 500 tells the caller nothing about what to fix. The log entry
matters because an attack that only shows up as an absence is one I'll never
find. The 2-second limit proves the size check runs *before* the model, so
nobody can tie up the service by sending a novel.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
