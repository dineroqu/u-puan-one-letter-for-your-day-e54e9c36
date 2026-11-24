"""One Letter for Your Day — the letter K, for "knackered".

The judge sees only a single letter and infers the word behind it, scoring
candidates on five criteria, most important first: the word is a real
day-word, it is vivid and specific, it is funny or surprising, it feels
true to a real day, and the initial fits the word (with a sharper pick
beating the obvious one).

Candidate words were scored against those criteria (weights: vivid 4,
funny 3, true 2, fit 1), with an obviousness penalty of 3 for Z — the
sponsor's own printed example, so the pick every entrant reaches for
first:

    letter  word       vivid  funny  true  fit  score
    A       amazing       1      1     2    2    13
    F       fried         4      3     4    4    37
    J       jinxed        4      4     3    4    38
    K       knackered     5      4     5    5    47
    Q       queued        3      4     4    3    35
    X       exhausted     4      2     5    4    36
    Y       yawn          3      3     4    5    34
    Z       zombie        5      5     4    5    48 - 3 = 45

Why K wins: one word paints the whole picture — flat on the sofa, good
for nothing — instead of a vague mood; blunt British slang that lands at
once; true of everyone's worst days; the hard K punch fits the word; and
it is not the obvious pick (A, F and Z are what every entrant reaches
for first).

The program writes exactly one letter, "K", with no newline, to
/output/entry.txt.
"""

WEIGHTS = (4, 3, 2, 1)  # vivid, funny, true, fit
OBVIOUSNESS_PENALTY = {"Z": 3}

# (letter, word, vivid, funny, true, fit)
CANDIDATES = [
    ("A", "amazing", 1, 1, 2, 2),
    ("F", "fried", 4, 3, 4, 4),
    ("J", "jinxed", 4, 4, 3, 4),
    ("K", "knackered", 5, 4, 5, 5),
    ("Q", "queued", 3, 4, 4, 3),
    ("X", "exhausted", 4, 2, 5, 4),
    ("Y", "yawn", 3, 3, 4, 5),
    ("Z", "zombie", 5, 5, 4, 5),
]


def score(candidate):
    """Score one candidate: weighted criteria minus obviousness penalty."""
    _, _, vivid, funny, true, fit = candidate
    total = sum(w * v for w, v in zip(WEIGHTS, (vivid, funny, true, fit)))
    return total - OBVIOUSNESS_PENALTY.get(candidate[0], 0)


def choose_letter():
    """Pick the highest-scoring letter; ties go to the earlier alphabet."""
    best = None
    best_score = None
    for candidate in CANDIDATES:
        # Sanity: the letter is a single capital A-Z.
        assert len(candidate[0]) == 1 and "A" <= candidate[0] <= "Z"
        # Note: X stands for "exhausted" by its opening "ex-" sound,
        # not by spelling — the fit criterion is sound and shape.
        candidate_score = score(candidate)
        if best_score is None or candidate_score > best_score:
            best, best_score = candidate, candidate_score
    return best[0]


def main():
    letter = choose_letter()
    assert len(letter) == 1 and "A" <= letter <= "Z"
    with open("/output/entry.txt", "w", encoding="utf-8", newline="") as handle:
        handle.write(letter)
    with open("/output/entry.txt", "rb") as handle:
        written = handle.read()
    assert written == letter.encode("ascii") and len(written) == 1


if __name__ == "__main__":
    main()
