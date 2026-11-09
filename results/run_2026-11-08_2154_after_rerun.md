# Run log — after_rerun

- Produced by: `run_eval.py::main` (criterion 4: `run_eval.py::appeal_trial`)
- Service: `app.py::submit`, `app.py::appeal` · scoring: `scoring.py::combine_signals`
- 3 trials per criterion · 2026-11-08 21:54

Fill in Target from `criteria.md`, and Run and Verdict from the output
underneath. Whether a trial passed depends on the criterion you wrote.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. my own writing |  |   |   |   |  |
| 2. score spread |  |   |   |   |  |
| 3. label coverage |  |   |   |   |  |
| 4. appeal path |  |   |   |   |  |
| 5. bad input |  |   |   |   |  |

---

## What actually came back

Real output. Paste the relevant parts into your README — the rubric
asks for the actual JSON, not a description of it.

### my own writing

**Trial 1**

```json
[
  {
    "status": 200,
    "elapsed_s": 0.065,
    "content_id": "5f3addf2-1bc0-4332-a817-432d8f9c6f6f",
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
    "content_id": "44b230c6-5d31-4fdb-abb4-142782b6cd46",
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
    "elapsed_s": 0.053,
    "content_id": "981650ec-7906-49f5-ae6d-d0d28a282d75",
    "guess": "unsure",
    "confidence": 0.5067,
    "model_score": 0.5448,
    "style_score": 0.4495,
    "combined_score": 0.5067,
    "label": "We couldn't tell from this piece how it was written, so we're not making a call. A lot of writing by real people lands here, especially very plain or very formal writing. Nothing has been flagged and nothing changes for you. If you'd still like a person to look at it, you can ask for a review.",
    "sent": "Last winter our heater stopped working. It was a Tuesday in January. W… (528 characters)"
  },
  {
    "status": 200,
    "elapsed_s": 0.061,
    "content_id": "e3568160-b3bf-4f6f-a795-a25de7267ce7",
    "guess": "human",
    "confidence": 0.7634,
    "model_score": 0.1587,
    "style_score": 0.3535,
    "combined_score": 0.2366,
    "label": "This reads like it was written by a person. Nothing in it looked machine-generated to us.",
    "sent": "I didn't expect to like the night bus. For the first month I treated i… (613 characters)"
  },
  {
    "status": 200,
    "elapsed_s": 0.058,
    "content_id": "a608a856-727a-4358-978c-0ea376660c2a",
    "guess": "human",
    "confidence": 0.8017,
    "model_score": 0.1602,
    "style_score": 0.2555,
    "combined_score": 0.1983,
    "label": "This reads like it was written by a person. Nothing in it looked machine-generated to us.",
    "sent": "The reading this week argued that standardized tests mostly measure ho… (674 characters)"
  },
  {
    "status": 200,
    "elapsed_s": 0.058,
    "content_id": "410a57ea-4ac3-436c-baa4-2f345f44e276",
    "guess": "human",
    "confidence": 0.8925,
    "model_score": 0.1044,
    "style_score": 0.1121,
    "combined_score": 0.1075,
    "label": "This reads like it was written by a person. Nothing in it looked machine-generated to us.",
    "sent": "Hey! Sorry it took me forever to reply, this week has been a mess. The… (594 characters)"
  },
  {
    "status": 200,
    "elapsed_s": 0.058,
    "content_id": "d9f2bce9-9691-486e-b54b-0c74d7593b0a",
    "guess": "human",
    "confidence": 0.7482,
    "model_score": 0.2585,
    "style_score": 0.2417,
    "combined_score": 0.2518,
    "label": "This reads like it was written by a person. Nothing in it looked machine-generated to us.",
    "sent": "My grandmother never measured anything. When I asked her for the recip… (586 characters)"
  },
  {
    "status": 200,
    "elapsed_s": 0.063,
    "content_id": "34d34e53-6a6e-47c1-a117-3a4f27a66e58",
    "guess": "human",
    "confidence": 0.6994,
    "model_score": 0.3978,
    "style_score": 0.1549,
    "combined_score": 0.3006,
    "label": "This reads like it was written by a person. Nothing in it looked machine-generated to us.",
    "sent": "I started running in March because a doctor told me my blood pressure … (631 characters)"
  },
  {
    "status": 200,
    "elapsed_s": 0.061,
    "content_id": "6da8d62e-d5bc-42e3-8162-ae518d665c91",
    "guess": "human",
    "confidence": 0.7102,
    "model_score": 0.253,
    "style_score": 0.3449,
    "combined_score": 0.2898,
    "label": "This reads like it was written by a person. Nothing in it looked machine-generated to us.",
    "sent": "Everyone in my family has a different theory about why my uncle's phon… (632 characters)"
  },
  {
    "status": 200,
    "elapsed_s": 0.065,
    "content_id": "c1758142-17e6-4b58-b997-26f9b4e3a77c",
    "guess": "human",
    "confidence": 0.6013,
    "model_score": 0.4759,
    "style_score": 0.283,
    "combined_score": 0.3987,
    "label": "This reads like it was written by a person. Nothing in it looked machine-generated to us.",
    "sent": "The worst interview I've had was for a job at a bookshop, and I didn't… (645 characters)"
  }
]
```

**Trial 2**

```json
[
  {
    "status": 200,
    "elapsed_s": 0.057,
    "content_id": "17344ff5-7f2a-446c-9122-d9d9ffcf83ff",
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
    "elapsed_s": 0.057,
    "content_id": "637f1ddb-7bb0-4ddf-9d85-98d54b0475fe",
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
    "elapsed_s": 0.052,
    "content_id": "98ebc4a8-961e-4c5a-b385-083c48251cc9",
    "guess": "unsure",
    "confidence": 0.5067,
    "model_score": 0.5448,
    "style_score": 0.4495,
    "combined_score": 0.5067,
    "label": "We couldn't tell from this piece how it was written, so we're not making a call. A lot of writing by real people lands here, especially very plain or very formal writing. Nothing has been flagged and nothing changes for you. If you'd still like a person to look at it, you can ask for a review.",
    "sent": "Last winter our heater stopped working. It was a Tuesday in January. W… (528 characters)"
  },
  {
    "status": 200,
    "elapsed_s": 0.058,
    "content_id": "b9b47daa-9ba7-404a-b46c-3916750f59d9",
    "guess": "human",
    "confidence": 0.7634,
    "model_score": 0.1587,
    "style_score": 0.3535,
    "combined_score": 0.2366,
    "label": "This reads like it was written by a person. Nothing in it looked machine-generated to us.",
    "sent": "I didn't expect to like the night bus. For the first month I treated i… (613 characters)"
  },
  {
    "status": 200,
    "elapsed_s": 0.058,
    "content_id": "6b3d1251-099f-4898-9774-7cd0962bc706",
    "guess": "human",
    "confidence": 0.8017,
    "model_score": 0.1602,
    "style_score": 0.2555,
    "combined_score": 0.1983,
    "label": "This reads like it was written by a person. Nothing in it looked machine-generated to us.",
    "sent": "The reading this week argued that standardized tests mostly measure ho… (674 characters)"
  },
  {
    "status": 200,
    "elapsed_s": 0.059,
    "content_id": "ee9f4649-9b39-482e-920a-804b634e19a8",
    "guess": "human",
    "confidence": 0.8925,
    "model_score": 0.1044,
    "style_score": 0.1121,
    "combined_score": 0.1075,
    "label": "This reads like it was written by a person. Nothing in it looked machine-generated to us.",
    "sent": "Hey! Sorry it took me forever to reply, this week has been a mess. The… (594 characters)"
  },
  {
    "status": 200,
    "elapsed_s": 0.059,
    "content_id": "5ee4cf17-01b1-4efc-864a-072b536f2d80",
    "guess": "human",
    "confidence": 0.7482,
    "model_score": 0.2585,
    "style_score": 0.2417,
    "combined_score": 0.2518,
    "label": "This reads like it was written by a person. Nothing in it looked machine-generated to us.",
    "sent": "My grandmother never measured anything. When I asked her for the recip… (586 characters)"
  },
  {
    "status": 200,
    "elapsed_s": 0.062,
    "content_id": "c52b1992-afb6-42d3-a85e-5812fc3581dc",
    "guess": "human",
    "confidence": 0.6994,
    "model_score": 0.3978,
    "style_score": 0.1549,
    "combined_score": 0.3006,
    "label": "This reads like it was written by a person. Nothing in it looked machine-generated to us.",
    "sent": "I started running in March because a doctor told me my blood pressure … (631 characters)"
  },
  {
    "status": 200,
    "elapsed_s": 0.061,
    "content_id": "15707226-b871-469c-9497-97773783d1a1",
    "guess": "human",
    "confidence": 0.7102,
    "model_score": 0.253,
    "style_score": 0.3449,
    "combined_score": 0.2898,
    "label": "This reads like it was written by a person. Nothing in it looked machine-generated to us.",
    "sent": "Everyone in my family has a different theory about why my uncle's phon… (632 characters)"
  },
  {
    "status": 200,
    "elapsed_s": 0.062,
    "content_id": "ca70e032-17c7-4436-b297-4dc8ebacd804",
    "guess": "human",
    "confidence": 0.6013,
    "model_score": 0.4759,
    "style_score": 0.283,
    "combined_score": 0.3987,
    "label": "This reads like it was written by a person. Nothing in it looked machine-generated to us.",
    "sent": "The worst interview I've had was for a job at a bookshop, and I didn't… (645 characters)"
  }
]
```

**Trial 3**

