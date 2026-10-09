import os
import smtplib
from email.message import EmailMessage
import tempfile
import sys
import time
import json
import shutil
import zipfile
import hashlib
import fnmatch
from datetime import datetime, timedelta

try:
    import base64
    import secrets
    from cryptography.fernet import Fernet, InvalidToken
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.primitives import hashes
    CRYPTOGRAPHY_AVAILABLE = True
except ImportError:
    CRYPTOGRAPHY_AVAILABLE = False


# ============================================================
# ENCRYPTION HELPERS
# ============================================================

AES_MAGIC = b"MAQDAES1"
AES_SALT_SIZE = 16
AES_NONCE_SIZE = 12
AES_KEY_SIZE = 32
AES_KDF_ITERATIONS = 600_000


def derive_key(password, salt=None):
    """Derive a 256-bit key from a password using PBKDF2-HMAC-SHA256."""
    if not CRYPTOGRAPHY_AVAILABLE:
        raise RuntimeError("Encryption requires the cryptography package.")
    if not password:
        raise ValueError("A non-empty encryption password is required.")

    salt = salt or secrets.token_bytes(AES_SALT_SIZE)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=AES_KEY_SIZE,
        salt=salt,
        iterations=AES_KDF_ITERATIONS,
    )
    return kdf.derive(password.encode("utf-8")), salt


def encrypt_file(source_path, dest_path, password, throttle_kb=0):
    """Encrypt a file using authenticated AES-256-GCM."""
    if not CRYPTOGRAPHY_AVAILABLE:
        raise RuntimeError("Install cryptography to encrypt backups.")

    key, salt = derive_key(password)
    nonce = secrets.token_bytes(AES_NONCE_SIZE)

    with open(source_path, "rb") as source:
        plaintext = source.read()

    ciphertext = AESGCM(key).encrypt(nonce, plaintext, AES_MAGIC)

    with open(dest_path, "wb") as destination:
        destination.write(AES_MAGIC + salt + nonce + ciphertext)

    if throttle_kb > 0:
        time.sleep(len(plaintext) / (throttle_kb * 1024))


def decrypt_file(source_path, dest_path, password):
    """Decrypt AES-256-GCM backups and legacy Fernet backups."""
    if not CRYPTOGRAPHY_AVAILABLE:
        raise RuntimeError("Install cryptography to decrypt backups.")

    with open(source_path, "rb") as source:
        data = source.read()

    if data.startswith(AES_MAGIC):
        header_size = len(AES_MAGIC) + AES_SALT_SIZE + AES_NONCE_SIZE
        if len(data) < header_size + 16:
            raise ValueError("Encrypted backup is truncated.")

        offset = len(AES_MAGIC)
        salt = data[offset:offset + AES_SALT_SIZE]
        offset += AES_SALT_SIZE
        nonce = data[offset:offset + AES_NONCE_SIZE]
        ciphertext = data[header_size:]

        key, _ = derive_key(password, salt)
        plaintext = AESGCM(key).decrypt(nonce, ciphertext, AES_MAGIC)
    else:
        # Legacy format: SHA-256(password) -> Fernet key.
        legacy_key = base64.urlsafe_b64encode(
            hashlib.sha256(password.encode("utf-8")).digest()
        )
        try:
            plaintext = Fernet(legacy_key).decrypt(data)
        except InvalidToken as exc:
            raise ValueError(
                "Decryption failed: wrong password or corrupted backup."
            ) from exc

    with open(dest_path, "wb") as destination:
        destination.write(plaintext)


# ============================================================
# FILE SCANNER & PATTERN MATCHING
# ============================================================

def matches_pattern(filename, patterns):
    """Check if filename matches any glob pattern."""
    return any(fnmatch.fnmatch(filename, pat) for pat in patterns)


def format_bytes(size):
    """Format bytes into a human-readable size."""
    size = float(size)

    for unit in ("B", "KB", "MB", "GB", "TB", "PB"):
        if size < 1024 or unit == "PB":
            return f"{size:.2f} {unit}"
        size /= 1024

def calculate_file_hash(file_path, algorithm="sha256"):
    """Calculate a file's checksum in chunks."""
    digest = hashlib.new(algorithm)

    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)

    return digest.hexdigest()


