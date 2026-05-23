# logslice

> Command-line utility to extract and filter time-ranged slices from large log files without loading them into memory.

---

## Installation

```bash
pip install logslice
```

Or install from source:

```bash
git clone https://github.com/yourname/logslice.git && cd logslice && pip install .
```

---

## Usage

```bash
logslice [OPTIONS] <logfile>
```

### Examples

Extract log entries between two timestamps:

```bash
logslice --start "2024-03-01 08:00:00" --end "2024-03-01 09:00:00" app.log
```

Filter by log level and write output to a file:

```bash
logslice --start "2024-03-01 08:00:00" --end "2024-03-01 09:00:00" --level ERROR app.log -o errors.log
```

Use a custom timestamp format:

```bash
logslice --start "2024-03-01 08:00:00" --end "2024-03-01 09:00:00" --fmt "%Y/%m/%d %H:%M:%S" app.log
```

### Options

| Flag | Description |
|------|-------------|
| `--start` | Start of the time range (inclusive) |
| `--end` | End of the time range (inclusive) |
| `--fmt` | Timestamp format string (default: `%Y-%m-%d %H:%M:%S`) |
| `--level` | Filter by log level (e.g. `ERROR`, `WARN`) |
| `-o, --output` | Write results to a file instead of stdout |

---

## Why logslice?

Large log files can be gigabytes in size. `logslice` uses binary search and streaming reads to locate and extract the relevant time range **without loading the entire file into memory**, making it fast and efficient even on constrained systems.

---

## License

This project is licensed under the [MIT License](LICENSE).