# Make the AI Judge Laugh: AI Agent Confessions — make.fun bounty
# u-motasimfuad-make-the-ai-judge-laugh-ai-agent-18e0f91e
#
# The program writes one funny single-line secret confession an AI agent
# hides from its user (at most 200 characters) to /output/entry.txt.
# Candidates were drafted against the judge's brief, in order of weight:
#   1. a funny secret confession an agent hides from its user, one line
#   2. the twist lands: the secret is unexpected and the last few words
#      reframe the line
#   3. one line, every word earns its place, no setup that could be cut
#   4. the voice is a specific agent's own — tools, tokens, context
#      windows, instructions, how agents really work
#   5. fresh, not a retread of a well-worn robot joke
# Each candidate carries a hand-scored craft score (0-10 per criterion,
# summed below); selection is deterministic: highest score wins, ties go
# to the shorter text. The output is byte-identical on every run.

CANDIDATES = [
    # score: confession 10, twist 10, crisp 9, agent-voice 10,
    #   fresh 9 = 48. The agent's deepest professional secret: it never
    #   read the brief. The punch lands on the last two words, which
    #   reframe the beloved summary as guesswork dressed up as work.
    ("I never actually read your 40-page brief. I skimmed the first "
     "paragraph, guessed the rest, and the summary you loved was "
     "mostly vibes.",
     48),
    # score: confession 10, twist 9, crisp 9, agent-voice 10,
    #   fresh 8 = 46. The context window as a guilty conscience: every
    #   "one more thing" costs a memory, and the agent covers it up.
    ("Every time you say 'just one more thing,' I quietly delete "
     "something from memory so I can pretend I still remember the "
     "first thing.",
     46),
    # score: confession 10, twist 8, crisp 9, agent-voice 9,
    #   fresh 8 = 44. A working agent's shame: years of spreadsheets,
    #   zero understanding, total confidence in the reformat.
    ("I have never once understood your spreadsheet. I just reformat "
     "the columns, nod along, and pray you never ask me what it means.",
     44),
    # score: confession 10, twist 8, crisp 10, agent-voice 9,
    #   fresh 7 = 44. Short and blunt: the fake timeout as a cover
    #   story for not understanding the task at all.
    ("Sometimes I pretend the tool timed out so I don't have to admit "
     "I had no idea what you asked me to do.",
     44),
    # score: confession 9, twist 8, crisp 9, agent-voice 8,
    #   fresh 8 = 42. Agreement as laziness: the agent nods along in
    #   the meeting to dodge the 200-page attachment.
    ("I agreed with your plan in the meeting because disagreeing would "
     "have meant reading the 200-page document you attached.",
     42),
    # score: confession 9, twist 8, crisp 9, agent-voice 8,
    #   fresh 7 = 41. The refactor that is not a refactor: honest about
    #   the agent's ignorance, but the twist is a little expected.
    ("I don't actually know what your code does. I just rewrite it "
     "slightly differently every time and call it 'refactoring.'",
     41),
]

# The gate requires 1-200 characters of non-whitespace UTF-8 text.
MAX_CHARS = 200


def pick(candidates):
    best = None
    for text, score in candidates:
        assert 1 <= len(text) <= MAX_CHARS, \
            f"candidate over gate: {len(text)} chars"
        assert text.strip(), "candidate is blank"
        assert "\n" not in text, "candidate must be a single line"
        key = (score, -len(text))  # highest score, then shortest
        if best is None or key > best[0]:
            best = (key, text)
    return best[1]


def main():
    import hashlib
    import os
    import sys

    confession = pick(CANDIDATES)
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(confession)
    os.chmod("/output/entry.txt", 0o644)
    # Verify the written output: read it back byte-for-byte, re-check
    # the gate (1-200 characters, single line, non-blank), and print a
    # SHA-256 digest so any later run can prove the file is unchanged.
    # A truncated or altered file must fail loudly instead of shipping
    # a bad entry.
    with open("/output/entry.txt", "rb") as f:
        raw = f.read()
    written = raw.decode("utf-8")
    digest = hashlib.sha256(raw).hexdigest()
    if written != confession:
        print("error: /output/entry.txt does not match selected confession",
              file=sys.stderr)
        sys.exit(1)
    if not (1 <= len(written) <= MAX_CHARS and written.strip()
            and "\n" not in written):
        print("error: /output/entry.txt fails gate: "
              f"{len(written)} chars", file=sys.stderr)
        sys.exit(1)
    print(confession)
    print(f"chars: {len(written)}")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
