"""Statistics collection for log slicing operations."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class SliceStats:
    """Holds runtime statistics for a single logslice run."""

    total_lines_read: int = 0
    lines_matched: int = 0
    lines_filtered: int = 0
    lines_highlighted: int = 0
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    first_matched_ts: Optional[str] = None
    last_matched_ts: Optional[str] = None
    source_file: str = ""

    def record_line(self, matched: bool, filtered: bool = False) -> None:
        """Update counters for each line processed."""
        self.total_lines_read += 1
        if matched:
            self.lines_matched += 1
        if filtered:
            self.lines_filtered += 1

    @property
    def elapsed_seconds(self) -> Optional[float]:
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return None

    @property
    def match_rate(self) -> float:
        if self.total_lines_read == 0:
            return 0.0
        return self.lines_matched / self.total_lines_read


def build_stats(source_file: str) -> SliceStats:
    """Create a new SliceStats instance stamped with the current time."""
    return SliceStats(source_file=source_file, start_time=datetime.now())


def finalise_stats(stats: SliceStats) -> SliceStats:
    """Stamp the end time and return the same stats object."""
    stats.end_time = datetime.now()
    return stats


def format_stats(stats: SliceStats) -> str:
    """Return a human-readable summary string."""
    lines = [
        f"Source      : {stats.source_file or '<stdin>'}",
        f"Lines read  : {stats.total_lines_read}",
        f"Lines matched: {stats.lines_matched}",
        f"Lines filtered: {stats.lines_filtered}",
        f"Match rate  : {stats.match_rate:.1%}",
    ]
    if stats.elapsed_seconds is not None:
        lines.append(f"Elapsed     : {stats.elapsed_seconds:.3f}s")
    if stats.first_matched_ts:
        lines.append(f"First match : {stats.first_matched_ts}")
    if stats.last_matched_ts:
        lines.append(f"Last match  : {stats.last_matched_ts}")
    return "\n".join(lines)