def scan_source_directories(sources, include_patterns=None, exclude_patterns=None):
    """Scan and validate source paths, applying include/exclude patterns."""
    files_to_backup = []
    total_size = 0
    valid_sources = 0

    include_patterns = include_patterns or ["*"]
    exclude_patterns = exclude_patterns or []

    if not sources:
        raise ValueError("At least one source path is required.")

    for source in sources:
        src = os.path.abspath(os.path.expanduser(source))

        if not os.path.exists(src):
            print_error(f"Source path not found: {src}")
            continue

        valid_sources += 1

        if os.path.isfile(src):
            candidates = [(src, os.path.basename(src))]
        elif os.path.isdir(src):
            candidates = []
            for root, dirs, filenames in os.walk(src):
                dirs[:] = [
                    directory for directory in dirs
                    if not matches_pattern(directory, exclude_patterns)
                ]
                for filename in filenames:
                    full_path = os.path.join(root, filename)
                    relative_path = os.path.relpath(full_path, src)
                    candidates.append((full_path, relative_path))
        else:
            print_error(f"Unsupported source type: {src}")
            continue

        for full_path, relative_path in candidates:
            filename = os.path.basename(full_path)

            if not matches_pattern(filename, include_patterns):
                continue
            if matches_pattern(filename, exclude_patterns):
                continue

            try:
                size = os.path.getsize(full_path)
                mtime = os.path.getmtime(full_path)
                file_hash = calculate_file_hash(full_path)

                if not file_hash:
                    raise OSError("Could not calculate file hash.")

                files_to_backup.append({
                    "abs_path": full_path,
                    "rel_path": relative_path,
                    "size": size,
                    "mtime": mtime,
                    "hash": file_hash,
                })
                total_size += size
            except OSError as exc:
                print_error(f"Cannot read {full_path}: {exc}")

    if valid_sources == 0:
        raise ValueError("No valid source paths were found.")
    if not files_to_backup:
        raise ValueError("No files matched the backup patterns.")

    return files_to_backup, total_size


# ============================================================
# STATE TRACKING (For Incremental / Differential Backups)
# ============================================================

def load_destination_history(dest_dir):
    """Load backup execution history from destination metadata store."""
    history_file = os.path.join(dest_dir, ".backup_history.json")
    if os.path.exists(history_file):
        try:
            with open(history_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"backups": []}
    return {"backups": []}


def save_destination_history(dest_dir, history):
    """Save updated backup execution history."""
    history_file = os.path.join(dest_dir, ".backup_history.json")
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)


def load_backup_manifest(dest_dir, backup_record):
    """Load a backup manifest safely; return an empty list if unavailable."""
    manifest_path = os.path.join(
        dest_dir, backup_record.get("folder", ""), "manifest.json"
    )

    if not os.path.isfile(manifest_path):
        return []

    try:
        with open(manifest_path, "r", encoding="utf-8") as file:
            manifest = json.load(file)
        return manifest if isinstance(manifest, list) else []
    except (OSError, json.JSONDecodeError):
        return []


def get_backup_snapshot(dest_dir, backup_record):
    """Return relative paths and source hashes recorded for a backup."""
    snapshot = {}

    for item in load_backup_manifest(dest_dir, backup_record):
        items = item.get("files", []) if item.get("archive") else [item]

        for file_item in items:
            rel_path = file_item.get("rel_path")
            file_hash = file_item.get("source_hash")

            if rel_path and file_hash:
                snapshot[rel_path] = file_hash

    return snapshot


def filter_changed_files(files_to_backup, backup_type, history, dest_dir=None):
    """Select files using content hashes from previous backup manifests."""
    requested_type = backup_type.lower()

    if requested_type not in {"full", "incremental", "differential"}:
        raise ValueError(
            "Backup type must be full, incremental, or differential."
        )

    backups = history.get("backups", [])

    if requested_type == "full" or not backups:
        return files_to_backup, "Full"

    if dest_dir is None:
        raise ValueError("Destination path is required for change detection.")

    full_backups = [
        backup for backup in backups if backup.get("type") == "Full"
    ]

    if not full_backups:
        print_info("No previous full backup found; creating a Full backup.")
        return files_to_backup, "Full"

    if requested_type == "incremental":
        reference_backup = backups[-1]
        reference_snapshot = get_backup_snapshot(dest_dir, reference_backup)
        actual_type = "Incremental"
    else:
        reference_backup = full_backups[-1]
        reference_snapshot = get_backup_snapshot(dest_dir, reference_backup)
        actual_type = "Differential"

    changed_files = [
        item for item in files_to_backup
        if reference_snapshot.get(item["rel_path"]) != item.get("hash")
    ]

    return changed_files, actual_type


# ============================================================
# BACKUP EXECUTION ENGINE
# ============================================================



