import gzip
import os
import re
import shutil
import smtplib
import sys
import time
from collections import Counter
from datetime import datetime, timedelta
from email.message import EmailMessage
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

MAX_LOG_SIZE = 10 * 1024 * 1024  # 10 MB
MAX_ROTATED_LOGS = 3
ERROR_RATE_THRESHOLD = 0.05  # 5%

LOG_PATTERN = re.compile(
    r"^(?P<timestamp>\S+ \S+)\s+"
    r"(?P<level>INFO|WARNING|ERROR)\s+"
    r"(?P<message>.*)$"
)


# ============================================================
# LOG PARSING
# ============================================================

def parse_log_line(line):
    """
    Parse one log line into timestamp, level and message.

    Expected format:

    2026-09-29 08:18:12 ERROR Database connection failed
    """

    match = LOG_PATTERN.match(line.strip())

    if not match:
        return None

    data = match.groupdict()

    try:
        data["timestamp"] = datetime.strptime(
            data["timestamp"],
            "%Y-%m-%d %H:%M:%S"
        )
    except ValueError:
        return None

    return data


# ============================================================
# FILE READING
# ============================================================

def read_log_file(filename):
    """
    Read a log file line by line.

    Returns:
        list[dict]: Parsed log entries.
    """

    entries = []

    with open(filename, "r", encoding="utf-8", errors="replace") as file:
        for line in file:
            entry = parse_log_line(line)

            if entry is not None:
                entries.append(entry)

    return entries


# ============================================================
# STATISTICS
# ============================================================

def calculate_statistics(log_file):
    level_counts = Counter()
    error_types = Counter()
    timeline = Counter()

    total_entries = 0
    error_count = 0

    now = datetime.now()
    last_24_hours = now - timedelta(hours=24)

    with open(
        log_file,
        "r",
        encoding="utf-8",
        errors="replace"
    ) as file:

        for line in file:
            entry = parse_log_line(line)

            if entry is None:
                continue

            total_entries += 1

            level = entry["level"]
            level_counts[level] += 1

            if level == "ERROR":
                error_count += 1
                error_types[entry["message"]] += 1

            if entry["timestamp"] >= last_24_hours:
                timeline[level] += 1

    error_rate = (
        error_count / total_entries
        if total_entries
        else 0
    )

    return {
        "total": total_entries,
        "levels": level_counts,
        "error_count": error_count,
        "error_types": error_types,
        "timeline": timeline,
        "error_rate": error_rate,
    }


# ============================================================
# DISPLAY STATISTICS
# ============================================================

def display_statistics(statistics):
    """
    Display human-readable log statistics.
    """

    total = statistics["total"]
    levels = statistics["levels"]

    print("\n📊 STATISTICS:")

    for level in ("INFO", "WARNING", "ERROR"):
        count = levels[level]

        percentage = (
            count / total * 100
            if total
            else 0
        )

        print(
            f"{level}: {count:,} "
            f"({percentage:.1f}%)"
        )

    print("\n⏰ Timeline (Last 24h):")

    for level, emoji in (
        ("INFO", "🟢"),
        ("WARNING", "🟡"),
        ("ERROR", "🔴"),
    ):
        count = statistics["timeline"][level]

        print(
            f"{level:<7} {emoji} {count:,}"
        )

    print("\n🚨 TOP ERRORS:")

    top_errors = statistics["error_types"].most_common(5)

    if not top_errors:
        print("No errors found.")
    else:
        for number, (message, count) in enumerate(
            top_errors,
            start=1
        ):
            print(
                f"{number}. {message}: {count:,} times"
            )

    error_rate = statistics["error_rate"] * 100

    if error_rate >= ERROR_RATE_THRESHOLD * 100:
        print("\n⚠️ HIGH ERROR RATE DETECTED!")

        print(
            f"Error rate: {error_rate:.1f}% "
            f"(Threshold: "
            f"{ERROR_RATE_THRESHOLD * 100:.0f}%)"
        )
    else:
        print(
            f"\nError rate: {error_rate:.1f}% "
            f"(Threshold: "
            f"{ERROR_RATE_THRESHOLD * 100:.0f}%)"
        )


# ============================================================
# LOG ROTATION
# ============================================================

