"""Compose slicer, filter, and formatter into a single processing pipeline."""

from typing import IO, Iterable, Iterator, Optional

from logslice.filter import filter_lines, keyword_filter
from logslice.formatter import format_lines, print_summary
from logslice.highlighter import highlight_lines
from logslice.slicer import slice_log


def run_pipeline(
    source: Iterable[str],
    *,
    start: Optional[str] = None,
    end: Optional[str] = None,
    include_pattern: Optional[str] = None,
    exclude_pattern: Optional[str] = None,
    keywords: Optional[list] = None,
    ignore_case: bool = False,
    numbered: bool = False,
    colour: bool = False,
    show_summary: bool = False,
    output: IO[str],
) -> int:
    """Run the full log-processing pipeline and write results to *output*.

    Steps:
        1. Slice lines by time range (start / end).
        2. Apply regex include / exclude filters.
        3. Apply keyword filter if keywords are provided.
        4. Optionally highlight lines by severity.
        5. Write formatted lines to *output*.
        6. Optionally print a summary line.

    Returns:
        Number of lines written.
    """
    stream: Iterator[str] = slice_log(source, start=start, end=end)

    stream = filter_lines(
        stream,
        include_pattern=include_pattern,
        exclude_pattern=exclude_pattern,
        ignore_case=ignore_case,
    )

    if keywords:
        stream = keyword_filter(stream, keywords, ignore_case=ignore_case)

    if colour:
        stream = highlight_lines(stream)

    count = format_lines(stream, output=output, numbered=numbered)

    if show_summary:
        print_summary(count, output=output)

    return count
