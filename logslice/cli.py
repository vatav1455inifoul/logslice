"""Command-line interface for logslice."""

import argparse
import sys

from logslice.parser import parse_user_datetime
from logslice.slicer import slice_log
from logslice.formatter import format_lines, print_summary, SUPPORTED_FORMATS


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="logslice",
        description="Extract time-ranged slices from large log files.",
    )
    p.add_argument("file", nargs="?", help="Log file to read (default: stdin)")
    p.add_argument("-s", "--start", metavar="DATETIME", help="Start of time range (inclusive)")
    p.add_argument("-e", "--end", metavar="DATETIME", help="End of time range (inclusive)")
    p.add_argument(
        "-f",
        "--format",
        choices=SUPPORTED_FORMATS,
        default="plain",
        help="Output format (default: plain)",
    )
    p.add_argument(
        "--summary",
        action="store_true",
        help="Print matched line count to stderr after output",
    )
    return p


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    start_dt = None
    end_dt = None

    try:
        if args.start:
            start_dt = parse_user_datetime(args.start)
        if args.end:
            end_dt = parse_user_datetime(args.end)
    except ValueError as exc:
        print(f"logslice: error parsing datetime — {exc}", file=sys.stderr)
        return 2

    try:
        if args.file:
            fh = open(args.file, "r", encoding="utf-8", errors="replace")
        else:
            fh = sys.stdin

        with fh if args.file else _nullctx(fh):
            matched = slice_log(fh, start=start_dt, end=end_dt)
            count = format_lines(matched, fmt=args.format)

    except FileNotFoundError:
        print(f"logslice: file not found — {args.file}", file=sys.stderr)
        return 1
    except BrokenPipeError:
        pass

    if args.summary:
        print_summary(count)

    return 0


class _nullctx:
    """No-op context manager for wrapping already-open streams."""

    def __init__(self, obj):
        self._obj = obj

    def __enter__(self):
        return self._obj

    def __exit__(self, *_):
        pass


if __name__ == "__main__":
    sys.exit(main())
