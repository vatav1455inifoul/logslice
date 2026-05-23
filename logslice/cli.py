"""Command-line entry point for logslice."""

import sys
from pathlib import Path

import click

from logslice.parser import parse_user_datetime
from logslice.slicer import slice_log, count_lines


@click.command()
@click.argument("logfile", type=click.Path(exists=True, dir_okay=False))
@click.option("-s", "--start", default=None, help="Start datetime (inclusive).")
@click.option("-e", "--end", default=None, help="End datetime (inclusive).")
@click.option(
    "--invert", is_flag=True, default=False,
    help="Output lines OUTSIDE the given range."
)
@click.option(
    "--count", is_flag=True, default=False,
    help="Print only the number of matching lines."
)
@click.option("-o", "--output", default=None, help="Write output to this file.")
def main(logfile, start, end, invert, count, output):
    """Extract a time-ranged slice from LOGFILE."""
    start_dt = parse_user_datetime(start) if start else None
    end_dt = parse_user_datetime(end) if end else None

    out_stream = open(output, "w", encoding="utf-8") if output else sys.stdout

    try:
        with open(logfile, "r", encoding="utf-8", errors="replace") as fh:
            if count:
                n = count_lines(fh, start=start_dt, end=end_dt)
                click.echo(n, file=out_stream)
            else:
                for line in slice_log(fh, start=start_dt, end=end_dt, invert=invert):
                    out_stream.write(line)
    except ValueError as exc:
        click.echo(f"Error: {exc}", err=True)
        sys.exit(1)
    finally:
        if output and out_stream is not sys.stdout:
            out_stream.close()


if __name__ == "__main__":
    main()
