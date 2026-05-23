"""Output formatting utilities for logslice."""

import sys
from typing import Iterator, Optional, TextIO


DEFAULT_FORMAT = "plain"
SUPPORTED_FORMATS = ("plain", "numbered", "json")


def format_lines(
    lines: Iterator[str],
    fmt: str = DEFAULT_FORMAT,
    output: Optional[TextIO] = None,
) -> int:
    """Write formatted lines to output stream.

    Returns the number of lines written.
    """
    if fmt not in SUPPORTED_FORMATS:
        raise ValueError(f"Unsupported format '{fmt}'. Choose from: {SUPPORTED_FORMATS}")

    out = output or sys.stdout
    count = 0

    if fmt == "plain":
        for line in lines:
            out.write(line if line.endswith("\n") else line + "\n")
            count += 1

    elif fmt == "numbered":
        for i, line in enumerate(lines, start=1):
            stripped = line.rstrip("\n")
            out.write(f"{i:>6}  {stripped}\n")
            count += 1

    elif fmt == "json":
        import json

        out.write("[\n")
        buffer = []
        for line in lines:
            buffer.append(line.rstrip("\n"))
            count += 1
        for idx, entry in enumerate(buffer):
            comma = "," if idx < len(buffer) - 1 else ""
            out.write(f"  {json.dumps(entry)}{comma}\n")
        out.write("]\n")

    return count


def print_summary(count: int, output: Optional[TextIO] = None) -> None:
    """Print a short summary line to stderr (or provided stream)."""
    err = output or sys.stderr
    noun = "line" if count == 1 else "lines"
    err.write(f"logslice: {count} {noun} matched.\n")
