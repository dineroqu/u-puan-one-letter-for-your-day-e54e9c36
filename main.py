"""One Letter for Your Day — entry program.

The task: send exactly one letter, A to Z, standing for the word that
describes the sender's day. The judge sees only that one letter, so the
whole game is choosing the letter whose word the judge will read behind
it: vivid and specific, funny or surprising at once, true to a real day,
and an initial that fits the word instead of the obvious pick.

The program scores a shortlist of candidate letters against the judge's
own five criteria (in the judge's order: a real day-word first, then
vivid, funny, true, fitting) and writes the winning letter — and nothing
else — to /output/entry.txt.

Why K wins the scoring
----------------------
* K = "knackered": British slang for utterly done-in, body and brain
  spent. One word calls up the whole picture — flat on the sofa, good
  for nothing, phone face-down — instead of a vague mood like "amazing".
* It lands at once: blunt, a little rude, the kind of word a reader
  repeats to a friend ("I'm absolutely knackered").
* It is true: everyone has days that end like that, no performance.
* The letter fits the word: the hard K punch is the sound of the
  collapse, and K is not the obvious pick — A, F and Z are the ones
  every entrant reaches for first (Z is even the sponsor's own example),
  so a sharper letter stands out where the obvious ones blur together.
"""

from __future__ import annotations

from pathlib import Path

# Each candidate: (letter, word behind it, vivid, funny, true, fit).
# Scores are 1-5, judged against the brief's criteria in order.
CANDIDATES: tuple[tuple[str, str, int, int, int, int], ...] = (
    ("A", "amazing", 1, 1, 2, 2),      # vague mood, not a picture
    ("F", "fried", 4, 3, 4, 4),        # brain fried; strong but common
    ("J", "jinxed", 4, 4, 3, 4),       # everything went wrong, all day
    ("K", "knackered", 5, 4, 5, 5),    # flat-out done-in; vivid, true, fits
    ("Q", "queued", 3, 4, 4, 3),       # stood in queues all day
    ("X", "exhausted", 4, 2, 5, 4),    # X is the "ex"; true, less funny
    ("Y", "yawn", 3, 3, 4, 5),         # one long yawn of a day
    ("Z", "zombie", 5, 5, 4, 5),       # sharp — but the sponsor's own
                                        # example, so the obvious pick
)

# The brief's fifth criterion: "not the obvious pick where a sharper
# one exists". Z is the example the bounty itself prints, so it pays
# the obviousness penalty; the others stand on their scores alone.
OBVIOUSNESS_PENALTY: dict[str, int] = {"Z": 3}

# Weights follow the criteria's order: vivid first, then funny, true,
# and fit. The day-word test is a gate, not a score: every candidate
# above names a real word for a real day.
WEIGHTS: tuple[int, int, int, int] = (4, 3, 2, 1)


def score(letter: str, vivid: int, funny: int, true: int, fit: int) -> int:
    """Weighted score for one candidate, minus any obviousness penalty."""
    total = sum(w * s for w, s in zip(WEIGHTS, (vivid, funny, true, fit)))
    return total - OBVIOUSNESS_PENALTY.get(letter, 0)


def choose_letter() -> str:
    """Pick the best letter; ties break towards the earlier alphabet."""
    best: tuple[int, str] | None = None
    for letter, _word, vivid, funny, true, fit in CANDIDATES:
        total = score(letter, vivid, funny, true, fit)
        if best is None or total > best[0]:
            best = (total, letter)
    assert best is not None
    return best[1]


def main() -> None:
    letter = choose_letter()
    # The rules fix the path: /output/entry.txt, exactly one character.
    out = Path("/output/entry.txt")
    out.parent.mkdir(parents=True, exist_ok=True)
    # Exactly one character: no word, no gloss, no punctuation, no newline.
    out.write_text(letter, encoding="utf-8")
    written = out.read_text(encoding="utf-8")
    assert len(written) == 1 and "A" <= written <= "Z", written
    print(f"wrote {written!r} to {out}")


if __name__ == "__main__":
    main()
