import json
import time
from pathlib import Path
from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

CONFIG_FILE = Path("backup_schedule.json")


def load_config():
    if not CONFIG_FILE.exists():
        return {"jobs": []}

    with CONFIG_FILE.open("r", encoding="utf-8") as file:
        config = json.load(file)

    if not isinstance(config.get("jobs"), list):
        raise ValueError("Configuration must contain a jobs list.")

    return config


def save_config(config):
    with CONFIG_FILE.open("w", encoding="utf-8") as file:
        json.dump(config, file, indent=2)


def execute_backup(job):
    """Execute a scheduled backup and record its result."""
    from backup_utility import run_backup_job

    started_at = datetime.now().isoformat(timespec="seconds")
    job_name = job.get("job_name", "Unnamed_Backup")
    config = dict(job.get("backup_config", {}))
    config.setdefault("job_name", job_name)

    print(f"\\n[{started_at}] Running: {job_name}")

    result = {
        "job_name": job_name,
        "started_at": started_at,
        "finished_at": None,
        "status": "failed",
        "error": None,
    }

    try:
        success = run_backup_job(config)
        result["status"] = "success" if success is True else "failed"

    except Exception as exc:
        result["error"] = str(exc)
        print(f"[ERROR] Scheduled backup raised an exception: {exc}")

    finally:
        result["finished_at"] = datetime.now().isoformat(
            timespec="seconds"
        )

        log_path = Path(__file__).resolve().parent / "scheduler_runs.log"

        try:
            with log_path.open("a", encoding="utf-8") as file:
                file.write(json.dumps(result, ensure_ascii=False) + "\n")
        except OSError as exc:
            print(f"[ERROR] Could not write scheduler log: {exc}")

    if result["status"] == "success":
        print(f"[SUCCESS] Scheduled job completed: {job_name}")
    else:
        print(f"[ERROR] Scheduled job failed: {job_name}")

    return result["status"] == "success"


def build_trigger(job):
    frequency = job["frequency"].lower()
    hour = int(job.get("hour", 2))
    minute = int(job.get("minute", 0))

    if not 0 <= hour <= 23 or not 0 <= minute <= 59:
        raise ValueError("Hour must be 0–23 and minute must be 0–59.")

    if frequency == "daily":
        return CronTrigger(hour=hour, minute=minute)

    if frequency == "weekly":
        day = job.get("day_of_week", "mon").lower()
        return CronTrigger(day_of_week=day, hour=hour, minute=minute)

    if frequency == "monthly":
        day = int(job.get("day", 1))
        if not 1 <= day <= 28:
            raise ValueError("Monthly day must be between 1 and 28.")
        return CronTrigger(day=day, hour=hour, minute=minute)

    if frequency == "cron":
        expression = job.get("cron", {})
        return CronTrigger(
            minute=expression.get("minute", "0"),
            hour=expression.get("hour", "2"),
            day=expression.get("day", "*"),
            month=expression.get("month", "*"),
            day_of_week=expression.get("day_of_week", "*"),
        )

    raise ValueError(f"Unsupported frequency: {frequency}")


def main():
    config = load_config()
    jobs = config.get("jobs", [])

    if not jobs:
        print("No scheduled jobs found.")
        print(f"Create your schedule in: {CONFIG_FILE.resolve()}")
        return

    scheduler = BlockingScheduler()

    for job in jobs:
        trigger = build_trigger(job)
        scheduler.add_job(
            execute_backup,
            trigger=trigger,
            args=[job],
            id=job["job_name"],
            replace_existing=True,
            max_instances=1,
            coalesce=True,
        )
        print(f"Scheduled: {job['job_name']} ({job['frequency']})")

    print("Scheduler running. Press Ctrl+C to stop.")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("Scheduler stopped.")


if __name__ == "__main__":
    main()
