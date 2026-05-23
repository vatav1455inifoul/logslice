"""Keyword and regex filtering for log lines."""

import re
from typing import Iterable, Iterator, Optional


def compile_pattern(pattern: str, ignore_case: bool = False) -> re.Pattern:
    """Compile a regex pattern with optional case-insensitivity."""
    flags = re.IGNORECASE if ignore_case else 0
    try:
        return re.compile(pattern, flags)
    except re.error as exc:
        raise ValueError(f"Invalid regex pattern {pattern!r}: {exc}") from exc


def filter_lines(
    lines: Iterable[str],
    include_pattern: Optional[str] = None,
    exclude_pattern: Optional[str] = None,
    ignore_case: bool = False,
) -> Iterator[str]:
    """Yield lines that match include_pattern and do not match exclude_pattern.

    Args:
        lines: Iterable of log line strings.
        include_pattern: If given, only lines matching this regex are kept.
        exclude_pattern: If given, lines matching this regex are dropped.
        ignore_case: Apply case-insensitive matching to both patterns.

    Yields:
        Filtered log lines.
    """
    inc_re = compile_pattern(include_pattern, ignore_case) if include_pattern else None
    exc_re = compile_pattern(exclude_pattern, ignore_case) if exclude_pattern else None

    for line in lines:
        if inc_re and not inc_re.search(line):
            continue
        if exc_re and exc_re.search(line):
            continue
        yield line


def keyword_filter(
    lines: Iterable[str],
    keywords: Iterable[str],
    ignore_case: bool = False,
) -> Iterator[str]:
    """Yield lines that contain at least one of the given keywords.

    Args:
        lines: Iterable of log line strings.
        keywords: Plain-text keywords to search for.
        ignore_case: Compare keywords case-insensitively.

    Yields:
        Lines containing at least one keyword.
    """
    kw_list = [
        kw.lower() if ignore_case else kw for kw in keywords
    ]
    if not kw_list:
        yield from lines
        return

    for line in lines:
        haystack = line.lower() if ignore_case else line
        if any(kw in haystack for kw in kw_list):
            yield line
