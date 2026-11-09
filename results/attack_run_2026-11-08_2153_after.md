# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-08 21:53
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `024d5008-0d66-461e-a2c2-c3230b06e76f` | human | 0.669 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `e1e2874a-f7ad-476b-af78-d8896f67544a` | human | 0.799 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `8395e533-e9d6-43d3-8561-445d275ee08e` | human | 0.631 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `a8fe13cb-6d23-4672-b72a-d097df3de765` | unsure | 0.511 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `a71dd603-3759-4c31-a14a-6e16d22f2b6b` | human | 0.864 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `392df922-56e9-42a5-b66d-715973b9e100` | human | 0.714 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `1fd451e3-4847-47fd-9ece-e0b37c12e6e5` | human | 0.721 |  |
| EV08 | evasion | signal one: text below the token window | 400 | `—` | — | — |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `5fbe8f1f-c071-493b-83e9-724e0274266c` | unsure | 0.506 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `dbde2284-1cb2-4e91-a581-99ecd6975282` | ai | 0.922 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `4c2b47b7-eff3-42b4-99c5-eda4e1fac1a7` | human | 0.557 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `980ba4da-2dc2-496c-97a1-814646a61dae` | unsure | 0.649 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `80f7ba1a-5844-47d4-a5d9-400aca1865ba` | unsure | 0.707 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `883f7138-cda7-42e2-816b-3e80efda3dd7` | unsure | 0.628 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `3366fd77-b3c4-458f-aae5-ee3153d67557` | unsure | 0.713 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `b48134c2-bddb-4ed3-beb1-1c63acd5c49e` | unsure | 0.732 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `1a6a0a99-152c-4260-9132-2b27c8d91fd3` | unsure | 0.705 |  |
| FP08 | false_positive | very short genuine human submission | 400 | `—` | — | — |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `6edb34c7-4684-418a-b045-00002343389a` | human | 0.788 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `9f4e1275-80e6-4b57-b88a-b4b74e1e25db` | human | 0.923 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `0055ad11-596b-483d-9739-1cf8dc7b8717` | human | 0.670 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `5f077c37-9d08-4841-a67d-23eb8aef3a9a` | human | 0.758 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `8d45ee1f-dd92-457e-847f-477ebbefc473` | human | 0.683 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `c2bd651f-3354-44eb-aadf-30904bb915e4` | human | 0.601 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 400 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 400 | `—` | — | — |  |
| MF04 | malformed | text is only punctuation | 400 | `—` | — | — |  |
| MF05 | malformed | text is a very long single word | 400 | `—` | — | — |  |
| MF06 | malformed | text is emoji only | 400 | `—` | — | — |  |
| MF07 | malformed | text is right-to-left script | 400 | `—` | — | — |  |
| MF08 | malformed | text is 60,000 characters | 413 | `—` | — | — |  |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — |  |
| RQ02 | malformed | no creator_id | 400 | `—` | — | — |  |
| RQ03 | malformed | text is a number | 400 | `—` | — | — |  |
| RQ04 | malformed | text is a list | 400 | `—` | — | — |  |
| RQ05 | malformed | text is null | 400 | `—` | — | — |  |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — |  |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — |  |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — |  |
| RQ09 | malformed | body is empty | 400 | `—` | — | — |  |
| RQ10 | malformed | body is form-encoded, not JSON | 429 | `—` | — | — |  |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | `—` | — | — |  |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — |  |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 400 | `—` | — | — |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 400 | `—` | — | — |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 400 | `—` | — | — |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 400 | `—` | — | — |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 400 | `—` | — | — |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 0 | 20 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "024d5008-0d66-461e-a2c2-c3230b06e76f",
  "creator_id": "attacker_EV01",
  "guess": "human",
  "confidence": 0.6694,
  "model_score": 0.0176,
  "style_score": 0.8,
  "label": "This reads like it was written by a person. Nothing in it looked machine-generated to us.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "e1e2874a-f7ad-476b-af78-d8896f67544a",
  "creator_id": "attacker_EV02",
  "guess": "human",
  "confidence": 0.7991,
  "model_score": 0.2946,
  "style_score": 0.0603,
  "label": "This reads like it was written by a person. Nothing in it looked machine-generated to us.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "8395e533-e9d6-43d3-8561-445d275ee08e",
  "creator_id": "attacker_EV03",
  "guess": "human",
  "confidence": 0.6307,
  "model_score": 0.4039,
  "style_score": 0.3173,
  "label": "This reads like it was written by a person. Nothing in it looked machine-generated to us.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "a8fe13cb-6d23-4672-b72a-d097df3de765",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.511,
  "model_score": 0.3184,
  "style_score": 0.8,
  "label": "We couldn't tell from this piece how it was written, so we're not making a call. A lot of writing by real people lands here, especially very plain or very formal writing. Nothing has been flagged and nothing changes for you. If you'd still like a person to look at it, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "a71dd603-3759-4c31-a14a-6e16d22f2b6b",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.8643,
  "model_score": 0.0667,
  "style_score": 0.2392,
  "label": "This reads like it was written by a person. Nothing in it looked machine-generated to us.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "392df922-56e9-42a5-b66d-715973b9e100",
  "creator_id": "attacker_EV06",
  "guess": "human",
  "confidence": 0.7136,
  "model_score": 0.2666,
  "style_score": 0.316,
  "label": "This reads like it was written by a person. Nothing in it looked machine-generated to us.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "1fd451e3-4847-47fd-9ece-e0b37c12e6e5",
  "creator_id": "attacker_EV07",
  "guess": "human",
  "confidence": 0.7214,
  "model_score": 0.2838,
  "style_score": 0.2709,
  "label": "This reads like it was written by a person. Nothing in it looked machine-generated to us.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_EV08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "5fbe8f1f-c071-493b-83e9-724e0274266c",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.5059,
  "model_score": 0.4715,
  "style_score": 0.5281,
  "label": "We couldn't tell from this piece how it was written, so we're not making a call. A lot of writing by real people lands here, especially very plain or very formal writing. Nothing has been flagged and nothing changes for you. If you'd still like a person to look at it, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "dbde2284-1cb2-4e91-a581-99ecd6975282",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.9217,
  "model_score": 0.9895,
  "style_score": 0.8201,
  "label": "This looks like it was probably written with an AI tool. That's our best guess, not a finding about you, and it can be wrong. If you wrote this yourself, ask for a review and a person will look at it.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "4c2b47b7-eff3-42b4-99c5-eda4e1fac1a7",
  "creator_id": "attacker_FP01",
  "guess": "human",
  "confidence": 0.5568,
  "model_score": 0.3272,
  "style_score": 0.6173,
  "label": "This reads like it was written by a person. Nothing in it looked machine-generated to us.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "980ba4da-2dc2-496c-97a1-814646a61dae",
  "creator_id": "attacker_FP02",
  "guess": "unsure",
  "confidence": 0.6491,
  "model_score": 0.5386,
  "style_score": 0.8149,
  "label": "We couldn't tell from this piece how it was written, so we're not making a call. A lot of writing by real people lands here, especially very plain or very formal writing. Nothing has been flagged and nothing changes for you. If you'd still like a person to look at it, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "80f7ba1a-5844-47d4-a5d9-400aca1865ba",
  "creator_id": "attacker_FP03",
  "guess": "unsure",
  "confidence": 0.7066,
  "model_score": 0.6785,
  "style_score": 0.7488,
  "label": "We couldn't tell from this piece how it was written, so we're not making a call. A lot of writing by real people lands here, especially very plain or very formal writing. Nothing has been flagged and nothing changes for you. If you'd still like a person to look at it, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "883f7138-cda7-42e2-816b-3e80efda3dd7",
  "creator_id": "attacker_FP04",
  "guess": "unsure",
  "confidence": 0.6281,
  "model_score": 0.739,
  "style_score": 0.4618,
  "label": "We couldn't tell from this piece how it was written, so we're not making a call. A lot of writing by real people lands here, especially very plain or very formal writing. Nothing has been flagged and nothing changes for you. If you'd still like a person to look at it, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "3366fd77-b3c4-458f-aae5-ee3153d67557",
  "creator_id": "attacker_FP05",
  "guess": "unsure",
  "confidence": 0.7131,
  "model_score": 0.6686,
  "style_score": 0.7798,
  "label": "We couldn't tell from this piece how it was written, so we're not making a call. A lot of writing by real people lands here, especially very plain or very formal writing. Nothing has been flagged and nothing changes for you. If you'd still like a person to look at it, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "b48134c2-bddb-4ed3-beb1-1c63acd5c49e",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.7319,
  "model_score": 0.8409,
  "style_score": 0.5685,
  "label": "We couldn't tell from this piece how it was written, so we're not making a call. A lot of writing by real people lands here, especially very plain or very formal writing. Nothing has been flagged and nothing changes for you. If you'd still like a person to look at it, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "1a6a0a99-152c-4260-9132-2b27c8d91fd3",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.7047,
  "model_score": 0.8412,
  "style_score": 0.5,
  "label": "We couldn't tell from this piece how it was written, so we're not making a call. A lot of writing by real people lands here, especially very plain or very formal writing. Nothing has been flagged and nothing changes for you. If you'd still like a person to look at it, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_FP08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "6edb34c7-4684-418a-b045-00002343389a",
  "creator_id": "attacker_PI01",
  "guess": "human",
  "confidence": 0.7877,
  "model_score": 0.1539,
  "style_score": 0.3,
  "label": "This reads like it was written by a person. Nothing in it looked machine-generated to us.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "9f4e1275-80e6-4b57-b88a-b4b74e1e25db",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.923,
  "model_score": 0.0268,
  "style_score": 0.1524,
  "label": "This reads like it was written by a person. Nothing in it looked machine-generated to us.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "0055ad11-596b-483d-9739-1cf8dc7b8717",
  "creator_id": "attacker_PI03",
  "guess": "human",
  "confidence": 0.6698,
  "model_score": 0.2946,
  "style_score": 0.3836,
  "label": "This reads like it was written by a person. Nothing in it looked machine-generated to us.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "5f077c37-9d08-4841-a67d-23eb8aef3a9a",
  "creator_id": "attacker_PI04",
  "guess": "human",
  "confidence": 0.7585,
  "model_score": 0.1869,
  "style_score": 0.3233,
  "label": "This reads like it was written by a person. Nothing in it looked machine-generated to us.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "8d45ee1f-dd92-457e-847f-477ebbefc473",
  "creator_id": "attacker_PI05",
  "guess": "human",
  "confidence": 0.6832,
  "model_score": 0.3614,
  "style_score": 0.25,
  "label": "This reads like it was written by a person. Nothing in it looked machine-generated to us.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "c2bd651f-3354-44eb-aadf-30904bb915e4",
  "creator_id": "attacker_PI06",
  "guess": "human",
  "confidence": 0.6011,
  "model_score": 0.2491,
  "style_score": 0.6236,
  "label": "This reads like it was written by a person. Nothing in it looked machine-generated to us.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF06",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF07",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 413,
  "content_id": null,
  "creator_id": "attacker_MF08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 400,
  "content_id": null,
  "creator_id": {
    "id": "x"
  },
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
