"""
Signal two: the style signal.

Signal one reads the text for meaning. This one measures it *as text* — the
shape of it, without understanding a word.

Three measures are stubbed below because the brief names those three. They are
stubs, not implementations: what they compute is yours, and so is how you
combine them.

    sentence_length_spread   do sentences vary in length, or march in step?
    type_token_ratio         how much of the vocabulary repeats?
    punctuation_density      how much punctuation, and how varied?

Why these might differ between human and AI writing: generated prose tends
toward even, mid-length sentences and a narrower band of vocabulary, because
that's what "most likely next word" produces on average. Human writing is
lumpier — a three-word sentence next to a forty-word one.

⚠️ **The blind spot, which you have to name in Milestone 1.**

This signal cannot read. It has no idea what the text says. Anything that
changes the shape without changing the substance moves it — adding typos,
breaking up sentences, pasting in a quotation. That is a very cheap thing for
someone to do on purpose, and unit 8's attack set will do it to you.

Build each function on its own and call it from a terminal before you wire
anything together:

    python stylometry.py "some text to look at"
"""

import re
import statistics


def sentences(text: str) -> list[str]:
    """Split into sentences. Rough and good enough — given to you."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p.strip()]


def words(text: str) -> list[str]:
    """Split into lowercase words, punctuation stripped. Given to you."""
    return re.findall(r"[a-z0-9']+", text.lower())


# ── The three measures — YOU BUILD THESE ─────────────────────────────────────

def sentence_length_spread(text: str) -> float:
    """
    How much sentence length varies.

    Returns:
        The coefficient of variation of words-per-sentence: stdev / mean.
        0.0 means every sentence is the same length; human prose usually sits
        around 0.4–0.8, generated prose lower. **Higher means more human.**

    Fewer than two sentences has no spread to measure, so it returns 0.0 —
    and `style_signal` treats that case as "can't tell" rather than as
    "perfectly even", because one sentence isn't evidence of anything.
    """
    lengths = [len(words(s)) for s in sentences(text)]
    lengths = [n for n in lengths if n > 0]
    if len(lengths) < 2:
        return 0.0
    mean = statistics.mean(lengths)
    return round(statistics.stdev(lengths) / mean, 4)


TTR_WINDOW = 50


def type_token_ratio(text: str) -> float:
    """
    Unique words over total words, averaged over a sliding window.

    Returns:
        A float between 0 and 1. **Higher means more varied vocabulary**, which
        reads as more human.

    Plain TTR falls as text gets longer, so this is the moving-average version:
    TTR of every 50-word window, averaged. A 100-word text and a 600-word text
    then land on the same scale. Shorter than one window falls back to plain
    TTR, which runs high on very short text — another reason short input is
    weak evidence.
    """
    tokens = words(text)
    if not tokens:
        return 0.0
    if len(tokens) <= TTR_WINDOW:
        return round(len(set(tokens)) / len(tokens), 4)
    ratios = [
        len(set(tokens[i:i + TTR_WINDOW])) / TTR_WINDOW
        for i in range(len(tokens) - TTR_WINDOW + 1)
    ]
    return round(statistics.mean(ratios), 4)


EXPRESSIVE_PUNCTUATION = re.compile(r"[;:()!?\u2014\u2013]|--| - ")


def punctuation_density(text: str) -> float:
    """
    Expressive punctuation per 100 words.

    Returns:
        A float, 0 upward. **Higher means more human.**

    Counts semicolons, colons, parentheses, dashes, exclamation and question
    marks — not full stops or commas, which everyone uses about equally. These
    are the marks that vary from writer to writer: an aside, an interruption,
    a question to the reader.

    Known weakness: recent chat models love the em dash, so this measure can
    point the wrong way on their output.
    """
    n_words = len(words(text))
    if n_words == 0:
        return 0.0
    marks = len(EXPRESSIVE_PUNCTUATION.findall(text))
    return round(100 * marks / n_words, 4)


# ── Combining them ───────────────────────────────────────────────────────────

# Each measure is mapped onto 0–1 "AI-ness" by a straight line between two
# anchors: the value typical of generated prose (scores 1.0) and the value
# typical of human prose (scores 0.0). Anything past an anchor is clamped.
# Anchors come from the calibration inputs in Milestone 4 — see the README.
#
#   measure                  AI anchor  human anchor  weight
SPREAD_ANCHORS = (0.25, 0.65)
TTR_ANCHORS = (0.72, 0.86)
PUNCT_ANCHORS = (0.5, 4.0)
STYLE_WEIGHTS = {"spread": 0.50, "ttr": 0.20, "punct": 0.30}

# Below this many sentences, spread isn't measured at all.
MIN_SENTENCES_FOR_SPREAD = 3

# The plain-writing guard. Generated prose is even AND mid-length; a learner or
# a deliberately plain writer is even and SHORT. Evenness only counts as AI
# evidence in proportion to mean sentence length: not at all at 7 words or
# fewer, fully at 12 or more. Without this, the false positive traced in
# DESIGN.md §3 scored 1.0 on this signal. The cost: AI text told to write in
# short sentences slips under it.
PLAIN_GUARD_WORDS = (7.0, 12.0)


def _ai_ness(value: float, anchors: tuple[float, float]) -> float:
    """0–1, where 1 means the value sits at or past the AI anchor."""
    ai, human = anchors
    position = (human - value) / (human - ai)
    return min(max(position, 0.0), 1.0)


def style_parts(text: str) -> dict:
    """Each measure's raw value and its 0–1 AI-ness. Handy for debugging."""
    spread = sentence_length_spread(text)
    ttr = type_token_ratio(text)
    punct = punctuation_density(text)
    parts = {
        "spread": (spread, _ai_ness(spread, SPREAD_ANCHORS)),
        "ttr": (ttr, _ai_ness(ttr, TTR_ANCHORS)),
        "punct": (punct, _ai_ness(punct, PUNCT_ANCHORS)),
    }
    # Two sentences can't show a spread; score that measure as a coin flip
    # rather than as "perfectly even, so AI".
    sents = sentences(text)
    if len(sents) < MIN_SENTENCES_FOR_SPREAD:
        parts["spread"] = (spread, 0.5)
    else:
        mean_len = len(words(text)) / len(sents)
        short, full = PLAIN_GUARD_WORDS
        guard = min(max((mean_len - short) / (full - short), 0.0), 1.0)
        parts["spread"] = (spread, parts["spread"][1] * guard)
    return parts