def print_success(message):
    print(f"[SUCCESS] {message}")


def print_error(message):
    print(f"[ERROR] {message}")


def print_warning(message):
    print(f"[WARNING] {message}")


def print_info(message):
    print(f"[INFO] {message}")


def print_header(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def write_backup_log(event, details):
    """Append a timestamped backup event to the local log."""
    log_path = os.path.join(os.path.dirname(__file__), "backup.log")
    record = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "event": event,
        "details": details,
    }

    with open(log_path, "a", encoding="utf-8") as file:
        file.write(json.dumps(record, ensure_ascii=False) + "\\n")


def write_backup_report(report):
    """Save a JSON report for a backup execution."""
    reports_dir = os.path.join(os.path.dirname(__file__), "reports")
    os.makedirs(reports_dir, exist_ok=True)

    safe_name = "".join(
        character if character.isalnum() or character in "-_" else "_"
        for character in report.get("job_name", "Backup_Job")
    )
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_path = os.path.join(
        reports_dir, f"{safe_name}_{timestamp}.json"
    )

    with open(report_path, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=2, ensure_ascii=False)

    return report_path


def run_backup_job(config):
    """Execute a backup job, recording destination results and a report."""
    start_time = time.time()
    started_at = datetime.now().isoformat(timespec="seconds")

    job_name = config.get("job_name", "Backup_Job")
    sources = config.get("sources", [])
    destinations = config.get("destinations", [])
    backup_type = str(config.get("type", "incremental")).lower()
    password = config.get("password")
    compress = config.get("compress", True)
    throttle_kb = config.get("throttle_kb", 0)
    retention_days = config.get("retention_days", 30)

    if isinstance(sources, str):
        sources = [sources]
    if isinstance(destinations, str):
        destinations = [destinations]

    report = {
        "job_name": job_name,
        "started_at": started_at,
        "finished_at": None,
        "status": "failed",
        "requested_type": backup_type,
        "sources": sources,
        "destinations": destinations,
        "files_scanned": 0,
        "total_size_scanned": 0,
        "duration_seconds": 0,
        "destination_results": [],
        "errors": [],
    }

    def finish_report():
        report["finished_at"] = datetime.now().isoformat(
            timespec="seconds"
        )
        report["duration_seconds"] = round(
            time.time() - start_time, 3
        )

        try:
            write_backup_log(
                "backup_job_finished",
                {
                    "job_name": job_name,
                    "status": report["status"],
                    "duration_seconds": report["duration_seconds"],
                    "errors": report["errors"],
                },
            )
            report_path = write_backup_report(report)
            print_info(f"Report saved: {report_path}")
        except Exception as exc:
            print_error(f"Could not save backup report/log: {exc}")

    print_header(f"BACKUP JOB: {job_name}")

    if not sources:
        report["errors"].append("At least one source path is required.")
    elif not destinations:
        report["errors"].append(
            "At least one destination path is required."
        )
    elif backup_type not in {"full", "incremental", "differential"}:
        report["errors"].append("Invalid backup type.")
    elif password and not CRYPTOGRAPHY_AVAILABLE:
        report["errors"].append(
            "Encryption requires the cryptography package."
        )
    elif retention_days < 0:
        report["errors"].append(
            "retention_days cannot be negative."
        )

    if report["errors"]:
        for error in report["errors"]:
            print_error(error)
        finish_report()
        return False

    print(f"Sources: {', '.join(sources)}")
    print(f"Destinations: {', '.join(destinations)}")
    print(f"Requested Type: {backup_type.capitalize()}")

    try:
        all_files, total_size = scan_source_directories(
            sources,
            config.get("include_patterns"),
            config.get("exclude_patterns"),
        )
    except Exception as exc:
        message = f"Source scanning failed: {exc}"
        report["errors"].append(message)
        print_error(message)
        write_backup_log(
            "source_scan_failed",
            {"job_name": job_name, "error": str(exc)},
        )
        finish_report()
        return False

    report["files_scanned"] = len(all_files)
    report["total_size_scanned"] = total_size

    print_success(f"Files Scanned: {len(all_files):,}")
    print_success(f"Total Size: {format_bytes(total_size)}")

    timestamp_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    timestamp_epoch = time.time()

    # Process each destination independently.
    for dest in destinations:
        result = {
            "destination": dest,
            "status": "failed",
            "backup_type": None,
            "files_written": 0,
            "bytes_written": 0,
            "integrity_check": "not_run",
            "error": None,
        }
        report["destination_results"].append(result)

        print(f"\nDestination: {dest}")

        try:
            os.makedirs(dest, exist_ok=True)

            history = load_destination_history(dest)
            files_to_process, actual_type = filter_changed_files(
                all_files, backup_type, history, dest
            )

            result["backup_type"] = actual_type
            print_info(f"Execution Mode: {actual_type} Backup")
            print_info(f"Files to Write: {len(files_to_process):,}")

            if not files_to_process:
                result["status"] = "up_to_date"
                result["integrity_check"] = "not_needed"

                print_success(
                    "No files changed. Destination is up to date."
                )
                write_backup_log(
                    "destination_up_to_date",
                    {"job_name": job_name, "destination": dest},
                )
                continue

            backup_folder_name = (
                f"backup_{timestamp_str}_{actual_type.lower()}"
            )
            current_backup_dir = os.path.join(
                dest, backup_folder_name
            )
            os.makedirs(current_backup_dir, exist_ok=False)

            manifest = []
            written_bytes = 0

            if compress:
                zip_path = os.path.join(
                    current_backup_dir, "archive.zip"
                )

                with zipfile.ZipFile(
                    zip_path, "w", zipfile.ZIP_DEFLATED
                ) as zipf:
                    for item in files_to_process:
                        zipf.write(
                            item["abs_path"], item["rel_path"]
                        )
                        written_bytes += item["size"]

                if password:
                    encrypted_path = zip_path + ".enc"
                    encrypt_file(
                        zip_path, encrypted_path, password, throttle_kb
                    )
                    os.remove(zip_path)
                    stored_path = encrypted_path
                else:
                    stored_path = zip_path

                manifest.append({
                    "archive": True,
                    "hash": calculate_file_hash(stored_path),
                    "file_count": len(files_to_process),
                    "files": [
                        {
                            "rel_path": item["rel_path"],
                            "source_hash": item.get("hash", ""),
                            "size": item["size"],
                            "mtime": item["mtime"],
                        }
                        for item in files_to_process
                    ],
                })

            else:
                for item in files_to_process:
                    target_path = os.path.join(
                        current_backup_dir, item["rel_path"]
                    )
                    os.makedirs(
                        os.path.dirname(target_path), exist_ok=True
                    )

                    if password:
                        stored_file = target_path + ".enc"
                        encrypt_file(
                            item["abs_path"],
                            stored_file,
                            password,
                            throttle_kb,
                        )
                    else:
                        stored_file = target_path
                        shutil.copy2(item["abs_path"], stored_file)

                    file_hash = calculate_file_hash(stored_file)
                    written_bytes += item["size"]

                    manifest.append({
                        "rel_path": item["rel_path"],
                        "hash": file_hash,
                        "source_hash": item.get("hash", ""),
                        "size": item["size"],
                        "mtime": item["mtime"],
                    })

            manifest_path = os.path.join(
                current_backup_dir, "manifest.json"
            )
            with open(manifest_path, "w", encoding="utf-8") as file:
                json.dump(manifest, file, indent=2)

            # Verify stored files before recording a successful backup.
            integrity_ok = True

            if compress:
                stored_path = os.path.join(
                    current_backup_dir,
                    "archive.zip.enc" if password else "archive.zip",
                )
                expected_hash = manifest[0]["hash"]
                actual_hash = calculate_file_hash(stored_path)

                integrity_ok = (
                    bool(actual_hash) and actual_hash == expected_hash
                )

                if integrity_ok and not password:
                    try:
                        with zipfile.ZipFile(stored_path, "r") as archive:
                            integrity_ok = archive.testzip() is None
                    except (OSError, zipfile.BadZipFile):
                        integrity_ok = False

            else:
                for item in manifest:
                    stored_path = os.path.join(
                        current_backup_dir,
                        item["rel_path"] + (".enc" if password else ""),
                    )
                    actual_hash = calculate_file_hash(stored_path)

                    if (
                        not actual_hash
                        or actual_hash != item["hash"]
                    ):
                        integrity_ok = False
                        print_error(
                            f"Integrity check failed: {item['rel_path']}"
                        )

            if not integrity_ok:
                result["integrity_check"] = "failed"
                raise RuntimeError("Backup integrity verification failed.")

            result["integrity_check"] = "passed"
            result["files_written"] = len(files_to_process)
            result["bytes_written"] = written_bytes
            result["status"] = "success"

            history.setdefault("backups", []).append({
                "folder": backup_folder_name,
                "timestamp": timestamp_epoch,
                "date": timestamp_str,
                "type": actual_type,
                "file_count": len(files_to_process),
                "size": written_bytes,
            })
            save_destination_history(dest, history)

            print_success(
                f"{len(files_to_process):,} files written "
                f"({format_bytes(written_bytes)})"
            )
            print_success("Integrity check: PASSED (SHA-256)")

            write_backup_log(
                "destination_backup_succeeded",
                {
                    "job_name": job_name,
                    "destination": dest,
                    "backup_folder": backup_folder_name,
                    "backup_type": actual_type,
                    "files_written": len(files_to_process),
                    "bytes_written": written_bytes,
                    "integrity_check": "passed",
                },
            )

            try:
                cleanup_old_backups(
                    dest, history, retention_days
                )
            except Exception as exc:
                # Cleanup failure should be visible without hiding the
                # fact that the newly created backup passed verification.
                warning = f"Retention cleanup failed for {dest}: {exc}"
                report["errors"].append(warning)
                print_warning(warning)
                write_backup_log(
                    "retention_cleanup_failed",
                    {"job_name": job_name, "error": warning},
                )

        except Exception as exc:
            result["status"] = "failed"
            result["error"] = str(exc)
            message = f"Destination {dest} failed: {exc}"
            report["errors"].append(message)
            print_error(message)

            try:
                write_backup_log(
                    "destination_backup_failed",
                    {
                        "job_name": job_name,
                        "destination": dest,
                        "error": str(exc),
                    },
                )
            except Exception as log_exc:
                print_error(f"Could not write failure log: {log_exc}")

    # Up-to-date destinations count as successful: no changes were needed.
    successful_statuses = {"success", "up_to_date"}
    report["status"] = (
        "success"
        if report["destination_results"]
        and all(
            item["status"] in successful_statuses
            for item in report["destination_results"]
        )
        else "failed"
    )

    duration = time.time() - start_time
    speed = (total_size / 1024) / duration if duration > 0 else 0

    print_header("BACKUP COMPLETE")
    print(f"Duration: {duration:.2f} seconds")
    print(f"Total size scanned: {format_bytes(total_size)}")
    print(f"Speed: {speed:.2f} KB/s")

    if report["status"] == "success":
        print_success("Backup job completed successfully.")
    else:
        print_error("Backup job failed on one or more destinations.")

    finish_report()

    if config.get("email_notifications", False):
        outcome = "SUCCESS" if report["status"] == "success" else "FAILED"
        subject = f"Backup {outcome}: {job_name}"
        body = (
            f"Job: {job_name}\n"
            f"Status: {report['status']}\n"
            f"Started: {report['started_at']}\n"
            f"Finished: {report['finished_at']}\n"
            f"Sources: {', '.join(sources)}\n"
            f"Destinations: {', '.join(destinations)}\n"
            f"Files scanned: {report['files_scanned']}\n"
            f"Bytes scanned: {report['total_size_scanned']}\n"
            f"Duration: {report['duration_seconds']} seconds\n"
            f"Errors: {report['errors']}\n"
            f"Destination results: {report['destination_results']}\n"
        )
        try:
            send_email_notification(config, subject, body)
        except Exception as exc:
            print_warning(f"Email notification failed: {exc}")
            try:
                write_backup_log(
                    "email_notification_failed",
                    {"subject": subject, "error": str(exc)},
                )
            except Exception:
                pass

    return report["status"] == "success"



