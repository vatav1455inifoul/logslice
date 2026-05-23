"""Tests for logslice.highlighter."""

import io
import pytest
from logslice.highlighter import (
    highlight_line,
    highlight_lines,
    _supports_colour,
    _RESET,
    _RED,
    _YELLOW,
    _GREEN,
    _CYAN,
    _BOLD,
)


class TestHighlightLine:
    def test_error_keyword_coloured_red_bold(self):
        result = highlight_line("ERROR: something went wrong")
        assert _RED in result
        assert _BOLD in result
        assert _RESET in result

    def test_critical_coloured(self):
        result = highlight_line("CRITICAL failure detected")
        assert _RED in result

    def test_warning_coloured_yellow(self):
        result = highlight_line("WARNING: disk space low")
        assert _YELLOW in result

    def test_info_coloured_green(self):
        result = highlight_line("INFO starting service")
        assert _GREEN in result

    def test_debug_coloured_green(self):
        result = highlight_line("DEBUG value=42")
        assert _GREEN in result

    def test_iso_timestamp_coloured_cyan(self):
        result = highlight_line("2024-01-15T08:30:00 some event")
        assert _CYAN in result

    def test_apache_timestamp_coloured_cyan(self):
        result = highlight_line("10/Oct/2000:13:55:36 GET /index.html")
        assert _CYAN in result

    def test_plain_line_unchanged_content(self):
        line = "nothing special here"
        result = highlight_line(line)
        # Original text still present
        assert "nothing special here" in result

    def test_no_extra_escapes_on_plain_line(self):
        line = "nothing special here"
        result = highlight_line(line)
        assert _RED not in result
        assert _YELLOW not in result
        assert _CYAN not in result


class TestHighlightLines:
    def test_force_applies_colour(self):
        lines = ["ERROR boom", "INFO ok"]
        result = list(highlight_lines(lines, force=True))
        assert _RED in result[0]
        assert _GREEN in result[1]

    def test_non_tty_stream_no_colour_by_default(self):
        stream = io.StringIO()  # not a TTY
        lines = ["ERROR boom"]
        result = list(highlight_lines(lines, stream=stream))
        assert result == ["ERROR boom"]

    def test_force_overrides_non_tty(self):
        stream = io.StringIO()
        lines = ["WARNING watch out"]
        result = list(highlight_lines(lines, stream=stream, force=True))
        assert _YELLOW in result[0]

    def test_empty_input_yields_nothing(self):
        assert list(highlight_lines([], force=True)) == []


class TestSupportsColour:
    def test_string_io_not_a_tty(self):
        assert _supports_colour(io.StringIO()) is False

    def test_fake_tty_returns_true(self):
        class FakeTTY:
            def isatty(self):
                return True
        assert _supports_colour(FakeTTY()) is True
