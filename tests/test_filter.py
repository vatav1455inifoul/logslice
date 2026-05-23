"""Tests for logslice.filter module."""

import pytest
from logslice.filter import compile_pattern, filter_lines, keyword_filter


LINES = [
    "2024-01-01 INFO  server started",
    "2024-01-01 DEBUG connection accepted from 10.0.0.1",
    "2024-01-01 ERROR failed to bind port 8080",
    "2024-01-01 WARNING disk usage at 90%",
    "2024-01-01 INFO  shutdown initiated",
]


class TestCompilePattern:
    def test_valid_pattern_compiles(self):
        p = compile_pattern(r"\d+")
        assert p.search("abc 123")

    def test_invalid_pattern_raises_value_error(self):
        with pytest.raises(ValueError, match="Invalid regex"):
            compile_pattern(r"[unclosed")

    def test_ignore_case_flag(self):
        p = compile_pattern("error", ignore_case=True)
        assert p.search("ERROR something")


class TestFilterLines:
    def test_no_patterns_returns_all(self):
        result = list(filter_lines(LINES))
        assert result == LINES

    def test_include_pattern_keeps_matches(self):
        result = list(filter_lines(LINES, include_pattern="ERROR"))
        assert len(result) == 1
        assert "ERROR" in result[0]

    def test_exclude_pattern_drops_matches(self):
        result = list(filter_lines(LINES, exclude_pattern="DEBUG"))
        assert all("DEBUG" not in line for line in result)
        assert len(result) == len(LINES) - 1

    def test_include_and_exclude_combined(self):
        result = list(
            filter_lines(LINES, include_pattern="INFO", exclude_pattern="shutdown")
        )
        assert len(result) == 1
        assert "started" in result[0]

    def test_ignore_case_include(self):
        result = list(filter_lines(LINES, include_pattern="error", ignore_case=True))
        assert len(result) == 1

    def test_ignore_case_exclude(self):
        result = list(filter_lines(LINES, exclude_pattern="info", ignore_case=True))
        assert all("INFO" not in line for line in result)


class TestKeywordFilter:
    def test_no_keywords_returns_all(self):
        result = list(keyword_filter(LINES, []))
        assert result == LINES

    def test_single_keyword_match(self):
        result = list(keyword_filter(LINES, ["ERROR"]))
        assert len(result) == 1

    def test_multiple_keywords_union(self):
        result = list(keyword_filter(LINES, ["ERROR", "WARNING"]))
        assert len(result) == 2

    def test_ignore_case_keyword(self):
        result = list(keyword_filter(LINES, ["error"], ignore_case=True))
        assert len(result) == 1
        assert "ERROR" in result[0]

    def test_no_match_returns_empty(self):
        result = list(keyword_filter(LINES, ["CRITICAL"]))
        assert result == []