# ============================================================
# EMAIL NOTIFICATIONS
# ============================================================

def send_email_notification(config, subject, body):
    """Send an optional email using SMTP environment configuration."""
    if not config.get("email_notifications", False):
        return False

    smtp_host = os.environ.get("BACKUP_SMTP_HOST")
    smtp_port_value = os.environ.get("BACKUP_SMTP_PORT", "587")
    smtp_user = os.environ.get("BACKUP_SMTP_USER")
    smtp_password = os.environ.get("BACKUP_SMTP_PASSWORD")
    sender = os.environ.get("BACKUP_EMAIL_FROM", smtp_user or "")
    recipients = config.get("email_to", [])

    if isinstance(recipients, str):
        recipients = [recipients]

    recipients = [
        recipient.strip()
        for recipient in recipients
        if isinstance(recipient, str) and recipient.strip()
    ]

    if not smtp_host or not sender or not recipients:
        print_warning(
            "Email notification skipped: configure BACKUP_SMTP_HOST, "
            "BACKUP_EMAIL_FROM (or BACKUP_SMTP_USER), and valid email_to recipients."
        )
        return False

    if "@" not in sender or any("@" not in recipient for recipient in recipients):
        print_warning("Email notification skipped: sender or recipient address is invalid.")
        return False

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = sender
    message["To"] = ", ".join(recipients)
    message.set_content(body)

    try:
        smtp_port = int(smtp_port_value)
        if not 1 <= smtp_port <= 65535:
            raise ValueError("SMTP port must be between 1 and 65535.")

        if smtp_port == 465:
            smtp_connection = smtplib.SMTP_SSL(
                smtp_host,
                smtp_port,
                timeout=20,
            )
        else:
            smtp_connection = smtplib.SMTP(
                smtp_host,
                smtp_port,
                timeout=20,
            )

        with smtp_connection as server:
            server.ehlo()

            if smtp_port != 465:
                server.starttls()
                server.ehlo()

            if smtp_user and smtp_password:
                server.login(smtp_user, smtp_password)

            server.send_message(message)

        print_success("Email notification sent.")
        write_backup_log(
            "email_notification_sent",
            {"subject": subject, "recipients": recipients},
        )
        return True

    except Exception as exc:
        print_warning(f"Email notification failed: {exc}")
        try:
            write_backup_log(
                "email_notification_failed",
                {"subject": subject, "error": str(exc)},
            )
        except Exception:
            pass
        return False

