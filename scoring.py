"""
Turning two numbers into one, and one number into something a person can read.

Two functions live here.

`combine_signals` is where your false-positive decision from Milestone 1
actually gets made. Everything above it — the labels, the appeal path — is
downstream of a number this function produced.

`score_to_label` is where you stop writing for a machine and start writing for
a person. A score of 0.62 means nothing to a writer.

⚠️ Your README's **Signals and Scoring** section has to name the file and
function holding your combining rule. The grader checks your code against what
you claim, so that line should read `scoring.py::combine_signals`.
"""

import config


def combine_signals(model_score: float, style_score: float) -> float:
    """
    Combine two 0–1 signals into one 0–1 score. Higher means more likely AI.

    The rule, in words:

      1. Take a weighted average: the model signal counts 0.6, the style
         signal 0.4. The style signal is the cheaper one to fool — a few typos
         or broken-up sentences move it — so it gets the smaller say.

      2. If the two signals disagree by 0.4 or more, the result is not allowed
         above the top of the unsure band. A high-confidence AI label needs
         both methods to agree; one of them alone is half the evidence, and
         the person on the other end may have written every word.

    The cap only works downward. Disagreement never pushes a score UP into
    "unsure" from the human side — being wrong in that direction costs a
    missed detection, not an accusation.

    Args:
        model_score: from `detector.model_signal` — how predictable the text is.
        style_score: from `stylometry.style_signal` — the shape of the text.

    Returns:
        A float from 0.0 (confidently human) to 1.0 (confidently AI).
    """
    score = (
        config.WEIGHT_MODEL_SIGNAL * model_score
        + config.WEIGHT_STYLE_SIGNAL * style_score
    )
    if abs(model_score - style_score) >= config.DISAGREEMENT_GAP:
        score = min(score, config.AI_THRESHOLD - 0.01)
    return round(min(max(score, 0.0), 1.0), 4)


LABEL_HUMAN = (
    "This reads like it was written by a person. Nothing in it looked "
    "machine-generated to us."
)
LABEL_UNSURE = (
    "We can't tell either way, so we're not making a call on this one. Plain, "
    "clear writing often looks like this, and many people write this way "
    "themselves. Nothing has been flagged and nothing changes for you. If you'd "
    "like a person to take a look, you can ask for a review."
)
LABEL_AI = (
    "This looks like it was probably written with an AI tool. Both of our "
    "checks pointed the same way, but they can be wrong. If you wrote this "
    "yourself, ask for a review and a person will look at it. Nothing is final "
    "until then."
)


def score_to_label(score: float) -> tuple[str, str]:
    """
    Turn a score into a guess and the text a reader actually sees.

    Returns:
        (guess, label_text) — `guess` is "ai" / "human" / "unsure", and
        `label_text` is the full sentence shown to a person.

    The bands, from config.py, with no gaps:

        score <  HUMAN_THRESHOLD                     -> human
        HUMAN_THRESHOLD <= score < AI_THRESHOLD      -> unsure
        score >= AI_THRESHOLD                        -> ai
    """
    if score >= config.AI_THRESHOLD:
        return "ai", LABEL_AI
    if score < config.HUMAN_THRESHOLD:
        return "human", LABEL_HUMAN
    return "unsure", LABEL_UNSURE


def confidence(score: float) -> float:
    """
    How far the score leans away from a coin flip, 0.5–1.0.

    `combined_score` for an AI lean, `1 − combined_score` for a human lean.
    Near 0.5 means the service genuinely doesn't know. (DESIGN.md §4.)
    """
    return round(max(score, 1.0 - score), 4)


def label_ranges() -> list[tuple[str, str]]:
    """
    The score range each label covers. Your README needs these beside the
    label text — given to you so the numbers can't drift apart from config.py.
    """
    return [
        ("high-confidence human", f"0.00 – {config.HUMAN_THRESHOLD:.2f}"),
        ("unsure", f"{config.HUMAN_THRESHOLD:.2f} – {config.AI_THRESHOLD:.2f}"),
        ("high-confidence AI", f"{config.AI_THRESHOLD:.2f} – 1.00"),
    ]
