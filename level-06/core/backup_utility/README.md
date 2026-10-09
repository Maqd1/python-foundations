# Backup Utility

A Python utility for creating, verifying, restoring, and managing file and directory backups.

## Features

- Multiple source files and directories.
- Multiple backup destinations.
- Full, incremental, and differential backups.
- Include and exclude file patterns.
- Optional ZIP compression.
- AES-256-GCM encryption and legacy Fernet decryption support.
- SHA-256 integrity verification and backup manifests.
- Safe archive restoration checks.
- Chain-aware retention cleanup.
- Structured logs and JSON reports.
- Scheduled backups.
- Optional SMTP email notifications.

## Requirements

- Python
- `cryptography`
- `APScheduler`

See `requirements.txt` for the pinned dependency versions.

## Installation

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Configuration

Backup jobs use a Python dictionary. Common settings include:

| Setting | Purpose |
|---|---|
|---|---|
| `job_name` | Name of the backup job |
| `sources` | Files or directories to back up |
| `destinations` | Destination directories |
| `type` | `full`, `incremental`, or `differential` |
| `password` | Optional encryption password |
| `compress` | Whether to compress backup data |
| `throttle_kb` | Optional transfer throttling |
| `retention_days` | Retention period for eligible backup chains |
| `include_patterns` | Patterns for files to include |
| `exclude_patterns` | Patterns for files to exclude |
| `email_notifications` | Whether email notifications are enabled |
| `email_to` | Notification recipients |

Check `backup_utility.py` for the exact supported options and defaults.

## Running a Backup

The `run_backup_job(config)` function in `backup_utility.py` returns a Boolean indicating whether the job succeeded.

Example:

```python
from backup_utility import run_backup_job

config = {
    "job_name": "Example_Backup",
    "sources": ["sample_data"],
    "destinations": ["./backups"],
    "type": "full",
    "compress": True,
    "retention_days": 30,
}

success = run_backup_job(config)
print("Backup successful." if success else "Backup failed.")
```

Add a suitable `password` setting when encryption is required.

## Scheduled Backups

Scheduled jobs are configured in `backup_schedule.json` and managed by `backup_scheduler.py`.

Start the scheduler:

```bash
python backup_scheduler.py
```

The scheduler must remain running for scheduled jobs to execute. Review source paths, destinations, and schedules before starting it.

## Email Notifications

Email notifications are optional. Add these settings to a backup job:

```python
{
    "email_notifications": True,
    "email_to": ["recipient@example.com"],
}
```

Configure SMTP through environment variables:

```bash
export BACKUP_SMTP_HOST="smtp.example.com"
export BACKUP_SMTP_PORT="587"
export BACKUP_SMTP_USER="sender@example.com"
export BACKUP_SMTP_PASSWORD="your-app-password"
export BACKUP_EMAIL_FROM="sender@example.com"
```

The utility supports STARTTLS on port `587` and implicit TLS on port `465`.

Use your provider's SMTP settings. Where possible, use an app-specific password. Never commit credentials or other secrets to version control.

## Logs and Reports

- `backup.log` records backup events.
- `reports/` stores JSON backup reports.
- `scheduler_runs.log` records scheduler execution results.

These are runtime outputs and generally should not be committed.

## Data Safety

- Keep backups separate from the original source files.
- Test restoration regularly.
- Keep encryption passwords safe; losing one can make encrypted backups unrecoverable.
- Protect backup destinations and SMTP credentials.
- Review retention settings before enabling automated cleanup.
- Test with non-critical files before relying on the utility for important data.

## Project Structure

```text
backup_utility/
├── backup_utility.py
├── backup_scheduler.py
├── backup_schedule.json
├── requirements.txt
├── README.md
├── sample_data/
└── reports/  # Generated at runtime
```

Additional files and directories may be created during execution and testing.

## Limitations

- Scheduled jobs run only while the scheduler process is running.
- Email delivery depends on valid SMTP configuration and provider availability.
- Backup destinations must be accessible to the running process.
- A successful backup does not replace independent restoration testing.

## License

No license has been specified for this project yet.