# ============================================================
# RETENTION POLICY & CLEANUP
# ============================================================

def cleanup_old_backups(dest_dir, history, retention_days=30):
    """Remove expired backup chains without orphaning retained backups."""
    print(f"\n🗑️ CLEANUP (Keeping last {retention_days} days):")

    if retention_days < 0:
        raise ValueError("retention_days cannot be negative.")

    backups = sorted(
        history.get("backups", []),
        key=lambda item: item.get("timestamp", 0)
    )
    cutoff = time.time() - retention_days * 86400

    # Each full backup starts a new chain. Incremental and differential
    # backups remain with their full backup until the whole chain expires.
    chains = []
    current_chain = []

    for backup in backups:
        if backup.get("type", "").lower() == "full":
            if current_chain:
                chains.append(current_chain)
            current_chain = [backup]
        elif current_chain:
            current_chain.append(backup)
        else:
            # Preserve orphaned records rather than deleting blindly.
            chains.append([backup])

    if current_chain:
        chains.append(current_chain)

    retained = []
    removed_count = 0
    saved_bytes = 0

    for chain in chains:
        newest_timestamp = max(
            item.get("timestamp", 0) for item in chain
        )

        # Retain the newest chain even if it is older than the cutoff.
        is_latest_chain = chain is chains[-1]
        chain_expired = newest_timestamp < cutoff

        if chain_expired and not is_latest_chain:
            folders = [item.get("folder") for item in chain]
            paths = [
                os.path.join(dest_dir, folder)
                for folder in folders
                if folder
            ]

            # Only remove a chain if every recorded folder is present.
            # Missing folders are retained in history for investigation.
            if len(paths) != len(chain) or not all(
                os.path.isdir(folder) for folder in paths
            ):
                retained.extend(chain)
                print_warning(
                    "Retaining an expired chain because a backup folder "
                    "is missing or unavailable."
                )
                continue

            try:
                for folder in paths:
                    shutil.rmtree(folder)
                removed_count += len(chain)
                saved_bytes += sum(
                    item.get("size", 0) for item in chain
                )
            except OSError as exc:
                retained.extend(chain)
                print_error(f"Could not remove backup chain: {exc}")
        else:
            retained.extend(chain)

    history["backups"] = sorted(
        retained, key=lambda item: item.get("timestamp", 0)
    )
    save_destination_history(dest_dir, history)

    if removed_count:
        print_success(
            f"Removed {removed_count} expired backups; "
            f"freed approximately {format_bytes(saved_bytes)}."
        )
    else:
        print_info("No complete backup chains eligible for cleanup.")

