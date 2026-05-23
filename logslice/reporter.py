"""Reporter: writes stats output to stderr or a file."""

import sys
from typing import IO, Optional

from logslice.stats import SliceStats, format_stats


_SEPARATOR = "-" * 40


def report_stats(
    stats: SliceStats,
    dest: Optional[IO[str]] = None,
    *,
    show_separator: bool = True,
) -> None:
    """
    Print formatted statistics to *dest* (defaults to stderr).

    Parameters
    ----------
    stats:
        Populated :class:`SliceStats` instance.
    dest:
        File-like object to write to.  Defaults to ``sys.stderr``.
    show_separator:
        Whether to print a dashed separator line before the stats block.
    """
    out = dest if dest is not None else sys.stderr
    if show_separator:
        out.write(_SEPARATOR + "\n")
    out.write(format_stats(stats) + "\n")


def maybe_report(
    stats: SliceStats,
    verbose: bool,
    dest: Optional[IO[str]] = None,
) -> None:
    """Only call :func:`report_stats` when *verbose* is True."""
    if verbose:
        report_stats(stats, dest=dest)
