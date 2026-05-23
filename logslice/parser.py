"""Timestamp parsing utilities for logslice."""

import re
from datetime import datetime
from typing import Optional

# Common log timestamp patterns
TIMESTAMP_PATTERNS = [
    # ISO 8601: 2024-01-15T13:45:00
    (r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})?)', '%Y-%m-%dT%H:%M:%S'),
    # ISO with space: 2024-01-15 13:45:00
    (r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}(?:\.\d+)?)', '%Y-%m-%d %H:%M:%S'),
    # Apache/nginx: 15/Jan/2024:13:45:00
    (r'(\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2})', '%d/%b/%Y:%H:%M:%S'),
    # Syslog: Jan 15 13:45:00
    (r'(\w{3}\s+\d{1,2} \d{2}:\d{2}:\d{2})', '%b %d %H:%M:%S'),
]


def extract_timestamp(line: str) -> Optional[datetime]:
    """Extract the first recognizable timestamp from a log line."""
    for pattern, fmt in TIMESTAMP_PATTERNS:
        match = re.search(pattern, line)
        if match:
            raw = match.group(1)
            # Strip fractional seconds and timezone for parsing
            clean = re.sub(r'\.\d+', '', raw)
            clean = re.sub(r'(Z|[+-]\d{2}:?\d{2})$', '', clean)
            try:
                return datetime.strptime(clean, fmt)
            except ValueError:
                continue
    return None


def parse_user_datetime(value: str) -> datetime:
    """Parse a user-supplied datetime string into a datetime object."""
    formats = [
        '%Y-%m-%dT%H:%M:%S',
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%dT%H:%M',
        '%Y-%m-%d %H:%M',
        '%Y-%m-%d',
    ]
    for fmt in formats:
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    raise ValueError(
        f"Cannot parse datetime: '{value}'. "
        "Expected formats like '2024-01-15 13:45:00' or '2024-01-15T13:45'"
    )
