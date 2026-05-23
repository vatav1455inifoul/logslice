"""Tests for logslice.parser."""

from datetime import datetime

import pytest

from logslice.parser import extract_timestamp, parse_user_datetime


class TestExtractTimestamp:
    def test_iso8601_with_T(self):
        line = "2024-03-10T08:22:01 INFO server started"
        assert extract_timestamp(line) == datetime(2024, 3, 10, 8, 22, 1)

    def test_iso_with_space(self):
        line = "2024-03-10 08:22:01.456 ERROR disk full"
        assert extract_timestamp(line) == datetime(2024, 3, 10, 8, 22, 1)

    def test_apache_style(self):
        line = '127.0.0.1 - - [15/Jan/2024:13:45:00 +0000] "GET / HTTP/1.1"'
        result = extract_timestamp(line)
        assert result == datetime(2024, 1, 15, 13, 45, 0)

    def test_no_timestamp_returns_none(self):
        line = "    at com.example.App.main(App.java:42)"
        assert extract_timestamp(line) is None

    def test_syslog_style(self):
        line = "Jan  5 09:01:33 myhost sshd[1234]: Accepted"
        result = extract_timestamp(line)
        assert result is not None
        assert result.hour == 9
        assert result.minute == 1


class TestParseUserDatetime:
    def test_full_iso(self):
        assert parse_user_datetime("2024-06-01T12:00:00") == datetime(2024, 6, 1, 12, 0, 0)

    def test_date_only(self):
        assert parse_user_datetime("2024-06-01") == datetime(2024, 6, 1, 0, 0, 0)

    def test_space_separator(self):
        assert parse_user_datetime("2024-06-01 15:30") == datetime(2024, 6, 1, 15, 30)

    def test_invalid_raises(self):
        with pytest.raises(ValueError, match="Cannot parse datetime"):
            parse_user_datetime("not-a-date")
