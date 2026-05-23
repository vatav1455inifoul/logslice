"""Tests for logslice.reporter."""

import io

from logslice.stats import SliceStats
from logslice.reporter import report_stats, maybe_report


def _make_stats(**kwargs) -> SliceStats:
    return SliceStats(source_file="test.log", **kwargs)


class TestReportStats:
    def test_writes_to_provided_dest(self):
        buf = io.StringIO()
        s = _make_stats(total_lines_read=10, lines_matched=5)
        report_stats(s, dest=buf)
        output = buf.getvalue()
        assert "10" in output
        assert "5" in output

    def test_separator_shown_by_default(self):
        buf = io.StringIO()
        report_stats(_make_stats(), dest=buf)
        assert "---" in buf.getvalue()

    def test_separator_hidden_when_disabled(self):
        buf = io.StringIO()
        report_stats(_make_stats(), dest=buf, show_separator=False)
        assert "---" not in buf.getvalue()

    def test_source_file_in_output(self):
        buf = io.StringIO()
        report_stats(_make_stats(), dest=buf)
        assert "test.log" in buf.getvalue()


class TestMaybeReport:
    def test_does_not_write_when_not_verbose(self):
        buf = io.StringIO()
        maybe_report(_make_stats(), verbose=False, dest=buf)
        assert buf.getvalue() == ""

    def test_writes_when_verbose(self):
        buf = io.StringIO()
        maybe_report(_make_stats(total_lines_read=7), verbose=True, dest=buf)
        assert "7" in buf.getvalue()