# ============================================================
# RESTORE ENGINE
# ============================================================


def restore_backup(dest_dir, target_restore_dir, password=None, point_in_time=None):
    """Restore a backup chain with integrity checks and safe path handling."""
    print_header("RESTORE SYSTEM")
    history = load_destination_history(dest_dir)
    backups = history.get("backups", [])

    if point_in_time:
        backups = [
            backup for backup in backups
            if backup.get("date", "") <= point_in_time
        ]

    if not backups:
        print_error("No backups found for the requested restore point.")
        return False

    backups = sorted(backups, key=lambda backup: backup.get("timestamp", 0))
    target_root = os.path.realpath(target_restore_dir)
    os.makedirs(target_root, exist_ok=True)

    def safe_output_path(relative_path):
        if not isinstance(relative_path, str) or not relative_path:
            raise ValueError("Missing or invalid relative path.")

        normalized = relative_path.replace("\\", "/")
        if normalized.startswith("/") or "\x00" in normalized:
            raise ValueError(f"Unsafe backup path: {relative_path}")

        parts = normalized.split("/")
        if any(part in ("", ".", "..") for part in parts):
            raise ValueError(f"Unsafe backup path: {relative_path}")

        output_path = os.path.realpath(os.path.join(target_root, *parts))
        if os.path.commonpath([target_root, output_path]) != target_root:
            raise ValueError(f"Backup path escapes restore directory: {relative_path}")

        return output_path

    def verify_hash(file_path, expected_hash, description):
        actual_hash = calculate_file_hash(file_path)
        if not actual_hash or not expected_hash or actual_hash.lower() != expected_hash.lower():
            raise ValueError(f"SHA-256 verification failed: {description}")

    restored_count = 0
    failures = []

    print_info(f"Restoring chain of {len(backups)} backups to '{target_root}'...")

    for backup in backups:
        backup_folder = os.path.join(dest_dir, backup.get("folder", ""))
        manifest_path = os.path.join(backup_folder, "manifest.json")

        try:
            if not os.path.isfile(manifest_path):
                raise FileNotFoundError("Manifest is missing.")

            with open(manifest_path, "r", encoding="utf-8") as file:
                manifest = json.load(file)

            if not isinstance(manifest, list):
                raise ValueError("Invalid manifest format.")

            if manifest and manifest[0].get("archive"):
                item = manifest[0]
                encrypted_archive = os.path.join(backup_folder, "archive.zip.enc")
                plain_archive = os.path.join(backup_folder, "archive.zip")
                temporary_zip = None

                if os.path.isfile(encrypted_archive):
                    if not password:
                        raise ValueError("Password required to decrypt this archive.")

                    verify_hash(encrypted_archive, item.get("hash"), "encrypted archive")
                    fd, temporary_zip = tempfile.mkstemp(
                        prefix="backup_restore_", suffix=".zip", dir=target_root
                    )
                    os.close(fd)
                    try:
                        decrypt_file(encrypted_archive, temporary_zip, password)
                        with zipfile.ZipFile(temporary_zip, "r") as archive:
                            bad_member = archive.testzip()
                            if bad_member:
                                raise ValueError(f"Corrupt ZIP member: {bad_member}")

                            for member in archive.infolist():
                                if member.is_dir():
                                    continue

                                output_path = safe_output_path(member.filename)
                                os.makedirs(os.path.dirname(output_path), exist_ok=True)

                                with archive.open(member, "r") as source, open(output_path, "wb") as output:
                                    shutil.copyfileobj(source, output)

                                expected_files = {
                                    entry.get("rel_path"): entry
                                    for entry in item.get("files", [])
                                }
                                expected = expected_files.get(member.filename, {})
                                if expected.get("source_hash"):
                                    verify_hash(
                                        output_path,
                                        expected["source_hash"],
                                        member.filename
                                    )
                                restored_count += 1
                    finally:
                        if temporary_zip and os.path.exists(temporary_zip):
                            os.remove(temporary_zip)

                elif os.path.isfile(plain_archive):
                    verify_hash(plain_archive, item.get("hash"), "archive")
                    with zipfile.ZipFile(plain_archive, "r") as archive:
                        bad_member = archive.testzip()
                        if bad_member:
                            raise ValueError(f"Corrupt ZIP member: {bad_member}")

                        expected_files = {
                            entry.get("rel_path"): entry
                            for entry in item.get("files", [])
                        }

                        for member in archive.infolist():
                            if member.is_dir():
                                continue

                            output_path = safe_output_path(member.filename)
                            os.makedirs(os.path.dirname(output_path), exist_ok=True)

                            with archive.open(member, "r") as source, open(output_path, "wb") as output:
                                shutil.copyfileobj(source, output)

                            expected = expected_files.get(member.filename, {})
                            if expected.get("source_hash"):
                                verify_hash(
                                    output_path,
                                    expected["source_hash"],
                                    member.filename
                                )
                            restored_count += 1
                else:
                    raise FileNotFoundError("Backup archive is missing.")

            else:
                for item in manifest:
                    rel_path = item.get("rel_path")
                    output_path = safe_output_path(rel_path)
                    encrypted_file = os.path.join(backup_folder, rel_path + ".enc")
                    raw_file = os.path.join(backup_folder, rel_path)

                    if os.path.isfile(encrypted_file):
                        if not password:
                            raise ValueError(f"Password required for {rel_path}.")
                        verify_hash(encrypted_file, item.get("hash"), rel_path + " encrypted backup")
                        os.makedirs(os.path.dirname(output_path), exist_ok=True)
                        decrypt_file(encrypted_file, output_path, password)
                    elif os.path.isfile(raw_file):
                        verify_hash(raw_file, item.get("hash"), rel_path + " backup")
                        os.makedirs(os.path.dirname(output_path), exist_ok=True)
                        shutil.copy2(raw_file, output_path)
                    else:
                        raise FileNotFoundError(f"Backup file missing: {rel_path}")

                    if item.get("source_hash"):
                        verify_hash(output_path, item["source_hash"], rel_path)
                    restored_count += 1

        except Exception as exc:
            message = f'{backup.get("date", backup.get("folder", "unknown"))}: {exc}'
            failures.append(message)
            print_error(f"Restore failed: {message}")

    if failures:
        print_error(
            f"Restore completed with errors. Files restored: {restored_count}; "
            f"failed backups: {len(failures)}."
        )
        return False

    print_success(
        f"Restore and integrity verification passed. "
        f"Files restored: {restored_count}. Destination: '{target_root}'"
    )
    return True


