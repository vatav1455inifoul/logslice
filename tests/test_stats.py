"""Tests for logslice.stats."""

from datetime import datetime

import pytest

from logslice.stats import (
    SliceStats,
    build_stats,
    finalise_stats,
    format_stats,
)


class TestSliceStats:
    def test_initial_counters_are_zero(self):
        s = SliceStats()
        assert s.total_lines_read == 0
        assert s.lines_matched == 0
        assert s.lines_filtered == 0

    def test_record_line_matched(self):
        s = SliceStats()
        s.record_line(matched=True)
        assert s.total_lines_read == 1
        assert s.lines_matched == 1

    def test_record_line_not_matched(self):
        s = SliceStats()
        s.record_line(matched=False)
        assert s.total_lines_read == 1
        assert s.lines_matched == 0

    def test_record_line_filtered(self):
        s = SliceStats()
        s.record_line(matched=True, filtered=True)
        assert s.lines_filtered == 1

    def test_match_rate_no_lines(self):
        s = SliceStats()
        assert s.match_rate == 0.0

    def test_match_rate_half(self):
        s = SliceStats()
        s.record_line(matched=True)
        s.record_line(matched=False)
        assert s.match_rate == pytest.approx(0.5)

    def test_elapsed_none_without_timestamps(self):
        s = SliceStats()
        assert s.elapsed_seconds is None

    def test_elapsed_computed(self):
        s = SliceStats(
            start_time=datetime(2024, 1, 1, 0, 0, 0),
            end_time=datetime(2024, 1, 1, 0, 0, 2),
        )
        assert s.elapsed_seconds == pytest.approx(2.0)


def test_build_stats_sets_source_and_start():
    s = build_stats("app.log")
    assert s.source_file == "app.log"
    assert s.start_time is not None


def test_finalise_stats_sets_end_time():
    s = build_stats("app.log")
    finalise_stats(s)
    assert s.end_time is not None


def test_format_stats_contains_key_fields():
    s = SliceStats(
        source_file="app.log",
        total_lines_read=100,
        lines_matched=42,
        lines_filtered=3,
        start_time=datetime(2024, 1, 1, 0, 0, 0),
        end_time=datetime(2024, 1, 1, 0, 0, 1),
        first_matched_ts="2024-01-01 00:00:01",
        last_matched_ts="2024-01-01 00:00:59",
    )
    out = format_stats(s)
    assert "app.log" in out
    assert "100" in out
    assert "42" in out
    assert "42.0%" in out
    assert "1.000s" in out
    assert "2024-01-01 00:00:01" in out
