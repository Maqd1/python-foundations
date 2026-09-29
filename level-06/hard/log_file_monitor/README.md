# Log File Monitor

A command-line log monitoring utility that analyzes application logs, tracks error statistics, rotates large log files, compresses old logs, and supports real-time monitoring.

## Features

- Reads log files line by line for memory-efficient analysis
- Parses:
  - Timestamps
  - INFO messages
  - WARNING messages
  - ERROR messages
- Calculates:
  - Total log entries
  - Log-level counts
  - Log-level percentages
  - Error count
  - Error rate
  - Top error messages
  - Last-24-hour timeline
- Detects high error rates
- Automatically rotates logs when they exceed 10 MB
- Compresses rotated logs using gzip
- Maintains three compressed log generations
- Removes the oldest rotation when necessary
- Supports real-time log monitoring with `tail`
- Supports forced rotation for testing
- Supports optional email alerts through SMTP configuration

## Log Format

The monitor expects log entries in this format:

```text
YYYY-MM-DD HH:MM:SS LEVEL Message
```

Example:

2026-09-29 08:15:23 INFO Application started
2026-09-29 08:17:45 WARNING API response slow
2026-09-29 08:18:12 ERROR Database connection failed

Supported levels:

INFO
WARNING
ERROR
Usage
Analyze a log
python log_monitor.py analyze application.log

Example output:

📊 STATISTICS:
INFO: 4 (40.0%)
WARNING: 2 (20.0%)
ERROR: 4 (40.0%)

⏰ Timeline (Last 24h):
INFO    🟢 4
WARNING 🟡 2
ERROR   🔴 4

🚨 TOP ERRORS:
1. Database connection failed: 2 times
2. Connection timeout: 2 times
Real-time monitoring
python log_monitor.py tail application.log

The program waits for new entries and displays them as they are appended to the log.

Press:

Ctrl+C

to stop monitoring.

Create a sample log
python log_monitor.py sample application.log

This creates a sample log containing INFO, WARNING, and ERROR entries for testing.

Force log rotation
python log_monitor.py rotate application.log

The rotate command forces rotation even when the log is below 10 MB. This is useful for testing.

Log Rotation

Normal automatic rotation occurs when the active log exceeds:

10 MB

Rotated logs are compressed using gzip.

The rotation structure is:

application.log
application.log.1.gz
application.log.2.gz
application.log.3.gz

When another rotation occurs:

application.log.3.gz

is removed.

The remaining rotations move upward:

.2.gz → .3.gz
.1.gz → .2.gz
current → .1.gz

A new empty application.log is then created.

Email Alerts

Email alerts are optional.

The program can send an alert when the error rate reaches the configured threshold.

The default threshold is:

5%

SMTP settings are read from environment variables:

SMTP_HOST
SMTP_PORT
SMTP_USERNAME
SMTP_PASSWORD
ALERT_FROM
ALERT_TO

Example:

export SMTP_HOST="smtp.example.com"
export SMTP_PORT="587"
export SMTP_USERNAME="username"
export SMTP_PASSWORD="password"
export ALERT_FROM="alerts@example.com"
export ALERT_TO="admin@example.com"

If SMTP configuration is incomplete, the program continues normally and reports that the email alert was not sent.

Memory Efficiency

Log analysis processes the file one line at a time.

Instead of loading the entire log into memory:

log file
    ↓
all lines
    ↓
Python list
    ↓
analyze

the monitor uses:

log file
    ↓
one line
    ↓
parse
    ↓
update statistics
    ↓
discard line
    ↓
next line

This keeps memory usage much lower when processing large log files.

Concepts Practiced
File handling
Reading files line by line
Regular expressions
datetime
Counter
Dictionaries
Functions
Command-line arguments
Path
File rotation
Gzip compression
Environment variables
SMTP
Exception handling
Real-time file monitoring
Streaming data processing
Memory-efficient algorithms
Project Structure
log_file_monitor/
├── README.md
└── log_monitor.py
Testing

The project was tested for:

Log parsing
Statistics calculation
Error frequency detection
Last-24-hour timeline
High error-rate detection
Missing log files
Invalid log entries
Real-time monitoring
Gzip compression
Multiple log rotations
Three-generation rotation limit
Forced rotation
Python compilation

Then run:

```bash
python -m py_compile log_monitor.py
rm -rf __pycache__