def rotate_logs(log_file, force=False):
    """
    Rotate logs when the active log exceeds 10 MB.

    Example:

        application.log
        application.log.1.gz
        application.log.2.gz
        application.log.3.gz

    The oldest .3.gz is removed.
    """

    log_file = Path(log_file)

    if not log_file.exists():
        return False

    size = log_file.stat().st_size

    if size <= MAX_LOG_SIZE and not force:
        return False

    print("\n📁 Rotating logs...")

    oldest = log_file.with_name(
        f"{log_file.name}.{MAX_ROTATED_LOGS}.gz"
    )

    if oldest.exists():
        oldest.unlink()

        print(
            f"Removed oldest rotation: "
            f"{oldest.name}"
        )

    for number in range(
        MAX_ROTATED_LOGS - 1,
        0,
        -1
    ):
        current = log_file.with_name(
            f"{log_file.name}.{number}.gz"
        )

        new_name = log_file.with_name(
            f"{log_file.name}.{number + 1}.gz"
        )

        if current.exists():
            current.rename(new_name)

    temporary_file = log_file.with_suffix(
        log_file.suffix + ".tmp"
    )

    with open(log_file, "rb") as source:
        with gzip.open(
            temporary_file,
            "wb"
        ) as destination:
            shutil.copyfileobj(
                source,
                destination
            )

    rotated_file = log_file.with_name(
        f"{log_file.name}.1.gz"
    )

    temporary_file.rename(rotated_file)

    log_file.unlink()

    log_file.touch()

    print(
        f"{log_file.name} → "
        f"{rotated_file.name} (compressed)"
    )

    print(
        f"New log created: {log_file.name}"
    )

    print("✅ Log rotation complete")

    return True


# ============================================================
# EMAIL ALERTS
# ============================================================

def send_email_alert(subject, body):
    """
    Send an email alert using SMTP environment variables.

    Required environment variables:

        SMTP_HOST
        SMTP_PORT
        SMTP_USERNAME
        SMTP_PASSWORD
        ALERT_FROM
        ALERT_TO

    The function returns False if email configuration
    is incomplete.
    """

    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = os.getenv("SMTP_PORT")
    smtp_username = os.getenv("SMTP_USERNAME")
    smtp_password = os.getenv("SMTP_PASSWORD")
    alert_from = os.getenv("ALERT_FROM")
    alert_to = os.getenv("ALERT_TO")

    required = [
        smtp_host,
        smtp_port,
        smtp_username,
        smtp_password,
        alert_from,
        alert_to,
    ]

    if not all(required):
        print(
            "ℹ️ Email alert not sent: "
            "SMTP configuration is incomplete."
        )

        return False

    message = EmailMessage()

    message["Subject"] = subject
    message["From"] = alert_from
    message["To"] = alert_to

    message.set_content(body)

    try:
        with smtplib.SMTP(
            smtp_host,
            int(smtp_port),
            timeout=10
        ) as server:

            server.starttls()

            server.login(
                smtp_username,
                smtp_password
            )

            server.send_message(message)

    except Exception as error:
        print(
            f"❌ Email alert failed: {error}"
        )

        return False

    print("📧 Alert email sent!")

    return True


def check_alerts(log_file, statistics):
    """
    Check whether the error rate has crossed the threshold.
    """

    if statistics["error_rate"] < ERROR_RATE_THRESHOLD:
        return

    error_rate = statistics["error_rate"] * 100

    subject = "High Error Rate Detected"

    body = (
        f"Log file: {log_file}\n"
        f"Error rate: {error_rate:.2f}%\n"
        f"Threshold: "
        f"{ERROR_RATE_THRESHOLD * 100:.2f}%\n"
        f"Error count: "
        f"{statistics['error_count']}\n"
    )

    send_email_alert(subject, body)


# ============================================================
# REAL-TIME TAIL
# ============================================================

def follow_log(log_file):
    """
    Continuously monitor a log file like:

        tail -f application.log
    """

    log_file = Path(log_file)

    print("\n👀 REAL-TIME MONITORING")
    print(
        "Watching for new log entries..."
    )
    print("Press Ctrl+C to stop.\n")

    with open(
        log_file,
        "r",
        encoding="utf-8",
        errors="replace"
    ) as file:

        file.seek(0, 2)

        try:
            while True:
                line = file.readline()

                if not line:
                    time.sleep(0.5)
                    continue

                entry = parse_log_line(line)

                if entry is None:
                    continue

                timestamp = entry["timestamp"]
                level = entry["level"]
                message = entry["message"]

                if level == "ERROR":
                    emoji = "🔴"
                elif level == "WARNING":
                    emoji = "🟡"
                else:
                    emoji = "🟢"

                print(
                    f"{timestamp} "
                    f"{emoji} {level}: "
                    f"{message}"
                )

        except KeyboardInterrupt:
            print(
                "\n\n🛑 Real-time monitoring stopped."
            )


