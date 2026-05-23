"""Tests for logslice.slicer."""

import io
from datetime import datetime

from logslice.slicer import slice_log, count_lines

SAMPLE_LOG = """2024-01-10 08:00:00 INFO  boot sequence started
2024-01-10 09:00:00 INFO  service alpha ready
2024-01-10 10:00:00 WARN  high memory usage
    at com.example.MemCheck.run(MemCheck.java:55)
2024-01-10 11:00:00 ERROR connection refused
2024-01-10 12:00:00 INFO  recovered
"""


def _stream(text=SAMPLE_LOG):
    return io.StringIO(text)


class TestSliceLog:
    def test_no_bounds_returns_all(self):
        lines = list(slice_log(_stream()))
        assert len(lines) == 6  # 5 timestamped + 1 continuation

    def test_start_bound(self):
        start = datetime(2024, 1, 10, 10, 0, 0)
        lines = list(slice_log(_stream(), start=start))
        assert len(lines) == 4  # WARN + continuation + ERROR + INFO

    def test_end_bound(self):
        end = datetime(2024, 1, 10, 9, 0, 0)
        lines = list(slice_log(_stream(), end=end))
        assert len(lines) == 2

    def test_start_and_end(self):
        start = datetime(2024, 1, 10, 9, 0, 0)
        end = datetime(2024, 1, 10, 10, 0, 0)
        lines = list(slice_log(_stream(), start=start, end=end))
        # 09:00 line + 10:00 line + continuation
        assert len(lines) == 3

    def test_invert(self):
        start = datetime(2024, 1, 10, 10, 0, 0)
        end = datetime(2024, 1, 10, 11, 0, 0)
        lines = list(slice_log(_stream(), start=start, end=end, invert=True))
        texts = "".join(lines)
        assert "08:00:00" in texts
        assert "12:00:00" in texts
        assert "10:00:00" not in texts

    def test_continuation_line_follows_match(self):
        start = datetime(2024, 1, 10, 10, 0, 0)
        end = datetime(2024, 1, 10, 10, 0, 0)
        lines = list(slice_log(_stream(), start=start, end=end))
        assert any("MemCheck" in l for l in lines)


class TestCountLines:
    def test_count(self):
        start = datetime(2024, 1, 10, 11, 0, 0)
        assert count_lines(_stream(), start=start) == 2