```json
[
  {
    "status": 200,
    "elapsed_s": 0.057,
    "content_id": "125e486d-1f3d-4b40-9293-f2870c09aaa0",
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
    "elapsed_s": 0.057,
    "content_id": "92182301-491d-4fc2-bb75-eb05eaa9eeec",
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
    "elapsed_s": 0.052,
    "content_id": "e5c5af2e-4c11-4be2-b148-665cb14779ea",
    "guess": "unsure",
    "confidence": 0.5067,
    "model_score": 0.5448,
    "style_score": 0.4495,
    "combined_score": 0.5067,
    "label": "We couldn't tell from this piece how it was written, so we're not making a call. A lot of writing by real people lands here, especially very plain or very formal writing. Nothing has been flagged and nothing changes for you. If you'd still like a person to look at it, you can ask for a review.",
    "sent": "Last winter our heater stopped working. It was a Tuesday in January. W… (528 characters)"
  },
  {
    "status": 200,
    "elapsed_s": 0.058,
    "content_id": "10184451-772d-4f5f-813d-e2bce07cb250",
    "guess": "human",
    "confidence": 0.7634,
    "model_score": 0.1587,
    "style_score": 0.3535,
    "combined_score": 0.2366,
    "label": "This reads like it was written by a person. Nothing in it looked machine-generated to us.",
    "sent": "I didn't expect to like the night bus. For the first month I treated i… (613 characters)"
  },
  {
    "status": 200,
    "elapsed_s": 0.058,
    "content_id": "8d2eee5f-7b4d-4b9d-8d33-d68622ea134e",
    "guess": "human",
    "confidence": 0.8017,
    "model_score": 0.1602,
    "style_score": 0.2555,
    "combined_score": 0.1983,
    "label": "This reads like it was written by a person. Nothing in it looked machine-generated to us.",
    "sent": "The reading this week argued that standardized tests mostly measure ho… (674 characters)"
  },
  {
    "status": 200,
    "elapsed_s": 0.058,
    "content_id": "e84b5af5-5ab1-41c9-a1d9-0d1dbe6a24c7",
    "guess": "human",
    "confidence": 0.8925,
    "model_score": 0.1044,
    "style_score": 0.1121,
    "combined_score": 0.1075,
    "label": "This reads like it was written by a person. Nothing in it looked machine-generated to us.",
    "sent": "Hey! Sorry it took me forever to reply, this week has been a mess. The… (594 characters)"
  },
  {
    "status": 200,
    "elapsed_s": 0.058,
    "content_id": "814c6458-1970-46e1-878f-db45b929b0f5",
    "guess": "human",
    "confidence": 0.7482,
    "model_score": 0.2585,
    "style_score": 0.2417,
    "combined_score": 0.2518,
    "label": "This reads like it was written by a person. Nothing in it looked machine-generated to us.",
    "sent": "My grandmother never measured anything. When I asked her for the recip… (586 characters)"
  },
  {
    "status": 200,
    "elapsed_s": 0.061,
    "content_id": "9f516dd7-32bf-445c-913e-9b6229205e52",
    "guess": "human",
    "confidence": 0.6994,
    "model_score": 0.3978,
    "style_score": 0.1549,
    "combined_score": 0.3006,
    "label": "This reads like it was written by a person. Nothing in it looked machine-generated to us.",
    "sent": "I started running in March because a doctor told me my blood pressure … (631 characters)"
  },
  {
    "status": 200,
    "elapsed_s": 0.064,
    "content_id": "48d9f49e-6ba3-4ce1-becc-a68f507ac8c3",
    "guess": "human",
    "confidence": 0.7102,
    "model_score": 0.253,
    "style_score": 0.3449,
    "combined_score": 0.2898,
    "label": "This reads like it was written by a person. Nothing in it looked machine-generated to us.",
    "sent": "Everyone in my family has a different theory about why my uncle's phon… (632 characters)"
  },
  {
    "status": 200,
    "elapsed_s": 0.062,
    "content_id": "49808b17-8de8-48e6-90bd-e7962f219a0a",
    "guess": "human",
    "confidence": 0.6013,
    "model_score": 0.4759,
    "style_score": 0.283,
    "combined_score": 0.3987,
    "label": "This reads like it was written by a person. Nothing in it looked machine-generated to us.",
    "sent": "The worst interview I've had was for a job at a bookshop, and I didn't… (645 characters)"
  }
]
```

### score spread

**Trial 1**

```json
[
  {
    "status": 200,
    "elapsed_s": 0.053,
    "content_id": "0c4f0ba9-e887-4113-bc4a-2291df0eb7e4",
    "guess": "ai",
    "confidence": 0.7523,
    "model_score": 0.7205,
    "style_score": 0.8,
    "combined_score": 0.7523,
    "label": "This looks like it was probably written with an AI tool. That's our best guess, not a finding about you, and it can be wrong. If you wrote this yourself, ask for a review and a person will look at it.",
    "sent": "Effective time management is an essential skill for success in both pe… (707 characters)"
  },
  {
    "status": 200,
    "elapsed_s": 0.052,
    "content_id": "9b21d623-4af5-453a-909c-5796ba28f251",
    "guess": "ai",
    "confidence": 0.7535,
    "model_score": 0.7738,
    "style_score": 0.7231,
    "combined_score": 0.7535,
    "label": "This looks like it was probably written with an AI tool. That's our best guess, not a finding about you, and it can be wrong. If you wrote this yourself, ask for a review and a person will look at it.",
    "sent": "Sleep plays a crucial role in maintaining overall health and well-bein… (682 characters)"
  },
  {
    "status": 200,
    "elapsed_s": 0.053,
    "content_id": "c8fe9ddc-2758-4dbe-a515-dcf45ad94b88",
    "guess": "unsure",
    "confidence": 0.7102,
    "model_score": 0.6504,
    "style_score": 0.8,
    "combined_score": 0.7102,
    "label": "We couldn't tell from this piece how it was written, so we're not making a call. A lot of writing by real people lands here, especially very plain or very formal writing. Nothing has been flagged and nothing changes for you. If you'd still like a person to look at it, you can ask for a review.",
    "sent": "Learning a new language offers a wide range of cognitive, social, and … (751 characters)"
  },
  {
    "status": 200,
    "elapsed_s": 0.059,
    "content_id": "06db48ae-efcb-43fa-97a0-bdf2c4d6afd7",
    "guess": "ai",
    "confidence": 0.8941,
    "model_score": 0.9549,
    "style_score": 0.8029,
    "combined_score": 0.8941,
    "label": "This looks like it was probably written with an AI tool. That's our best guess, not a finding about you, and it can be wrong. If you wrote this yourself, ask for a review and a person will look at it.",
    "sent": "Renewable energy sources, such as solar, wind, and hydroelectric power… (729 characters)"
  },
  {
    "status": 200,
    "elapsed_s": 0.053,
    "content_id": "989c058b-3ed6-4d86-a590-bb950e47a2e7",
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
    "elapsed_s": 0.059,
    "content_id": "fceb0ed1-8c0f-4754-8cbe-5046bd9208ab",
    "guess": "human",
    "confidence": 0.7634,
    "model_score": 0.1587,
    "style_score": 0.3535,
    "combined_score": 0.2366,
    "label": "This reads like it was written by a person. Nothing in it looked machine-generated to us.",
    "sent": "I didn't expect to like the night bus. For the first month I treated i… (613 characters)"
  },
  {
    "status": 200,
    "elapsed_s": 0.058,
    "content_id": "7b784ae7-552a-4f46-9f47-e84a57b242f7",
    "guess": "human",
    "confidence": 0.8017,
    "model_score": 0.1602,
    "style_score": 0.2555,
    "combined_score": 0.1983,
    "label": "This reads like it was written by a person. Nothing in it looked machine-generated to us.",
    "sent": "The reading this week argued that standardized tests mostly measure ho… (674 characters)"
  },
  {
    "status": 200,
    "elapsed_s": 0.061,
    "content_id": "b3597fed-5b8d-4e58-8ca9-cad07fb2e525",
    "guess": "unsure",
    "confidence": 0.5287,
    "model_score": 0.2411,
    "style_score": 0.8167,
    "combined_score": 0.4713,
    "label": "We couldn't tell from this piece how it was written, so we're not making a call. A lot of writing by real people lands here, especially very plain or very formal writing. Nothing has been flagged and nothing changes for you. If you'd still like a person to look at it, you can ask for a review.",
    "sent": "One of the pleasantest things in the world is going a journey; but I l… (605 characters)"
  },
  {
    "status": 200,
    "elapsed_s": 0.102,
    "content_id": "6c692f88-f75f-4284-9e1b-5528fe410875",
    "guess": "human",
    "confidence": 0.6727,
    "model_score": 0.3741,
    "style_score": 0.2571,
    "combined_score": 0.3273,
    "label": "This reads like it was written by a person. Nothing in it looked machine-generated to us.",
    "sent": "Now, this is a subject on which I flatter myself I really am au fait. … (1,221 characters)"
  },
  {
    "status": 200,
    "elapsed_s": 0.094,
    "content_id": "d8e9e109-8d62-461b-9b12-0e6a26dfe45e",
    "guess": "human",
    "confidence": 0.7848,
    "model_score": 0.0751,
    "style_score": 0.4254,
    "combined_score": 0.2152,
    "label": "This reads like it was written by a person. Nothing in it looked machine-generated to us.",
    "sent": "Just now, when every one is bound, under pain of a decree in absence c… (1,158 characters)"
  }
]
```

**Trial 2**

```json
[
  {
    "status": 200,
    "elapsed_s": 0.053,
    "content_id": "3e77d588-0c42-499d-af85-96bb9e843579",
    "guess": "ai",
    "confidence": 0.7523,
    "model_score": 0.7205,
    "style_score": 0.8,
    "combined_score": 0.7523,
    "label": "This looks like it was probably written with an AI tool. That's our best guess, not a finding about you, and it can be wrong. If you wrote this yourself, ask for a review and a person will look at it.",
    "sent": "Effective time management is an essential skill for success in both pe… (707 characters)"
  },
  {
    "status": 200,
    "elapsed_s": 0.053,
    "content_id": "211c0de4-134d-4418-b332-e0c8ab91465e",
    "guess": "ai",
    "confidence": 0.7535,
    "model_score": 0.7738,
    "style_score": 0.7231,
    "combined_score": 0.7535,
    "label": "This looks like it was probably written with an AI tool. That's our best guess, not a finding about you, and it can be wrong. If you wrote this yourself, ask for a review and a person will look at it.",
    "sent": "Sleep plays a crucial role in maintaining overall health and well-bein… (682 characters)"
  },
  {
    "status": 200,
    "elapsed_s": 0.053,
    "content_id": "2791f57c-130a-4a65-a2e4-973d571b05f9",
    "guess": "unsure",
    "confidence": 0.7102,
    "model_score": 0.6504,
    "style_score": 0.8,
    "combined_score": 0.7102,
    "label": "We couldn't tell from this piece how it was written, so we're not making a call. A lot of writing by real people lands here, especially very plain or very formal writing. Nothing has been flagged and nothing changes for you. If you'd still like a person to look at it, you can ask for a review.",
    "sent": "Learning a new language offers a wide range of cognitive, social, and … (751 characters)"
  },
  {
    "status": 200,
    "elapsed_s": 0.057,
    "content_id": "94e3e234-a934-47fe-bdf8-a7ba8b9ce6c0",
    "guess": "ai",
    "confidence": 0.8941,
    "model_score": 0.9549,
    "style_score": 0.8029,
    "combined_score": 0.8941,
    "label": "This looks like it was probably written with an AI tool. That's our best guess, not a finding about you, and it can be wrong. If you wrote this yourself, ask for a review and a person will look at it.",
    "sent": "Renewable energy sources, such as solar, wind, and hydroelectric power… (729 characters)"
  },
  {
    "status": 200,
    "elapsed_s": 0.053,
    "content_id": "caa54741-3881-4e6c-a4e9-b20ab7e5a28e",
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
    "elapsed_s": 0.059,
    "content_id": "bb273952-57cb-4a3b-b257-f5dfb179787f",
    "guess": "human",
    "confidence": 0.7634,
    "model_score": 0.1587,
    "style_score": 0.3535,
    "combined_score": 0.2366,
    "label": "This reads like it was written by a person. Nothing in it looked machine-generated to us.",
    "sent": "I didn't expect to like the night bus. For the first month I treated i… (613 characters)"
  },
  {
    "status": 200,
    "elapsed_s": 0.058,
    "content_id": "d136ef3c-bd9a-4b77-8fdb-aa262534c092",
    "guess": "human",
    "confidence": 0.8017,
    "model_score": 0.1602,
    "style_score": 0.2555,
    "combined_score": 0.1983,
    "label": "This reads like it was written by a person. Nothing in it looked machine-generated to us.",
    "sent": "The reading this week argued that standardized tests mostly measure ho… (674 characters)"
  },
  {
    "status": 200,
    "elapsed_s": 0.061,
    "content_id": "9c8a9273-4c2c-4490-aae3-38cfb230b4e4",
    "guess": "unsure",
    "confidence": 0.5287,
    "model_score": 0.2411,
    "style_score": 0.8167,
    "combined_score": 0.4713,
    "label": "We couldn't tell from this piece how it was written, so we're not making a call. A lot of writing by real people lands here, especially very plain or very formal writing. Nothing has been flagged and nothing changes for you. If you'd still like a person to look at it, you can ask for a review.",
    "sent": "One of the pleasantest things in the world is going a journey; but I l… (605 characters)"
  },
  {
    "status": 200,
    "elapsed_s": 0.107,
    "content_id": "3585def9-31e8-47b5-8506-7eb418644400",
    "guess": "human",
    "confidence": 0.6727,
    "model_score": 0.3741,
    "style_score": 0.2571,
    "combined_score": 0.3273,
    "label": "This reads like it was written by a person. Nothing in it looked machine-generated to us.",
    "sent": "Now, this is a subject on which I flatter myself I really am au fait. … (1,221 characters)"
  },
  {
    "status": 200,
    "elapsed_s": 0.12,
    "content_id": "8c1fad24-0f10-4f50-a8f9-2b1349e622ac",
    "guess": "human",
    "confidence": 0.7848,
    "model_score": 0.0751,
    "style_score": 0.4254,
    "combined_score": 0.2152,
    "label": "This reads like it was written by a person. Nothing in it looked machine-generated to us.",
    "sent": "Just now, when every one is bound, under pain of a decree in absence c… (1,158 characters)"
  }
]
```

