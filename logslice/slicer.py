"""Core log slicing logic — streams lines within a time range."""

from datetime import datetime
from typing import Generator, Optional, TextIO

from logslice.parser import extract_timestamp


def slice_log(
    file: TextIO,
    start: Optional[datetime] = None,
    end: Optional[datetime] = None,
    invert: bool = False,
) -> Generator[str, None, None]:
    """
    Yield lines from *file* whose timestamps fall within [start, end].

    Lines with no detectable timestamp are included if they immediately
    follow a matching line (continuation lines, stack traces, etc.).

    Args:
        file:    An open, readable text stream.
        start:   Lower bound (inclusive). None means no lower bound.
        end:     Upper bound (inclusive). None means no upper bound.
        invert:  When True, yield lines *outside* the range instead.
    """
    in_range = False

    for line in file:
        ts = extract_timestamp(line)

        if ts is None:
            # Continuation line — inherit the current range state
            if in_range ^ invert:
                yield line
            continue

        # Determine whether this timestamped line is within range
        after_start = (start is None) or (ts >= start)
        before_end = (end is None) or (ts <= end)
        in_range = after_start and before_end

        if in_range ^ invert:
            yield line


def count_lines(
    file: TextIO,
    start: Optional[datetime] = None,
    end: Optional[datetime] = None,
) -> int:
    """Return the number of matching lines without printing them."""
    return sum(1 for _ in slice_log(file, start=start, end=end))