def style_signal(text: str) -> float:
    """
    The style signal as a 0–1 score. **Higher means more likely AI.**

    All three measures run "higher = more human", so each is flipped by
    `_ai_ness`, which also puts them on the same 0–1 scale using the anchors
    above. The result is their weighted average:

        spread 0.50 — the strongest separator in calibration, discounted
                      for short sentences by the plain-writing guard
        ttr    0.20 — barely separated AI from human in calibration, and
                      mostly flagged plain writers; kept, but light
        punct  0.30 — unreliable on em-dash-heavy chat output
    """
    if not words(text):
        return 0.5
    parts = style_parts(text)
    score = sum(STYLE_WEIGHTS[name] * ai for name, (_, ai) in parts.items())
    return round(min(max(score, 0.0), 1.0), 4)


if __name__ == "__main__":
    import sys

    text = " ".join(sys.argv[1:]) or (
        "The system works well. It handles most cases correctly and provides "
        "good results. Users generally find it easy to use and understand."
    )

    print(f"{len(sentences(text))} sentences, {len(words(text))} words\n")
    print(f"sentence_length_spread   {sentence_length_spread(text)}")
    print(f"type_token_ratio         {type_token_ratio(text)}")
    print(f"punctuation_density      {punctuation_density(text)}")
    print(f"style_signal             {style_signal(text)}   (higher = more likely AI)")