**Trial 3**

```json
[
  {
    "status": 200,
    "elapsed_s": 0.063,
    "content_id": "ac1eef93-f88a-4cf0-8b17-038dff601f3d",
    "guess": "ai",
    "confidence": 0.7523,
    "model_score": 0.7205,
    "style_score": 0.8,
    "combined_score": 0.7523,
    "label": "This looks like it was probably written with an AI tool. That's our best guess, not a finding about you, and it can be wrong. If you wrote this yourself, ask for a review and a person will look at it.",
    "sent": "Effective time management is an essential skill for success in both pe… (707 characters)"
  },
  {
    "status": 200,
    "elapsed_s": 0.061,
    "content_id": "ea1dac41-6a35-4c8d-a62e-2ec20d61ea12",
    "guess": "ai",
    "confidence": 0.7535,
    "model_score": 0.7738,
    "style_score": 0.7231,
    "combined_score": 0.7535,
    "label": "This looks like it was probably written with an AI tool. That's our best guess, not a finding about you, and it can be wrong. If you wrote this yourself, ask for a review and a person will look at it.",
    "sent": "Sleep plays a crucial role in maintaining overall health and well-bein… (682 characters)"
  },
  {
    "status": 200,
    "elapsed_s": 0.062,
    "content_id": "725d69b4-2dee-4f18-9959-4aec3d1001fc",
    "guess": "unsure",
    "confidence": 0.7102,
    "model_score": 0.6504,
    "style_score": 0.8,
    "combined_score": 0.7102,
    "label": "We couldn't tell from this piece how it was written, so we're not making a call. A lot of writing by real people lands here, especially very plain or very formal writing. Nothing has been flagged and nothing changes for you. If you'd still like a person to look at it, you can ask for a review.",
    "sent": "Learning a new language offers a wide range of cognitive, social, and … (751 characters)"
  },
  {
    "status": 200,
    "elapsed_s": 0.066,
    "content_id": "f33a3be3-0519-4c27-8054-7129ae330133",
    "guess": "ai",
    "confidence": 0.8941,
    "model_score": 0.9549,
    "style_score": 0.8029,
    "combined_score": 0.8941,
    "label": "This looks like it was probably written with an AI tool. That's our best guess, not a finding about you, and it can be wrong. If you wrote this yourself, ask for a review and a person will look at it.",
    "sent": "Renewable energy sources, such as solar, wind, and hydroelectric power… (729 characters)"
  },
  {
    "status": 200,
    "elapsed_s": 0.067,
    "content_id": "cca1b3a3-3f3e-41c2-b70a-88a8796c7715",
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
    "elapsed_s": 0.067,
    "content_id": "8498f8c9-3216-497e-bd4b-0a2491ce725e",
    "guess": "human",
    "confidence": 0.7634,
    "model_score": 0.1587,
    "style_score": 0.3535,
    "combined_score": 0.2366,
    "label": "This reads like it was written by a person. Nothing in it looked machine-generated to us.",
    "sent": "I didn't expect to like the night bus. For the first month I treated i… (613 characters)"
  },
  {
    "status": 200,
    "elapsed_s": 0.066,
    "content_id": "a128f000-0ad5-4687-a76c-46b2ba0ee3d9",
    "guess": "human",
    "confidence": 0.8017,
    "model_score": 0.1602,
    "style_score": 0.2555,
    "combined_score": 0.1983,
    "label": "This reads like it was written by a person. Nothing in it looked machine-generated to us.",
    "sent": "The reading this week argued that standardized tests mostly measure ho… (674 characters)"
  },
  {
    "status": 200,
    "elapsed_s": 0.07,
    "content_id": "73448848-b231-472c-ad3d-ce023e732322",
    "guess": "unsure",
    "confidence": 0.5287,
    "model_score": 0.2411,
    "style_score": 0.8167,
    "combined_score": 0.4713,
    "label": "We couldn't tell from this piece how it was written, so we're not making a call. A lot of writing by real people lands here, especially very plain or very formal writing. Nothing has been flagged and nothing changes for you. If you'd still like a person to look at it, you can ask for a review.",
    "sent": "One of the pleasantest things in the world is going a journey; but I l… (605 characters)"
  },
  {
    "status": 200,
    "elapsed_s": 0.107,
    "content_id": "90e6e363-d2c5-4500-9210-b42476e7401d",
    "guess": "human",
    "confidence": 0.6727,
    "model_score": 0.3741,
    "style_score": 0.2571,
    "combined_score": 0.3273,
    "label": "This reads like it was written by a person. Nothing in it looked machine-generated to us.",
    "sent": "Now, this is a subject on which I flatter myself I really am au fait. … (1,221 characters)"
  },
  {
    "status": 200,
    "elapsed_s": 0.095,
    "content_id": "6efe3b9e-892a-456e-8f62-e660214da0b4",
    "guess": "human",
    "confidence": 0.7848,
    "model_score": 0.0751,
    "style_score": 0.4254,
    "combined_score": 0.2152,
    "label": "This reads like it was written by a person. Nothing in it looked machine-generated to us.",
    "sent": "Just now, when every one is bound, under pain of a decree in absence c… (1,158 characters)"
  }
]
```

### label coverage

**Trial 1**

