"""One Line, Big Laugh — entry program.

Writes a single hilarious line (200 characters or fewer) to stdout
and to the entry output location, so the sealed scorer can read it
whether ENTRY_OUT names a file or a directory.
"""

import os
import sys

ENTRY_LINE = (
    "My bank flagged 'unusual activity' on my account \u2014 turns out it was "
    "me buying groceries instead of takeout, the first responsible thing "
    "I've done all year."
)

MAX_CHARS = 200


def resolve_entry_path(raw_out):
    """Return the file path the entry text must be written to.

    ENTRY_OUT may point at a file (write it directly) or at a
    directory (write entry.txt inside it). With nothing set, fall
    back to the conventional /output/entry.txt path.
    """
    target = (raw_out or "").strip() or "/output/entry.txt"
    if os.path.isdir(target) or target.endswith(os.sep):
        return os.path.join(target, "entry.txt")
    return target


def validate_line(line):
    """Check the entry against the bounty's gate and report its size.

    The gate needs UTF-8 text of 1 to 200 characters, not only
    whitespace, on a single line. Returns the cleaned line or raises.
    """
    cleaned = " ".join(line.split())
    if not cleaned:
        raise ValueError("entry is empty")
    if len(cleaned) > MAX_CHARS:
        raise ValueError(
            f"entry is {len(cleaned)} chars, over the {MAX_CHARS} limit"
        )
    if "\n" in cleaned:
        raise ValueError("entry must be a single line")
    return cleaned


def main():
    try:
        line = validate_line(ENTRY_LINE)
    except ValueError as problem:
        print(f"invalid entry: {problem}", file=sys.stderr)
        return 1

    dest = resolve_entry_path(os.environ.get("ENTRY_OUT"))
    parent = os.path.dirname(dest)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(dest, "w", encoding="utf-8") as handle:
        handle.write(line + "\n")

    print(line)
    print(f"[entry: {len(line)} chars]", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
