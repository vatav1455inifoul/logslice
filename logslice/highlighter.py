"""Optional ANSI colour highlighting for log output."""

import re
import sys

# ANSI escape codes
_RESET  = "\033[0m"
_RED    = "\033[31m"
_YELLOW = "\033[33m"
_GREEN  = "\033[32m"
_CYAN   = "\033[36m"
_BOLD   = "\033[1m"

# Patterns ordered from most- to least-specific
_RULES = [
    (re.compile(r'\b(ERROR|CRITICAL|FATAL)\b', re.IGNORECASE), _RED + _BOLD),
    (re.compile(r'\b(WARN(?:ING)?)\b',          re.IGNORECASE), _YELLOW),
    (re.compile(r'\b(INFO|DEBUG)\b',             re.IGNORECASE), _GREEN),
    # ISO-8601 / Apache-style timestamps
    (re.compile(
        r'(\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}'
        r'|\d{2}/\w+/\d{4}:\d{2}:\d{2}:\d{2})'
    ), _CYAN),
]


def _supports_colour(stream=None) -> bool:
    """Return True when *stream* (default stdout) looks like a colour terminal."""
    stream = stream or sys.stdout
    return hasattr(stream, 'isatty') and stream.isatty()


def highlight_line(line: str) -> str:
    """Apply ANSI colour codes to *line* and return the coloured string."""
    for pattern, colour in _RULES:
        line = pattern.sub(lambda m, c=colour: f"{c}{m.group(0)}{_RESET}", line)
    return line


def highlight_lines(lines, stream=None, *, force: bool = False):
    """Yield lines, highlighting each one if colour output is appropriate.

    Parameters
    ----------
    lines:  iterable of str
    stream: output stream used to detect TTY support (default stdout)
    force:  when True, apply highlighting even when not a TTY
    """
    use_colour = force or _supports_colour(stream)
    for line in lines:
        yield highlight_line(line) if use_colour else line