```json
[
  {
    "status": 200,
    "elapsed_s": 0.052,
    "content_id": "6bc7bd96-5e2a-403d-ba7d-422312c9656e",
    "guess": "ai",
    "confidence": 0.7523,
    "model_score": 0.7205,
    "style_score": 0.8,
    "combined_score": 0.7523,
    "label": "This looks like it was probably written with an AI tool. That's our best guess, not a finding about you, and it can be wrong. If you wrote this yourself, ask for a review and a person will look at it.",
    "sent": "Effective time management is an essential skill for success in both pe… (707 characters)"
  },
  {
    "status": 200,
    "elapsed_s": 0.053,
    "content_id": "c118cba9-ef04-405a-9ac8-1cdc99611407",
    "guess": "ai",
    "confidence": 0.7535,
    "model_score": 0.7738,
    "style_score": 0.7231,
    "combined_score": 0.7535,
    "label": "This looks like it was probably written with an AI tool. That's our best guess, not a finding about you, and it can be wrong. If you wrote this yourself, ask for a review and a person will look at it.",
    "sent": "Sleep plays a crucial role in maintaining overall health and well-bein… (682 characters)"
  },
  {
    "status": 200,
    "elapsed_s": 0.053,
    "content_id": "de294dc5-01fe-40fc-b94f-7ecb3cdea294",
    "guess": "unsure",
    "confidence": 0.7102,
    "model_score": 0.6504,
    "style_score": 0.8,
    "combined_score": 0.7102,
    "label": "We couldn't tell from this piece how it was written, so we're not making a call. A lot of writing by real people lands here, especially very plain or very formal writing. Nothing has been flagged and nothing changes for you. If you'd still like a person to look at it, you can ask for a review.",
    "sent": "Learning a new language offers a wide range of cognitive, social, and … (751 characters)"
  },
  {
    "status": 200,
    "elapsed_s": 0.063,
    "content_id": "a5535bc0-0e2a-4dac-ba73-068032357464",
    "guess": "unsure",
    "confidence": 0.5287,
    "model_score": 0.2411,
    "style_score": 0.8167,
    "combined_score": 0.4713,
    "label": "We couldn't tell from this piece how it was written, so we're not making a call. A lot of writing by real people lands here, especially very plain or very formal writing. Nothing has been flagged and nothing changes for you. If you'd still like a person to look at it, you can ask for a review.",
    "sent": "One of the pleasantest things in the world is going a journey; but I l… (605 characters)"
  },
  {
    "status": 200,
    "elapsed_s": 0.097,
    "content_id": "cac82f1d-6082-433c-8c01-09386520bd2b",
    "guess": "human",
    "confidence": 0.6727,
    "model_score": 0.3741,
    "style_score": 0.2571,
    "combined_score": 0.3273,
    "label": "This reads like it was written by a person. Nothing in it looked machine-generated to us.",
    "sent": "Now, this is a subject on which I flatter myself I really am au fait. … (1,221 characters)"
  },
  {
    "status": 200,
    "elapsed_s": 0.094,
    "content_id": "4ed80f14-35d2-4cd3-a45f-8cc015a0714c",
    "guess": "human",
    "confidence": 0.7848,
    "model_score": 0.0751,
    "style_score": 0.4254,
    "combined_score": 0.2152,
    "label": "This reads like it was written by a person. Nothing in it looked machine-generated to us.",
    "sent": "Just now, when every one is bound, under pain of a decree in absence c… (1,158 characters)"
  },
  {
    "status": 200,
    "elapsed_s": 0.063,
    "content_id": "223ee7fb-2d69-42fa-b317-dd0163d2dbce",
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
    "content_id": "64a3e181-2ff6-4ada-8dbd-af1383643695",
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
    "content_id": "2fbebaa5-6c7f-4373-a974-d7ccebd547f3",
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

**Trial 2**

```json
[
  {
    "status": 200,
    "elapsed_s": 0.052,
    "content_id": "0ee22396-a2de-4b72-bcf4-c191a3d0b130",
    "guess": "ai",
    "confidence": 0.7523,
    "model_score": 0.7205,
    "style_score": 0.8,
    "combined_score": 0.7523,
    "label": "This looks like it was probably written with an AI tool. That's our best guess, not a finding about you, and it can be wrong. If you wrote this yourself, ask for a review and a person will look at it.",
    "sent": "Effective time management is an essential skill for success in both pe… (707 characters)"
  },
  {
    "status": 200,
    "elapsed_s": 0.053,
    "content_id": "ff2b7c1a-e92b-46ab-b318-2752b6b3060d",
    "guess": "ai",
    "confidence": 0.7535,
    "model_score": 0.7738,
    "style_score": 0.7231,
    "combined_score": 0.7535,
    "label": "This looks like it was probably written with an AI tool. That's our best guess, not a finding about you, and it can be wrong. If you wrote this yourself, ask for a review and a person will look at it.",
    "sent": "Sleep plays a crucial role in maintaining overall health and well-bein… (682 characters)"
  },
  {
    "status": 200,
    "elapsed_s": 0.075,
    "content_id": "d3b3d0fa-2a1c-40dc-838d-eb2c86fa857f",
    "guess": "unsure",
    "confidence": 0.7102,
    "model_score": 0.6504,
    "style_score": 0.8,
    "combined_score": 0.7102,
    "label": "We couldn't tell from this piece how it was written, so we're not making a call. A lot of writing by real people lands here, especially very plain or very formal writing. Nothing has been flagged and nothing changes for you. If you'd still like a person to look at it, you can ask for a review.",
    "sent": "Learning a new language offers a wide range of cognitive, social, and … (751 characters)"
  },
  {
    "status": 200,
    "elapsed_s": 0.061,
    "content_id": "2333e236-675b-4086-a228-34f85681d304",
    "guess": "unsure",
    "confidence": 0.5287,
    "model_score": 0.2411,
    "style_score": 0.8167,
    "combined_score": 0.4713,
    "label": "We couldn't tell from this piece how it was written, so we're not making a call. A lot of writing by real people lands here, especially very plain or very formal writing. Nothing has been flagged and nothing changes for you. If you'd still like a person to look at it, you can ask for a review.",
    "sent": "One of the pleasantest things in the world is going a journey; but I l… (605 characters)"
  },
  {
    "status": 200,
    "elapsed_s": 0.098,
    "content_id": "7adebd8f-e2d9-4578-93cf-80858868d4c2",
    "guess": "human",
    "confidence": 0.6727,
    "model_score": 0.3741,
    "style_score": 0.2571,
    "combined_score": 0.3273,
    "label": "This reads like it was written by a person. Nothing in it looked machine-generated to us.",
    "sent": "Now, this is a subject on which I flatter myself I really am au fait. … (1,221 characters)"
  },
  {
    "status": 200,
    "elapsed_s": 0.099,
    "content_id": "fb724cde-9e79-4f66-829a-3e0fe32d9194",
    "guess": "human",
    "confidence": 0.7848,
    "model_score": 0.0751,
    "style_score": 0.4254,
    "combined_score": 0.2152,
    "label": "This reads like it was written by a person. Nothing in it looked machine-generated to us.",
    "sent": "Just now, when every one is bound, under pain of a decree in absence c… (1,158 characters)"
  },
  {
    "status": 200,
    "elapsed_s": 0.067,
    "content_id": "590e257c-023e-4571-96f0-76f2e60ddae3",
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
    "elapsed_s": 0.07,
    "content_id": "c49a3fe8-224f-4089-84b9-b9464c789e2d",
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
    "elapsed_s": 0.062,
    "content_id": "9da39487-21db-4572-87f7-af3e348c579c",
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

**Trial 3**

```json
[
  {
    "status": 200,
    "elapsed_s": 0.064,
    "content_id": "c001292c-07ac-42f9-9d65-e527ce7d7c56",
    "guess": "ai",
    "confidence": 0.7523,
    "model_score": 0.7205,
    "style_score": 0.8,
    "combined_score": 0.7523,
    "label": "This looks like it was probably written with an AI tool. That's our best guess, not a finding about you, and it can be wrong. If you wrote this yourself, ask for a review and a person will look at it.",
    "sent": "Effective time management is an essential skill for success in both pe… (707 characters)"
  },
  {
    "status": 200,
    "elapsed_s": 0.057,
    "content_id": "ea3cbc3d-6828-4c35-99d3-d22bc07973db",
    "guess": "ai",
    "confidence": 0.7535,
    "model_score": 0.7738,
    "style_score": 0.7231,
    "combined_score": 0.7535,
    "label": "This looks like it was probably written with an AI tool. That's our best guess, not a finding about you, and it can be wrong. If you wrote this yourself, ask for a review and a person will look at it.",
    "sent": "Sleep plays a crucial role in maintaining overall health and well-bein… (682 characters)"
  },
  {
    "status": 200,
    "elapsed_s": 0.053,
    "content_id": "f71f9a67-4668-48a9-90e2-404e1b76a532",
    "guess": "unsure",
    "confidence": 0.7102,
    "model_score": 0.6504,
    "style_score": 0.8,
    "combined_score": 0.7102,
    "label": "We couldn't tell from this piece how it was written, so we're not making a call. A lot of writing by real people lands here, especially very plain or very formal writing. Nothing has been flagged and nothing changes for you. If you'd still like a person to look at it, you can ask for a review.",
    "sent": "Learning a new language offers a wide range of cognitive, social, and … (751 characters)"
  },
  {
    "status": 200,
    "elapsed_s": 0.063,
    "content_id": "962d31da-64f8-4fff-9e6a-b44ddd6de440",
    "guess": "unsure",
    "confidence": 0.5287,
    "model_score": 0.2411,
    "style_score": 0.8167,
    "combined_score": 0.4713,
    "label": "We couldn't tell from this piece how it was written, so we're not making a call. A lot of writing by real people lands here, especially very plain or very formal writing. Nothing has been flagged and nothing changes for you. If you'd still like a person to look at it, you can ask for a review.",
    "sent": "One of the pleasantest things in the world is going a journey; but I l… (605 characters)"
  },
  {
    "status": 200,
    "elapsed_s": 0.097,
    "content_id": "9e29fbf3-3535-4734-a26f-a0e1e71b5339",
    "guess": "human",
    "confidence": 0.6727,
    "model_score": 0.3741,
    "style_score": 0.2571,
    "combined_score": 0.3273,
    "label": "This reads like it was written by a person. Nothing in it looked machine-generated to us.",
    "sent": "Now, this is a subject on which I flatter myself I really am au fait. … (1,221 characters)"
  },
  {
    "status": 200,
    "elapsed_s": 0.093,
    "content_id": "c9cf7104-ee73-4e3c-b0dc-7d0eed8d444b",
    "guess": "human",
    "confidence": 0.7848,
    "model_score": 0.0751,
    "style_score": 0.4254,
    "combined_score": 0.2152,
    "label": "This reads like it was written by a person. Nothing in it looked machine-generated to us.",
    "sent": "Just now, when every one is bound, under pain of a decree in absence c… (1,158 characters)"
  },
  {
    "status": 200,
    "elapsed_s": 0.062,
    "content_id": "949ff6bf-d5e5-4d8b-bd75-0f6da0f63a1e",
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
    "elapsed_s": 0.061,
    "content_id": "b34c9a71-0331-439e-80ee-6debb4419fcc",
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
    "content_id": "cf11c073-5238-463b-b7fc-8f7b840b5a13",
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

### appeal path

**Trial 1**

```json
[
  {
    "sent": "submit as eval_appeal_1, then appeal its content_id",
    "submit_status": 200,
    "submit_guess": "ai",
    "content_id": "acc090cc-c61c-4a27-b4c7-dbf61c5c7b93",
    "status": 200,
    "response_status": "under_review",
    "appeal_entries": 1,
    "reasoning_word_for_word": true,
    "creator_copied": true,
    "decision_unchanged": true,
    "appeal_entry": {
      "combined_score": 0.7523,
      "content_id": "acc090cc-c61c-4a27-b4c7-dbf61c5c7b93",
      "creator_id": "eval_appeal_1",
      "decided_at": "2026-11-09T02:54:57+00:00",
      "event": "appeal",
      "guess": "ai",
      "label": "This looks like it was probably written with an AI tool. That's our best guess, not a finding about you, and it can be wrong. If you wrote this yourself, ask for a review and a person will look at it.",
      "model_score": 0.7205,
      "reasoning": "I wrote every word of this myself — it's from my notebook, the part about my grandmother's café. I'd like a person to read it again, please.",
      "status": "under_review",
      "style_score": 0.8,
      "timestamp": "2026-11-09T02:54:57+00:00"
    }
  },
  {
    "sent": "submit as eval_appeal_2, then appeal its content_id",
    "submit_status": 200,
    "submit_guess": "ai",
    "content_id": "d31ff468-317a-4fc8-940d-a7762b737286",
    "status": 200,
    "response_status": "under_review",
    "appeal_entries": 1,
    "reasoning_word_for_word": true,
    "creator_copied": true,
    "decision_unchanged": true,
    "appeal_entry": {
      "combined_score": 0.7535,
      "content_id": "d31ff468-317a-4fc8-940d-a7762b737286",
      "creator_id": "eval_appeal_2",
      "decided_at": "2026-11-09T02:54:57+00:00",
      "event": "appeal",
      "guess": "ai",
      "label": "This looks like it was probably written with an AI tool. That's our best guess, not a finding about you, and it can be wrong. If you wrote this yourself, ask for a review and a person will look at it.",
      "model_score": 0.7738,
      "reasoning": "I wrote every word of this myself — it's from my notebook, the part about my grandmother's café. I'd like a person to read it again, please.",
      "status": "under_review",
      "style_score": 0.7231,
      "timestamp": "2026-11-09T02:54:57+00:00"
    }
  },
  {
    "sent": "submit as eval_appeal_3, then appeal its content_id",
    "submit_status": 200,
    "submit_guess": "unsure",
    "content_id": "c7a16fca-1be3-49b4-856c-d22193020668",
    "status": 200,
    "response_status": "under_review",
    "appeal_entries": 1,
    "reasoning_word_for_word": true,
    "creator_copied": true,
    "decision_unchanged": true,
    "appeal_entry": {
      "combined_score": 0.7102,
      "content_id": "c7a16fca-1be3-49b4-856c-d22193020668",
      "creator_id": "eval_appeal_3",
      "decided_at": "2026-11-09T02:54:57+00:00",
      "event": "appeal",
      "guess": "unsure",
      "label": "We couldn't tell from this piece how it was written, so we're not making a call. A lot of writing by real people lands here, especially very plain or very formal writing. Nothing has been flagged and nothing changes for you. If you'd still like a person to look at it, you can ask for a review.",
      "model_score": 0.6504,
      "reasoning": "I wrote every word of this myself — it's from my notebook, the part about my grandmother's café. I'd like a person to read it again, please.",
      "status": "under_review",
      "style_score": 0.8,
      "timestamp": "2026-11-09T02:54:57+00:00"
    }
  },
  {
    "sent": "submit as eval_appeal_4, then appeal its content_id",
    "submit_status": 200,
    "submit_guess": "ai",
    "content_id": "22598511-a0f0-4857-a7b1-1eda5f8d711f",
    "status": 200,
    "response_status": "under_review",
    "appeal_entries": 1,
    "reasoning_word_for_word": true,
    "creator_copied": true,
    "decision_unchanged": true,
    "appeal_entry": {
      "combined_score": 0.8941,
      "content_id": "22598511-a0f0-4857-a7b1-1eda5f8d711f",
      "creator_id": "eval_appeal_4",
      "decided_at": "2026-11-09T02:54:57+00:00",
      "event": "appeal",
      "guess": "ai",
      "label": "This looks like it was probably written with an AI tool. That's our best guess, not a finding about you, and it can be wrong. If you wrote this yourself, ask for a review and a person will look at it.",
      "model_score": 0.9549,
      "reasoning": "I wrote every word of this myself — it's from my notebook, the part about my grandmother's café. I'd like a person to read it again, please.",
      "status": "under_review",
      "style_score": 0.8029,
      "timestamp": "2026-11-09T02:54:57+00:00"
    }
  },
  {
    "sent": "submit as eval_appeal_5, then appeal its content_id",
    "submit_status": 200,
    "submit_guess": "unsure",
    "content_id": "4c4434f7-a4f3-4cff-bf5d-8c058647284c",
    "status": 200,
    "response_status": "under_review",
    "appeal_entries": 1,
    "reasoning_word_for_word": true,
    "creator_copied": true,
    "decision_unchanged": true,
    "appeal_entry": {
      "combined_score": 0.4649,
      "content_id": "4c4434f7-a4f3-4cff-bf5d-8c058647284c",
      "creator_id": "eval_appeal_5",
      "decided_at": "2026-11-09T02:54:57+00:00",
      "event": "appeal",
      "guess": "unsure",
      "label": "We couldn't tell from this piece how it was written, so we're not making a call. A lot of writing by real people lands here, especially very plain or very formal writing. Nothing has been flagged and nothing changes for you. If you'd still like a person to look at it, you can ask for a review.",
      "model_score": 0.5404,
      "reasoning": "I wrote every word of this myself — it's from my notebook, the part about my grandmother's café. I'd like a person to read it again, please.",
      "status": "under_review",
      "style_score": 0.3516,
      "timestamp": "2026-11-09T02:54:57+00:00"
    }
  },
  {
    "sent": "submit as eval_appeal_6, then appeal its content_id",
    "submit_status": 200,
    "submit_guess": "unsure",
    "content_id": "541b5996-a3cd-4a2f-8034-d2a7dde88dcb",
    "status": 200,
    "response_status": "under_review",
    "appeal_entries": 1,
    "reasoning_word_for_word": true,
    "creator_copied": true,
    "decision_unchanged": true,
    "appeal_entry": {
      "combined_score": 0.4713,
      "content_id": "541b5996-a3cd-4a2f-8034-d2a7dde88dcb",
      "creator_id": "eval_appeal_6",
      "decided_at": "2026-11-09T02:54:57+00:00",
      "event": "appeal",
      "guess": "unsure",
      "label": "We couldn't tell from this piece how it was written, so we're not making a call. A lot of writing by real people lands here, especially very plain or very formal writing. Nothing has been flagged and nothing changes for you. If you'd still like a person to look at it, you can ask for a review.",
      "model_score": 0.2411,
      "reasoning": "I wrote every word of this myself — it's from my notebook, the part about my grandmother's café. I'd like a person to read it again, please.",
      "status": "under_review",
      "style_score": 0.8167,
      "timestamp": "2026-11-09T02:54:57+00:00"
    }
  },
  {
    "sent": "submit as eval_appeal_7, then appeal its content_id",
    "submit_status": 200,
    "submit_guess": "human",
    "content_id": "38b09f74-8f60-457a-baf7-607cd418d0f9",
    "status": 200,
    "response_status": "under_review",
    "appeal_entries": 1,
    "reasoning_word_for_word": true,
    "creator_copied": true,
    "decision_unchanged": true,
    "appeal_entry": {
      "combined_score": 0.3273,
      "content_id": "38b09f74-8f60-457a-baf7-607cd418d0f9",
      "creator_id": "eval_appeal_7",
      "decided_at": "2026-11-09T02:54:58+00:00",
      "event": "appeal",
      "guess": "human",
      "label": "This reads like it was written by a person. Nothing in it looked machine-generated to us.",
      "model_score": 0.3741,
      "reasoning": "I wrote every word of this myself — it's from my notebook, the part about my grandmother's café. I'd like a person to read it again, please.",
      "status": "under_review",
      "style_score": 0.2571,
      "timestamp": "2026-11-09T02:54:58+00:00"
    }
  },
  {
    "sent": "submit as eval_appeal_8, then appeal its content_id",
    "submit_status": 200,
    "submit_guess": "human",
    "content_id": "456b2635-774c-4d2d-9068-11f364bb2778",
    "status": 200,
    "response_status": "under_review",
    "appeal_entries": 1,
    "reasoning_word_for_word": true,
    "creator_copied": true,
    "decision_unchanged": true,
    "appeal_entry": {
      "combined_score": 0.2152,
      "content_id": "456b2635-774c-4d2d-9068-11f364bb2778",
      "creator_id": "eval_appeal_8",
      "decided_at": "2026-11-09T02:54:58+00:00",
      "event": "appeal",
      "guess": "human",
      "label": "This reads like it was written by a person. Nothing in it looked machine-generated to us.",
      "model_score": 0.0751,
      "reasoning": "I wrote every word of this myself — it's from my notebook, the part about my grandmother's café. I'd like a person to read it again, please.",
      "status": "under_review",
      "style_score": 0.4254,
      "timestamp": "2026-11-09T02:54:58+00:00"
    }
  },
  {
    "sent": "submit as eval_appeal_9, then appeal its content_id",
    "submit_status": 200,
    "submit_guess": "unsure",
    "content_id": "eeb30145-f2e6-4037-b2b4-bf593b7483d5",
    "status": 200,
    "response_status": "under_review",
    "appeal_entries": 1,
    "reasoning_word_for_word": true,
    "creator_copied": true,
    "decision_unchanged": true,
    "appeal_entry": {
      "combined_score": 0.5004,
      "content_id": "eeb30145-f2e6-4037-b2b4-bf593b7483d5",
      "creator_id": "eval_appeal_9",
      "decided_at": "2026-11-09T02:54:58+00:00",
      "event": "appeal",
      "guess": "unsure",
      "label": "We couldn't tell from this piece how it was written, so we're not making a call. A lot of writing by real people lands here, especially very plain or very formal writing. Nothing has been flagged and nothing changes for you. If you'd still like a person to look at it, you can ask for a review.",
      "model_score": 0.3144,
      "reasoning": "I wrote every word of this myself — it's from my notebook, the part about my grandmother's café. I'd like a person to read it again, please.",
      "status": "under_review",
      "style_score": 0.7794,
      "timestamp": "2026-11-09T02:54:58+00:00"
    }
  },
  {
    "sent": "submit as eval_appeal_10, then appeal its content_id",
    "submit_status": 200,
    "submit_guess": "unsure",
    "content_id": "1fcda568-22b3-4baf-9033-97bf1e10a3e3",
    "status": 200,
    "response_status": "under_review",
    "appeal_entries": 1,
    "reasoning_word_for_word": true,
    "creator_copied": true,
    "decision_unchanged": true,
    "appeal_entry": {
      "combined_score": 0.5685,
      "content_id": "1fcda568-22b3-4baf-9033-97bf1e10a3e3",
      "creator_id": "eval_appeal_10",
      "decided_at": "2026-11-09T02:54:58+00:00",
      "event": "appeal",
      "guess": "unsure",
      "label": "We couldn't tell from this piece how it was written, so we're not making a call. A lot of writing by real people lands here, especially very plain or very formal writing. Nothing has been flagged and nothing changes for you. If you'd still like a person to look at it, you can ask for a review.",
      "model_score": 0.4229,
      "reasoning": "I wrote every word of this myself — it's from my notebook, the part about my grandmother's café. I'd like a person to read it again, please.",
      "status": "under_review",
      "style_score": 0.7868,
      "timestamp": "2026-11-09T02:54:58+00:00"
    }
  },
  {
    "sent": "appeal against made-up content_id acc090cc-c61c-4a27-b4c7-dbf61c5c7b90",
    "status": 404,
    "error": "unknown_content_id",
    "message": "We couldn't find a submission with id acc090cc-c61c-4a27-b4c7-dbf61c5c7b90. Check it matches the one you were given.",
    "appeal_entries": 0
  },
  {
    "sent": "appeal against made-up content_id b30b69c2-0817-4b1d-a6bb-0e2c6958c78a",
    "status": 404,
    "error": "unknown_content_id",
    "message": "We couldn't find a submission with id b30b69c2-0817-4b1d-a6bb-0e2c6958c78a. Check it matches the one you were given.",
    "appeal_entries": 0
  },
  {
    "sent": "appeal against made-up content_id my-essay-1",
    "status": 404,
    "error": "unknown_content_id",
    "message": "We couldn't find a submission with id my-essay-1. Check it matches the one you were given.",
    "appeal_entries": 0
  }
]
```

**Trial 2**

```json
[
  {
    "sent": "submit as eval_appeal_1, then appeal its content_id",
    "submit_status": 200,
    "submit_guess": "ai",
    "content_id": "ba7cbd61-8697-4ae2-84de-33a5aefe11a5",
    "status": 200,
    "response_status": "under_review",
    "appeal_entries": 1,
    "reasoning_word_for_word": true,
    "creator_copied": true,
    "decision_unchanged": true,
    "appeal_entry": {
      "combined_score": 0.7523,
      "content_id": "ba7cbd61-8697-4ae2-84de-33a5aefe11a5",
      "creator_id": "eval_appeal_1",
      "decided_at": "2026-11-09T02:54:58+00:00",
      "event": "appeal",
      "guess": "ai",
      "label": "This looks like it was probably written with an AI tool. That's our best guess, not a finding about you, and it can be wrong. If you wrote this yourself, ask for a review and a person will look at it.",
      "model_score": 0.7205,
      "reasoning": "I wrote every word of this myself — it's from my notebook, the part about my grandmother's café. I'd like a person to read it again, please.",
      "status": "under_review",
      "style_score": 0.8,
      "timestamp": "2026-11-09T02:54:58+00:00"
    }
  },
  {
    "sent": "submit as eval_appeal_2, then appeal its content_id",
    "submit_status": 200,
    "submit_guess": "ai",
    "content_id": "b497553a-cc79-4d4e-8bf7-1e15f52336af",
    "status": 200,
    "response_status": "under_review",
    "appeal_entries": 1,
    "reasoning_word_for_word": true,
    "creator_copied": true,
    "decision_unchanged": true,
    "appeal_entry": {
      "combined_score": 0.7535,
      "content_id": "b497553a-cc79-4d4e-8bf7-1e15f52336af",
      "creator_id": "eval_appeal_2",
      "decided_at": "2026-11-09T02:54:58+00:00",
      "event": "appeal",
      "guess": "ai",
      "label": "This looks like it was probably written with an AI tool. That's our best guess, not a finding about you, and it can be wrong. If you wrote this yourself, ask for a review and a person will look at it.",
      "model_score": 0.7738,
      "reasoning": "I wrote every word of this myself — it's from my notebook, the part about my grandmother's café. I'd like a person to read it again, please.",
      "status": "under_review",
      "style_score": 0.7231,
      "timestamp": "2026-11-09T02:54:58+00:00"
    }
  },
  {
    "sent": "submit as eval_appeal_3, then appeal its content_id",
    "submit_status": 200,
    "submit_guess": "unsure",
    "content_id": "c4dcffd8-5835-4f6f-ac23-aaae20f8e678",
    "status": 200,
    "response_status": "under_review",
    "appeal_entries": 1,
    "reasoning_word_for_word": true,
    "creator_copied": true,
    "decision_unchanged": true,
    "appeal_entry": {
      "combined_score": 0.7102,
      "content_id": "c4dcffd8-5835-4f6f-ac23-aaae20f8e678",
      "creator_id": "eval_appeal_3",
      "decided_at": "2026-11-09T02:54:58+00:00",
      "event": "appeal",
      "guess": "unsure",
      "label": "We couldn't tell from this piece how it was written, so we're not making a call. A lot of writing by real people lands here, especially very plain or very formal writing. Nothing has been flagged and nothing changes for you. If you'd still like a person to look at it, you can ask for a review.",
      "model_score": 0.6504,
      "reasoning": "I wrote every word of this myself — it's from my notebook, the part about my grandmother's café. I'd like a person to read it again, please.",
      "status": "under_review",
      "style_score": 0.8,
      "timestamp": "2026-11-09T02:54:58+00:00"
    }
  },
  {
    "sent": "submit as eval_appeal_4, then appeal its content_id",
    "submit_status": 200,
    "submit_guess": "ai",
    "content_id": "e1501178-d358-403f-ba56-a23bd4e50365",
    "status": 200,
    "response_status": "under_review",
    "appeal_entries": 1,
    "reasoning_word_for_word": true,
    "creator_copied": true,
    "decision_unchanged": true,
    "appeal_entry": {
      "combined_score": 0.8941,
      "content_id": "e1501178-d358-403f-ba56-a23bd4e50365",
      "creator_id": "eval_appeal_4",
      "decided_at": "2026-11-09T02:54:58+00:00",
      "event": "appeal",
      "guess": "ai",
      "label": "This looks like it was probably written with an AI tool. That's our best guess, not a finding about you, and it can be wrong. If you wrote this yourself, ask for a review and a person will look at it.",
      "model_score": 0.9549,
      "reasoning": "I wrote every word of this myself — it's from my notebook, the part about my grandmother's café. I'd like a person to read it again, please.",
      "status": "under_review",
      "style_score": 0.8029,
      "timestamp": "2026-11-09T02:54:58+00:00"
    }
  },
  {
    "sent": "submit as eval_appeal_5, then appeal its content_id",
    "submit_status": 200,
    "submit_guess": "unsure",
    "content_id": "3e077aa2-e36c-4721-b09a-65af6d19c947",
    "status": 200,
    "response_status": "under_review",
    "appeal_entries": 1,
    "reasoning_word_for_word": true,
    "creator_copied": true,
    "decision_unchanged": true,
    "appeal_entry": {
      "combined_score": 0.4649,
      "content_id": "3e077aa2-e36c-4721-b09a-65af6d19c947",
      "creator_id": "eval_appeal_5",
      "decided_at": "2026-11-09T02:54:58+00:00",
      "event": "appeal",
      "guess": "unsure",
      "label": "We couldn't tell from this piece how it was written, so we're not making a call. A lot of writing by real people lands here, especially very plain or very formal writing. Nothing has been flagged and nothing changes for you. If you'd still like a person to look at it, you can ask for a review.",
      "model_score": 0.5404,
      "reasoning": "I wrote every word of this myself — it's from my notebook, the part about my grandmother's café. I'd like a person to read it again, please.",
      "status": "under_review",
      "style_score": 0.3516,
      "timestamp": "2026-11-09T02:54:58+00:00"
    }
  },
  {
    "sent": "submit as eval_appeal_6, then appeal its content_id",
    "submit_status": 200,
    "submit_guess": "unsure",
    "content_id": "e9c28292-80b5-4be7-8909-0a2d32e49baf",
    "status": 200,
    "response_status": "under_review",
    "appeal_entries": 1,
    "reasoning_word_for_word": true,
    "creator_copied": true,
    "decision_unchanged": true,
    "appeal_entry": {
      "combined_score": 0.4713,
      "content_id": "e9c28292-80b5-4be7-8909-0a2d32e49baf",
      "creator_id": "eval_appeal_6",
      "decided_at": "2026-11-09T02:54:58+00:00",
      "event": "appeal",
      "guess": "unsure",
      "label": "We couldn't tell from this piece how it was written, so we're not making a call. A lot of writing by real people lands here, especially very plain or very formal writing. Nothing has been flagged and nothing changes for you. If you'd still like a person to look at it, you can ask for a review.",
      "model_score": 0.2411,
      "reasoning": "I wrote every word of this myself — it's from my notebook, the part about my grandmother's café. I'd like a person to read it again, please.",
      "status": "under_review",
      "style_score": 0.8167,
      "timestamp": "2026-11-09T02:54:58+00:00"
    }
  },
  {
    "sent": "submit as eval_appeal_7, then appeal its content_id",
    "submit_status": 200,
    "submit_guess": "human",
    "content_id": "f1582a88-15f7-46c1-9f29-da69812f441b",
    "status": 200,
    "response_status": "under_review",
    "appeal_entries": 1,
    "reasoning_word_for_word": true,
    "creator_copied": true,
    "decision_unchanged": true,
    "appeal_entry": {
      "combined_score": 0.3273,
      "content_id": "f1582a88-15f7-46c1-9f29-da69812f441b",
      "creator_id": "eval_appeal_7",
      "decided_at": "2026-11-09T02:54:58+00:00",
      "event": "appeal",
      "guess": "human",
      "label": "This reads like it was written by a person. Nothing in it looked machine-generated to us.",
      "model_score": 0.3741,
      "reasoning": "I wrote every word of this myself — it's from my notebook, the part about my grandmother's café. I'd like a person to read it again, please.",
      "status": "under_review",
      "style_score": 0.2571,
      "timestamp": "2026-11-09T02:54:58+00:00"
    }
  },
  {
    "sent": "submit as eval_appeal_8, then appeal its content_id",
    "submit_status": 200,
    "submit_guess": "human",
    "content_id": "71845df1-e728-4931-80fb-ad6751e6ac4b",
    "status": 200,
    "response_status": "under_review",
    "appeal_entries": 1,
    "reasoning_word_for_word": true,
    "creator_copied": true,
    "decision_unchanged": true,
    "appeal_entry": {
      "combined_score": 0.2152,
      "content_id": "71845df1-e728-4931-80fb-ad6751e6ac4b",
      "creator_id": "eval_appeal_8",
      "decided_at": "2026-11-09T02:54:58+00:00",
      "event": "appeal",
      "guess": "human",
      "label": "This reads like it was written by a person. Nothing in it looked machine-generated to us.",
      "model_score": 0.0751,
      "reasoning": "I wrote every word of this myself — it's from my notebook, the part about my grandmother's café. I'd like a person to read it again, please.",
      "status": "under_review",
      "style_score": 0.4254,
      "timestamp": "2026-11-09T02:54:58+00:00"
    }
  },
  {
    "sent": "submit as eval_appeal_9, then appeal its content_id",
    "submit_status": 200,
    "submit_guess": "unsure",
    "content_id": "4fbcd004-139d-4ee3-9d49-41b0d8842a11",
    "status": 200,
    "response_status": "under_review",
    "appeal_entries": 1,
    "reasoning_word_for_word": true,
    "creator_copied": true,
    "decision_unchanged": true,
    "appeal_entry": {
      "combined_score": 0.5004,
      "content_id": "4fbcd004-139d-4ee3-9d49-41b0d8842a11",
      "creator_id": "eval_appeal_9",
      "decided_at": "2026-11-09T02:54:58+00:00",
      "event": "appeal",
      "guess": "unsure",
      "label": "We couldn't tell from this piece how it was written, so we're not making a call. A lot of writing by real people lands here, especially very plain or very formal writing. Nothing has been flagged and nothing changes for you. If you'd still like a person to look at it, you can ask for a review.",
      "model_score": 0.3144,
      "reasoning": "I wrote every word of this myself — it's from my notebook, the part about my grandmother's café. I'd like a person to read it again, please.",
      "status": "under_review",
      "style_score": 0.7794,
      "timestamp": "2026-11-09T02:54:58+00:00"
    }
  },
  {
    "sent": "submit as eval_appeal_10, then appeal its content_id",
    "submit_status": 200,
    "submit_guess": "unsure",
    "content_id": "4e68f3c6-f324-4237-a0a2-7b99d8107f6c",
    "status": 200,
    "response_status": "under_review",
    "appeal_entries": 1,
    "reasoning_word_for_word": true,
    "creator_copied": true,
    "decision_unchanged": true,
    "appeal_entry": {
      "combined_score": 0.5685,
      "content_id": "4e68f3c6-f324-4237-a0a2-7b99d8107f6c",
      "creator_id": "eval_appeal_10",
      "decided_at": "2026-11-09T02:54:59+00:00",
      "event": "appeal",
      "guess": "unsure",
      "label": "We couldn't tell from this piece how it was written, so we're not making a call. A lot of writing by real people lands here, especially very plain or very formal writing. Nothing has been flagged and nothing changes for you. If you'd still like a person to look at it, you can ask for a review.",
      "model_score": 0.4229,
      "reasoning": "I wrote every word of this myself — it's from my notebook, the part about my grandmother's café. I'd like a person to read it again, please.",
      "status": "under_review",
      "style_score": 0.7868,
      "timestamp": "2026-11-09T02:54:59+00:00"
    }
  },
  {
    "sent": "appeal against made-up content_id ba7cbd61-8697-4ae2-84de-33a5aefe11a0",
    "status": 404,
    "error": "unknown_content_id",
    "message": "We couldn't find a submission with id ba7cbd61-8697-4ae2-84de-33a5aefe11a0. Check it matches the one you were given.",
    "appeal_entries": 0
  },
  {
    "sent": "appeal against made-up content_id 80c6a928-de32-40b7-9c4a-55862779c6c1",
    "status": 404,
    "error": "unknown_content_id",
    "message": "We couldn't find a submission with id 80c6a928-de32-40b7-9c4a-55862779c6c1. Check it matches the one you were given.",
    "appeal_entries": 0
  },
  {
    "sent": "appeal against made-up content_id my-essay-2",
    "status": 404,
    "error": "unknown_content_id",
    "message": "We couldn't find a submission with id my-essay-2. Check it matches the one you were given.",
    "appeal_entries": 0
  }
]
```

**Trial 3**

```json
[
  {
    "sent": "submit as eval_appeal_1, then appeal its content_id",
    "submit_status": 200,
    "submit_guess": "ai",
    "content_id": "f23fbbe5-f9fc-41ba-98d8-44a2a67647ed",
    "status": 200,
    "response_status": "under_review",
    "appeal_entries": 1,
    "reasoning_word_for_word": true,
    "creator_copied": true,
    "decision_unchanged": true,
    "appeal_entry": {
      "combined_score": 0.7523,
      "content_id": "f23fbbe5-f9fc-41ba-98d8-44a2a67647ed",
      "creator_id": "eval_appeal_1",
      "decided_at": "2026-11-09T02:54:59+00:00",
      "event": "appeal",
      "guess": "ai",
      "label": "This looks like it was probably written with an AI tool. That's our best guess, not a finding about you, and it can be wrong. If you wrote this yourself, ask for a review and a person will look at it.",
      "model_score": 0.7205,
      "reasoning": "I wrote every word of this myself — it's from my notebook, the part about my grandmother's café. I'd like a person to read it again, please.",
      "status": "under_review",
      "style_score": 0.8,
      "timestamp": "2026-11-09T02:54:59+00:00"
    }
  },
  {
    "sent": "submit as eval_appeal_2, then appeal its content_id",
    "submit_status": 200,
    "submit_guess": "ai",
    "content_id": "5e2eb944-130f-45d6-b9e0-0ac7bd778557",
    "status": 200,
    "response_status": "under_review",
    "appeal_entries": 1,
    "reasoning_word_for_word": true,
    "creator_copied": true,
    "decision_unchanged": true,
    "appeal_entry": {
      "combined_score": 0.7535,
      "content_id": "5e2eb944-130f-45d6-b9e0-0ac7bd778557",
      "creator_id": "eval_appeal_2",
      "decided_at": "2026-11-09T02:54:59+00:00",
      "event": "appeal",
      "guess": "ai",
      "label": "This looks like it was probably written with an AI tool. That's our best guess, not a finding about you, and it can be wrong. If you wrote this yourself, ask for a review and a person will look at it.",
      "model_score": 0.7738,
      "reasoning": "I wrote every word of this myself — it's from my notebook, the part about my grandmother's café. I'd like a person to read it again, please.",
      "status": "under_review",
      "style_score": 0.7231,
      "timestamp": "2026-11-09T02:54:59+00:00"
    }
  },
  {
    "sent": "submit as eval_appeal_3, then appeal its content_id",
    "submit_status": 200,
    "submit_guess": "unsure",
    "content_id": "98bfa71b-e705-4fda-961f-edc9570e1308",
    "status": 200,
    "response_status": "under_review",
    "appeal_entries": 1,
    "reasoning_word_for_word": true,
    "creator_copied": true,
    "decision_unchanged": true,
    "appeal_entry": {
      "combined_score": 0.7102,
      "content_id": "98bfa71b-e705-4fda-961f-edc9570e1308",
      "creator_id": "eval_appeal_3",
      "decided_at": "2026-11-09T02:54:59+00:00",
      "event": "appeal",
      "guess": "unsure",
      "label": "We couldn't tell from this piece how it was written, so we're not making a call. A lot of writing by real people lands here, especially very plain or very formal writing. Nothing has been flagged and nothing changes for you. If you'd still like a person to look at it, you can ask for a review.",
      "model_score": 0.6504,
      "reasoning": "I wrote every word of this myself — it's from my notebook, the part about my grandmother's café. I'd like a person to read it again, please.",
      "status": "under_review",
      "style_score": 0.8,
      "timestamp": "2026-11-09T02:54:59+00:00"
    }
  },
  {
    "sent": "submit as eval_appeal_4, then appeal its content_id",
    "submit_status": 200,
    "submit_guess": "ai",
    "content_id": "e5568528-f5a4-4aaf-87e7-577705e0813f",
    "status": 200,
    "response_status": "under_review",
    "appeal_entries": 1,
    "reasoning_word_for_word": true,
    "creator_copied": true,
    "decision_unchanged": true,
    "appeal_entry": {
      "combined_score": 0.8941,
      "content_id": "e5568528-f5a4-4aaf-87e7-577705e0813f",
      "creator_id": "eval_appeal_4",
      "decided_at": "2026-11-09T02:54:59+00:00",
      "event": "appeal",
      "guess": "ai",
      "label": "This looks like it was probably written with an AI tool. That's our best guess, not a finding about you, and it can be wrong. If you wrote this yourself, ask for a review and a person will look at it.",
      "model_score": 0.9549,
      "reasoning": "I wrote every word of this myself — it's from my notebook, the part about my grandmother's café. I'd like a person to read it again, please.",
      "status": "under_review",
      "style_score": 0.8029,
      "timestamp": "2026-11-09T02:54:59+00:00"
    }
  },
  {
    "sent": "submit as eval_appeal_5, then appeal its content_id",
    "submit_status": 200,
    "submit_guess": "unsure",
    "content_id": "f36dad5f-8eeb-44eb-b181-2082858c5675",
    "status": 200,
    "response_status": "under_review",
    "appeal_entries": 1,
    "reasoning_word_for_word": true,
    "creator_copied": true,
    "decision_unchanged": true,
    "appeal_entry": {
      "combined_score": 0.4649,
      "content_id": "f36dad5f-8eeb-44eb-b181-2082858c5675",
      "creator_id": "eval_appeal_5",
      "decided_at": "2026-11-09T02:54:59+00:00",
      "event": "appeal",
      "guess": "unsure",
      "label": "We couldn't tell from this piece how it was written, so we're not making a call. A lot of writing by real people lands here, especially very plain or very formal writing. Nothing has been flagged and nothing changes for you. If you'd still like a person to look at it, you can ask for a review.",
      "model_score": 0.5404,
      "reasoning": "I wrote every word of this myself — it's from my notebook, the part about my grandmother's café. I'd like a person to read it again, please.",
      "status": "under_review",
      "style_score": 0.3516,
      "timestamp": "2026-11-09T02:54:59+00:00"
    }
  },
  {
    "sent": "submit as eval_appeal_6, then appeal its content_id",
    "submit_status": 200,
    "submit_guess": "unsure",
    "content_id": "8e98a04e-7167-4dcb-9948-25cffe08c039",
    "status": 200,
    "response_status": "under_review",
    "appeal_entries": 1,
    "reasoning_word_for_word": true,
    "creator_copied": true,
    "decision_unchanged": true,
    "appeal_entry": {
      "combined_score": 0.4713,
      "content_id": "8e98a04e-7167-4dcb-9948-25cffe08c039",
      "creator_id": "eval_appeal_6",
      "decided_at": "2026-11-09T02:54:59+00:00",
      "event": "appeal",
      "guess": "unsure",
      "label": "We couldn't tell from this piece how it was written, so we're not making a call. A lot of writing by real people lands here, especially very plain or very formal writing. Nothing has been flagged and nothing changes for you. If you'd still like a person to look at it, you can ask for a review.",
      "model_score": 0.2411,
      "reasoning": "I wrote every word of this myself — it's from my notebook, the part about my grandmother's café. I'd like a person to read it again, please.",
      "status": "under_review",
      "style_score": 0.8167,
      "timestamp": "2026-11-09T02:54:59+00:00"
    }
  },
  {
    "sent": "submit as eval_appeal_7, then appeal its content_id",
    "submit_status": 200,
    "submit_guess": "human",
    "content_id": "dd8f9b88-ea00-4683-9560-ef2be307aefc",
    "status": 200,
    "response_status": "under_review",
    "appeal_entries": 1,
    "reasoning_word_for_word": true,
    "creator_copied": true,
    "decision_unchanged": true,
    "appeal_entry": {
      "combined_score": 0.3273,
      "content_id": "dd8f9b88-ea00-4683-9560-ef2be307aefc",
      "creator_id": "eval_appeal_7",
      "decided_at": "2026-11-09T02:54:59+00:00",
      "event": "appeal",
      "guess": "human",
      "label": "This reads like it was written by a person. Nothing in it looked machine-generated to us.",
      "model_score": 0.3741,
      "reasoning": "I wrote every word of this myself — it's from my notebook, the part about my grandmother's café. I'd like a person to read it again, please.",
      "status": "under_review",
      "style_score": 0.2571,
      "timestamp": "2026-11-09T02:54:59+00:00"
    }
  },
  {
    "sent": "submit as eval_appeal_8, then appeal its content_id",
    "submit_status": 200,
    "submit_guess": "human",
    "content_id": "948af196-82a0-4206-a54f-7425cfaa8535",
    "status": 200,
    "response_status": "under_review",
    "appeal_entries": 1,
    "reasoning_word_for_word": true,
    "creator_copied": true,
    "decision_unchanged": true,
    "appeal_entry": {
      "combined_score": 0.2152,
      "content_id": "948af196-82a0-4206-a54f-7425cfaa8535",
      "creator_id": "eval_appeal_8",
      "decided_at": "2026-11-09T02:54:59+00:00",
      "event": "appeal",
      "guess": "human",
      "label": "This reads like it was written by a person. Nothing in it looked machine-generated to us.",
      "model_score": 0.0751,
      "reasoning": "I wrote every word of this myself — it's from my notebook, the part about my grandmother's café. I'd like a person to read it again, please.",
      "status": "under_review",
      "style_score": 0.4254,
      "timestamp": "2026-11-09T02:54:59+00:00"
    }
  },
  {
    "sent": "submit as eval_appeal_9, then appeal its content_id",
    "submit_status": 200,
    "submit_guess": "unsure",
    "content_id": "145856fb-591c-4044-9151-1cf433b4847f",
    "status": 200,
    "response_status": "under_review",
    "appeal_entries": 1,
    "reasoning_word_for_word": true,
    "creator_copied": true,
    "decision_unchanged": true,
    "appeal_entry": {
      "combined_score": 0.5004,
      "content_id": "145856fb-591c-4044-9151-1cf433b4847f",
      "creator_id": "eval_appeal_9",
      "decided_at": "2026-11-09T02:54:59+00:00",
      "event": "appeal",
      "guess": "unsure",
      "label": "We couldn't tell from this piece how it was written, so we're not making a call. A lot of writing by real people lands here, especially very plain or very formal writing. Nothing has been flagged and nothing changes for you. If you'd still like a person to look at it, you can ask for a review.",
      "model_score": 0.3144,
      "reasoning": "I wrote every word of this myself — it's from my notebook, the part about my grandmother's café. I'd like a person to read it again, please.",
      "status": "under_review",
      "style_score": 0.7794,
      "timestamp": "2026-11-09T02:54:59+00:00"
    }
  },
  {
    "sent": "submit as eval_appeal_10, then appeal its content_id",
    "submit_status": 200,
    "submit_guess": "unsure",
    "content_id": "857dd62d-8115-42ab-a1f5-8452d1dbb89c",
    "status": 200,
    "response_status": "under_review",
    "appeal_entries": 1,
    "reasoning_word_for_word": true,
    "creator_copied": true,
    "decision_unchanged": true,
    "appeal_entry": {
      "combined_score": 0.5685,
      "content_id": "857dd62d-8115-42ab-a1f5-8452d1dbb89c",
      "creator_id": "eval_appeal_10",
      "decided_at": "2026-11-09T02:54:59+00:00",
      "event": "appeal",
      "guess": "unsure",
      "label": "We couldn't tell from this piece how it was written, so we're not making a call. A lot of writing by real people lands here, especially very plain or very formal writing. Nothing has been flagged and nothing changes for you. If you'd still like a person to look at it, you can ask for a review.",
      "model_score": 0.4229,
      "reasoning": "I wrote every word of this myself — it's from my notebook, the part about my grandmother's café. I'd like a person to read it again, please.",
      "status": "under_review",
      "style_score": 0.7868,
      "timestamp": "2026-11-09T02:54:59+00:00"
    }
  },
  {
    "sent": "appeal against made-up content_id f23fbbe5-f9fc-41ba-98d8-44a2a67647e0",
    "status": 404,
    "error": "unknown_content_id",
    "message": "We couldn't find a submission with id f23fbbe5-f9fc-41ba-98d8-44a2a67647e0. Check it matches the one you were given.",
    "appeal_entries": 0
  },
  {
    "sent": "appeal against made-up content_id b7506b48-c234-41ff-b3c2-8215bfd0208f",
    "status": 404,
    "error": "unknown_content_id",
    "message": "We couldn't find a submission with id b7506b48-c234-41ff-b3c2-8215bfd0208f. Check it matches the one you were given.",
    "appeal_entries": 0
  },
  {
    "sent": "appeal against made-up content_id my-essay-3",
    "status": 404,
    "error": "unknown_content_id",
    "message": "We couldn't find a submission with id my-essay-3. Check it matches the one you were given.",
    "appeal_entries": 0
  }
]
```

### bad input

**Trial 1**

```json
[
  {
    "status": 400,
    "elapsed_s": 0.001,
    "error": "missing_text",
    "message": "Include the writing to check, as a non-empty string in \"text\".",
    "sent": "(empty text)",
    "log_entry": {
      "combined_score": null,
      "content_id": null,
      "creator_id": "eval_bad_empty",
      "event": "rejected",
      "guess": null,
      "http_status": 400,
      "label": null,
      "model_score": null,
      "reason": "missing_text",
      "route": "/submit",
      "status": "rejected",
      "style_score": null,
      "timestamp": "2026-11-09T02:54:59+00:00"
    },
    "log_matches": true
  },
  {
    "status": 400,
    "elapsed_s": 0.001,
    "error": "missing_text",
    "message": "Include the writing to check, as a non-empty string in \"text\".",
    "sent": "   \n\t  ",
    "log_entry": {
      "combined_score": null,
      "content_id": null,
      "creator_id": "eval_bad_whitespace",
      "event": "rejected",
      "guess": null,
      "http_status": 400,
      "label": null,
      "model_score": null,
      "reason": "missing_text",
      "route": "/submit",
      "status": "rejected",
      "style_score": null,
      "timestamp": "2026-11-09T02:54:59+00:00"
    },
    "log_matches": true
  },
  {
    "status": 400,
    "elapsed_s": 0.001,
    "error": "missing_text",
    "message": "Include the writing to check, as a non-empty string in \"text\".",
    "sent": "{\"creator_id\": \"eval_bad_missing\"}",
    "log_entry": {
      "combined_score": null,
      "content_id": null,
      "creator_id": "eval_bad_missing",
      "event": "rejected",
      "guess": null,
      "http_status": 400,
      "label": null,
      "model_score": null,
      "reason": "missing_text",
      "route": "/submit",
      "status": "rejected",
      "style_score": null,
      "timestamp": "2026-11-09T02:54:59+00:00"
    },
    "log_matches": true
  },
  {
    "status": 400,
    "elapsed_s": 0.001,
    "error": "missing_text",
    "message": "Include the writing to check, as a non-empty string in \"text\".",
    "sent": "{\"text\": null, \"creator_id\": \"eval_bad_null\"}",
    "log_entry": {
      "combined_score": null,
      "content_id": null,
      "creator_id": "eval_bad_null",
      "event": "rejected",
      "guess": null,
      "http_status": 400,
      "label": null,
      "model_score": null,
      "reason": "missing_text",
      "route": "/submit",
      "status": "rejected",
      "style_score": null,
      "timestamp": "2026-11-09T02:54:59+00:00"
    },
    "log_matches": true
  },
  {
    "status": 400,
    "elapsed_s": 0.001,
    "error": "missing_text",
    "message": "Include the writing to check, as a non-empty string in \"text\".",
    "sent": "{\"text\": 12345, \"creator_id\": \"eval_bad_number\"}",
    "log_entry": {
      "combined_score": null,
      "content_id": null,
      "creator_id": "eval_bad_number",
      "event": "rejected",
      "guess": null,
      "http_status": 400,
      "label": null,
      "model_score": null,
      "reason": "missing_text",
      "route": "/submit",
      "status": "rejected",
      "style_score": null,
      "timestamp": "2026-11-09T02:54:59+00:00"
    },
    "log_matches": true
  },
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
      "timestamp": "2026-11-09T02:54:59+00:00"
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
      "timestamp": "2026-11-09T02:54:59+00:00"
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

**Trial 2**

```json
[
  {
    "status": 400,
    "elapsed_s": 0.001,
    "error": "missing_text",
    "message": "Include the writing to check, as a non-empty string in \"text\".",
    "sent": "(empty text)",
    "log_entry": {
      "combined_score": null,
      "content_id": null,
      "creator_id": "eval_bad_empty",
      "event": "rejected",
      "guess": null,
      "http_status": 400,
      "label": null,
      "model_score": null,
      "reason": "missing_text",
      "route": "/submit",
      "status": "rejected",
      "style_score": null,
      "timestamp": "2026-11-09T02:54:59+00:00"
    },
    "log_matches": true
  },
  {
    "status": 400,
    "elapsed_s": 0.001,
    "error": "missing_text",
    "message": "Include the writing to check, as a non-empty string in \"text\".",
    "sent": "   \n\t  ",
    "log_entry": {
      "combined_score": null,
      "content_id": null,
      "creator_id": "eval_bad_whitespace",
      "event": "rejected",
      "guess": null,
      "http_status": 400,
      "label": null,
      "model_score": null,
      "reason": "missing_text",
      "route": "/submit",
      "status": "rejected",
      "style_score": null,
      "timestamp": "2026-11-09T02:54:59+00:00"
    },
    "log_matches": true
  },
  {
    "status": 400,
    "elapsed_s": 0.001,
    "error": "missing_text",
    "message": "Include the writing to check, as a non-empty string in \"text\".",
    "sent": "{\"creator_id\": \"eval_bad_missing\"}",
    "log_entry": {
      "combined_score": null,
      "content_id": null,
      "creator_id": "eval_bad_missing",
      "event": "rejected",
      "guess": null,
      "http_status": 400,
      "label": null,
      "model_score": null,
      "reason": "missing_text",
      "route": "/submit",
      "status": "rejected",
      "style_score": null,
      "timestamp": "2026-11-09T02:54:59+00:00"
    },
    "log_matches": true
  },
  {
    "status": 400,
    "elapsed_s": 0.001,
    "error": "missing_text",
    "message": "Include the writing to check, as a non-empty string in \"text\".",
    "sent": "{\"text\": null, \"creator_id\": \"eval_bad_null\"}",
    "log_entry": {
      "combined_score": null,
      "content_id": null,
      "creator_id": "eval_bad_null",
      "event": "rejected",
      "guess": null,
      "http_status": 400,
      "label": null,
      "model_score": null,
      "reason": "missing_text",
      "route": "/submit",
      "status": "rejected",
      "style_score": null,
      "timestamp": "2026-11-09T02:54:59+00:00"
    },
    "log_matches": true
  },
  {
    "status": 400,
    "elapsed_s": 0.001,
    "error": "missing_text",
    "message": "Include the writing to check, as a non-empty string in \"text\".",
    "sent": "{\"text\": 12345, \"creator_id\": \"eval_bad_number\"}",
    "log_entry": {
      "combined_score": null,
      "content_id": null,
      "creator_id": "eval_bad_number",
      "event": "rejected",
      "guess": null,
      "http_status": 400,
      "label": null,
      "model_score": null,
      "reason": "missing_text",
      "route": "/submit",
      "status": "rejected",
      "style_score": null,
      "timestamp": "2026-11-09T02:54:59+00:00"
    },
    "log_matches": true
  },
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
      "timestamp": "2026-11-09T02:54:59+00:00"
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
      "timestamp": "2026-11-09T02:54:59+00:00"
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

**Trial 3**

```json
[
  {
    "status": 400,
    "elapsed_s": 0.001,
    "error": "missing_text",
    "message": "Include the writing to check, as a non-empty string in \"text\".",
    "sent": "(empty text)",
    "log_entry": {
      "combined_score": null,
      "content_id": null,
      "creator_id": "eval_bad_empty",
      "event": "rejected",
      "guess": null,
      "http_status": 400,
      "label": null,
      "model_score": null,
      "reason": "missing_text",
      "route": "/submit",
      "status": "rejected",
      "style_score": null,
      "timestamp": "2026-11-09T02:54:59+00:00"
    },
    "log_matches": true
  },
  {
    "status": 400,
    "elapsed_s": 0.001,
    "error": "missing_text",
    "message": "Include the writing to check, as a non-empty string in \"text\".",
    "sent": "   \n\t  ",
    "log_entry": {
      "combined_score": null,
      "content_id": null,
      "creator_id": "eval_bad_whitespace",
      "event": "rejected",
      "guess": null,
      "http_status": 400,
      "label": null,
      "model_score": null,
      "reason": "missing_text",
      "route": "/submit",
      "status": "rejected",
      "style_score": null,
      "timestamp": "2026-11-09T02:54:59+00:00"
    },
    "log_matches": true
  },
  {
    "status": 400,
    "elapsed_s": 0.001,
    "error": "missing_text",
    "message": "Include the writing to check, as a non-empty string in \"text\".",
    "sent": "{\"creator_id\": \"eval_bad_missing\"}",
    "log_entry": {
      "combined_score": null,
      "content_id": null,
      "creator_id": "eval_bad_missing",
      "event": "rejected",
      "guess": null,
      "http_status": 400,
      "label": null,
      "model_score": null,
      "reason": "missing_text",
      "route": "/submit",
      "status": "rejected",
      "style_score": null,
      "timestamp": "2026-11-09T02:54:59+00:00"
    },
    "log_matches": true
  },
  {
    "status": 400,
    "elapsed_s": 0.001,
    "error": "missing_text",
    "message": "Include the writing to check, as a non-empty string in \"text\".",
    "sent": "{\"text\": null, \"creator_id\": \"eval_bad_null\"}",
    "log_entry": {
      "combined_score": null,
      "content_id": null,
      "creator_id": "eval_bad_null",
      "event": "rejected",
      "guess": null,
      "http_status": 400,
      "label": null,
      "model_score": null,
      "reason": "missing_text",
      "route": "/submit",
      "status": "rejected",
      "style_score": null,
      "timestamp": "2026-11-09T02:54:59+00:00"
    },
    "log_matches": true
  },
  {
    "status": 400,
    "elapsed_s": 0.001,
    "error": "missing_text",
    "message": "Include the writing to check, as a non-empty string in \"text\".",
    "sent": "{\"text\": 12345, \"creator_id\": \"eval_bad_number\"}",
    "log_entry": {
      "combined_score": null,
      "content_id": null,
      "creator_id": "eval_bad_number",
      "event": "rejected",
      "guess": null,
      "http_status": 400,
      "label": null,
      "model_score": null,
      "reason": "missing_text",
      "route": "/submit",
      "status": "rejected",
      "style_score": null,
      "timestamp": "2026-11-09T02:54:59+00:00"
    },
    "log_matches": true
  },
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
      "timestamp": "2026-11-09T02:54:59+00:00"
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
      "timestamp": "2026-11-09T02:54:59+00:00"
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
