"""Tests for logslice.formatter."""

import io
import json
import pytest

from logslice.formatter import format_lines, print_summary, SUPPORTED_FORMATS


SAMPLE_LINES = [
    "2024-01-01 00:00:01 INFO  server started\n",
    "2024-01-01 00:00:02 DEBUG request received\n",
    "2024-01-01 00:00:03 ERROR something failed\n",
]


def _buf():
    return io.StringIO()


class TestFormatLines:
    def test_plain_writes_all_lines(self):
        out = _buf()
        count = format_lines(iter(SAMPLE_LINES), fmt="plain", output=out)
        assert count == 3
        assert out.getvalue() == "".join(SAMPLE_LINES)

    def test_plain_adds_newline_if_missing(self):
        out = _buf()
        format_lines(iter(["no newline"]), fmt="plain", output=out)
        assert out.getvalue().endswith("\n")

    def test_numbered_prefixes_line_numbers(self):
        out = _buf()
        count = format_lines(iter(SAMPLE_LINES), fmt="numbered", output=out)
        lines = out.getvalue().splitlines()
        assert count == 3
        assert lines[0].startswith("     1  ")
        assert lines[2].startswith("     3  ")

    def test_json_produces_valid_json(self):
        out = _buf()
        count = format_lines(iter(SAMPLE_LINES), fmt="json", output=out)
        assert count == 3
        parsed = json.loads(out.getvalue())
        assert isinstance(parsed, list)
        assert len(parsed) == 3
        assert "INFO" in parsed[0]

    def test_json_empty_input(self):
        out = _buf()
        count = format_lines(iter([]), fmt="json", output=out)
        assert count == 0
        assert json.loads(out.getvalue()) == []

    def test_unsupported_format_raises(self):
        with pytest.raises(ValueError, match="Unsupported format"):
            format_lines(iter(SAMPLE_LINES), fmt="xml")

    def test_supported_formats_constant(self):
        assert "plain" in SUPPORTED_FORMATS
        assert "numbered" in SUPPORTED_FORMATS
        assert "json" in SUPPORTED_FORMATS


class TestPrintSummary:
    def test_singular_line(self):
        err = _buf()
        print_summary(1, output=err)
        assert "1 line matched" in err.getvalue()

    def test_plural_lines(self):
        err = _buf()
        print_summary(42, output=err)
        assert "42 lines matched" in err.getvalue()

    def test_zero_lines(self):
        err = _buf()
        print_summary(0, output=err)
        assert "0 lines matched" in err.getvalue()