# ============================================================
# MAIN INTERACTIVE & CLI INTERFACE
# ============================================================

def show_menu():
    print("""
============================================================
💾 MULTI-DESTINATION BACKUP SYSTEM
============================================================

1. Run Interactive Backup Job
2. Run Quick Sample Test Backup
3. Restore From Backup
4. View Destination Backup Chains
0. Exit

============================================================
""")


def main():
    # Setup default paths for demo
    sample_src = "demo_source"
    sample_dest1 = "demo_dest_local"
    sample_dest2 = "demo_dest_external"

    while True:
        show_menu()
        choice = input("Choose an option (0-4): ").strip()

        if choice == "1":
            src = input(f"Source folder path [{sample_src}]: ").strip() or sample_src
            d1 = input(f"Destination 1 path [{sample_dest1}]: ").strip() or sample_dest1
            d2 = input(f"Destination 2 path [{sample_dest2}]: ").strip() or sample_dest2
            b_type = input("Backup type (full / incremental) [incremental]: ").strip() or "incremental"
            pwd = input("Encryption password (blank for none): ").strip() or None

            config = {
                "job_name": "Custom_Backup",
                "sources": [src],
                "destinations": [d1, d2],
                "type": b_type,
                "password": pwd,
                "compress": True,
                "retention_days": 30
            }
            run_backup_job(config)

        elif choice == "2":
            # Generate sample directory and files
            os.makedirs(sample_src, exist_ok=True)
            with open(os.path.join(sample_src, "document.txt"), "w") as f:
                f.write("Important documents content line 1.\n")
            with open(os.path.join(sample_src, "data.json"), "w") as f:
                f.write('{"status": "active"}\n')

            config = {
                "job_name": "Demo_Documents_Backup",
                "sources": [sample_src],
                "destinations": [sample_dest1, sample_dest2],
                "type": "incremental",
                "password": "SecretPassword123",
                "compress": True,
                "include_patterns": ["*"],
                "exclude_patterns": ["*.tmp"],
                "retention_days": 30
            }
            run_backup_job(config)

        elif choice == "3":
            dest = input(f"Destination folder to restore from [{sample_dest1}]: ").strip() or sample_dest1
            restore_target = input("Target folder for restored files [restored_data]: ").strip() or "restored_data"
            pwd = input("Decryption password (if encrypted): ").strip() or None
            restore_backup(dest, restore_target, password=pwd)

        elif choice == "4":
            dest = input(f"Destination folder to inspect [{sample_dest1}]: ").strip() or sample_dest1
            history = load_destination_history(dest)
            print_header(f"INCREMENTAL CHAIN IN {dest}")
            for b in reversed(history.get("backups", [])):
                print(f" - {b['date']} | Type: {b['type']:11s} | Files: {b['file_count']:4d} | Size: {format_bytes(b['size'])}")

        elif choice == "0":
            print("\n👋 Backup Utility closed.")
            break
        else:
            print_error("Invalid option. Select 0-4.")


if __name__ == "__main__":
    main()




