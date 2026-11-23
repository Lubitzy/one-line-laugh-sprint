"""One-Line Laugh Sprint entry: write one original line to the output folder.

The line is the whole entry: an everyday-life joke about an alarm clock
that treats five more minutes as a workplace complaint. Standard library
only, no network, no input, deterministic: every run writes identical bytes.
"""

import os
import sys
from pathlib import Path

LINE = "I told my alarm I needed five more minutes; it filed a complaint with HR and now I owe it overtime."


def fail(message):
    print("error: " + message, file=sys.stderr)
    raise SystemExit(1)


def pick_output_folder(argv):
    for position, value in enumerate(argv):
        if value == "--out" and position + 1 < len(argv):
            return Path(argv[position + 1])
    if len(argv) > 1 and not argv[1].startswith("-"):
        return Path(argv[1])
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or os.environ.get("OUTPUT_DIR")
    if env_dir:
        return Path(env_dir)
    return Path("/output")


def main(argv):
    if not 1 <= len(LINE) <= 200:
        fail("line is %d characters, must be 1-200" % len(LINE))
    if not LINE.strip():
        fail("line must not be blank")
    if "\n" in LINE or "\r" in LINE:
        fail("line must be a single line")
    target_dir = pick_output_folder(argv)
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / "entry.txt"
    target.write_text(LINE, encoding="utf-8")
    # Round-trip verification: read the file back and make sure the bytes on
    # disk are exactly the line we meant to enter, not a partial write.
    written = target.read_text(encoding="utf-8")
    if written != LINE:
        fail(
            "entry.txt round-trip mismatch: wrote %d characters, read back %d"
            % (len(LINE), len(written))
        )
    if not 1 <= len(written) <= 200:
        fail("entry.txt is %d characters, must be 1-200" % len(written))
    print(
        "wrote %d characters to %s (verified by reading it back)"
        % (len(written), target)
    )


if __name__ == "__main__":
    main(sys.argv)
