"""High-level pipeline that wires slicer, filter, formatter and stats together."""

from __future__ import annotations

import sys
from typing import IO, Optional

from logslice.filter import compile_pattern, filter_lines, keyword_filter
from logslice.formatter import format_lines, print_summary
from logslice.highlighter import highlight_lines
from logslice.parser import parse_user_datetime
from logslice.slicer import slice_log, count_lines
from logslice.stats import build_stats, finalise_stats
from logslice.reporter import maybe_report


def run_pipeline(
    source: IO[str],
    *,
    start: Optional[str] = None,
    end: Optional[str] = None,
    pattern: Optional[str] = None,
    keywords: Optional[list[str]] = None,
    ignore_case: bool = False,
    numbered: bool = False,
    colour: bool = False,
    verbose: bool = False,
    output: IO[str] = sys.stdout,
    source_name: str = "",
) -> int:
    """
    Execute the full logslice pipeline.

    Returns the number of lines written to *output*.
    """
    stats = build_stats(source_name)

    start_dt = parse_user_datetime(start) if start else None
    end_dt = parse_user_datetime(end) if end else None

    regex = compile_pattern(pattern, ignore_case=ignore_case) if pattern else None

    lines = slice_log(source, start=start_dt, end=end_dt)

    if regex is not None:
        lines = filter_lines(lines, regex)

    if keywords:
        lines = keyword_filter(lines, keywords, ignore_case=ignore_case)

    if colour:
        lines = highlight_lines(lines)

    written = format_lines(
        lines,
        output=output,
        numbered=numbered,
        stats=stats,
    )

    finalise_stats(stats)
    maybe_report(stats, verbose=verbose)

    return written