# ============================================================
# LOG FILE CREATION FOR TESTING
# ============================================================

def create_sample_log(log_file):
    """
    Create a small sample log for testing.
    """

    sample_entries = [
        "2026-09-29 08:15:23 INFO Application started",
        "2026-09-29 08:16:02 INFO User logged in",
        "2026-09-29 08:17:45 WARNING API response slow",
        "2026-09-29 08:18:12 ERROR Database connection failed",
        "2026-09-29 08:18:15 ERROR Database connection failed",
        "2026-09-29 08:19:03 ERROR Connection timeout",
        "2026-09-29 08:20:11 INFO User logged out",
        "2026-09-29 08:21:33 ERROR Connection timeout",
        "2026-09-29 08:22:44 WARNING API response slow",
        "2026-09-29 08:23:51 INFO Application running",
    ]

    with open(
        log_file,
        "w",
        encoding="utf-8"
    ) as file:

        for entry in sample_entries:
            file.write(entry + "\n")

    print(
        f"✅ Sample log created: {log_file}"
    )


# ============================================================
# MAIN ANALYSIS
# ============================================================

def analyze_log(log_file):
    """
    Analyze a log file.
    """

    log_file = Path(log_file)

    if not log_file.exists():
        print(
            f"❌ Log file not found: {log_file}"
        )
        return

    if not log_file.is_file():
        print(
            f"❌ Not a file: {log_file}"
        )
        return

    size = log_file.stat().st_size

    size_mb = size / (1024 * 1024)

    print("\n📋 LOG MONITOR 📋")
    print(
        f"Log file: {log_file}"
    )
    print(
        f"Size: {size_mb:.2f} MB"
    )

    statistics = calculate_statistics(log_file)

    print(
        f"Entries: {statistics['total']:,}"
        )

    display_statistics(
        statistics
    )

    check_alerts(
        log_file,
        statistics
    )

    rotated = rotate_logs(log_file)

    if rotated:
        print(
            "\n⚠️ The log was rotated because "
            "it exceeded 10 MB."
        )


# ============================================================
# COMMAND-LINE INTERFACE
# ============================================================

def main():
    if len(sys.argv) == 1:
        print("\n📋 LOG FILE MONITOR")
        print()
        print("Usage:")
        print(
            "  python log_monitor.py "
            "<log_file>"
        )
        print()
        print("Commands:")
        print(
            "  analyze <log_file> "
            "Analyze a log file"
        )
        print(
            "  tail <log_file> "
            "Monitor in real time"
        )
        print(
            "  sample <log_file> "
            "Create sample log"
        )
        print(
            "  rotate <log_file> "
            "Force rotation test"
        )
        return

    command = sys.argv[1].lower()

    if command == "analyze":

        if len(sys.argv) < 3:
            print(
                "❌ Please provide a log file."
            )
            return

        analyze_log(sys.argv[2])

    elif command == "tail":

        if len(sys.argv) < 3:
            print(
                "❌ Please provide a log file."
            )
            return

        log_file = Path(sys.argv[2])

        if not log_file.exists():
            print(
                f"❌ Log file not found: "
                f"{log_file}"
            )
            return

        follow_log(log_file)

    elif command == "sample":

        if len(sys.argv) < 3:
            print(
                "❌ Please provide a log filename."
            )
            return

        create_sample_log(
            sys.argv[2]
        )

    elif command == "rotate":

        if len(sys.argv) < 3:
            print(
                "❌ Please provide a log file."
            )
            return

        if rotate_logs(sys.argv[2], force=True):
            print(
                "✅ Forced rotation completed."
            )
        else:
            print(
                "ℹ️ Log is below 10 MB. "
                "No rotation needed."
            )

    else:
        print(
            f"❌ Unknown command: {command}"
        )


if __name__ == "__main__":
    main()

