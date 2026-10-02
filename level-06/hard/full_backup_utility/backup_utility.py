import fnmatch
import hashlib
import json
import logging
import os
import shutil
import tarfile
import tempfile
import time
import zipfile
from datetime import datetime, timedelta
from getpass import getpass
from pathlib import Path

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt


# ============================================================
# CONSTANTS
# ============================================================

BACKUP_VERSION = "5.0"

ENCRYPTION_MAGIC = b"BKP-AESGCM-1"

SALT_SIZE = 16
NONCE_SIZE = 12
KEY_SIZE = 32

SCRYPT_N = 2**14
SCRYPT_R = 8
SCRYPT_P = 1

DEFAULT_RETENTION_DAYS = 30


# ============================================================
# LOGGING
# ============================================================

def configure_logger(destination):
    """Configure backup logging."""

    destination = Path(destination)
    destination.mkdir(
        parents=True,
        exist_ok=True,
    )

    logger = logging.getLogger("backup_utility")
    logger.setLevel(logging.INFO)

    if not logger.handlers:

        log_file = destination / "backup.log"

        file_handler = logging.FileHandler(
            log_file,
            encoding="utf-8",
        )

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        )

        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

    return logger


# ============================================================
# HASHING
# ============================================================

def calculate_md5(file_path):
    """Calculate the MD5 hash of a file."""

    md5 = hashlib.md5()

    with open(file_path, "rb") as file:

        while chunk := file.read(8192):
            md5.update(chunk)

    return md5.hexdigest()


def calculate_file_md5(file_path):
    """Calculate MD5 for a file."""

    return calculate_md5(file_path)


# ============================================================
# FILE SELECTION
# ============================================================

def matches_pattern(relative_path, pattern):
    """Check whether a relative path matches a pattern."""

    relative_path = Path(relative_path)

    path_string = relative_path.as_posix()

    return (
        fnmatch.fnmatch(
            path_string,
            pattern,
        )
        or fnmatch.fnmatch(
            relative_path.name,
            pattern,
        )
    )


def should_include_file(
    relative_path,
    include_patterns=None,
    exclude_patterns=None,
):
    """Determine whether a file should be included."""

    if exclude_patterns:

        for pattern in exclude_patterns:

            if matches_pattern(
                relative_path,
                pattern,
            ):
                return False

    if include_patterns:

        for pattern in include_patterns:

            if matches_pattern(
                relative_path,
                pattern,
            ):
                return True

        return False

    return True


# ============================================================
# FILE INFORMATION
# ============================================================

def get_file_info(
    file_path,
    source_directory,
    version=1,
):
    """Collect metadata about one file."""

    file_path = Path(file_path)
    source_directory = Path(source_directory)

    relative_path = file_path.relative_to(
        source_directory
    )

    stat = file_path.stat()

    return {
        "path": relative_path.as_posix(),
        "size": stat.st_size,
        "modified": stat.st_mtime,
        "md5": calculate_md5(file_path),
        "version": version,
    }


def determine_file_version(
    relative_path,
    current_md5,
    previous_manifest,
):
    """Determine the next version number for a file."""

    if not previous_manifest:
        return 1

    previous_info = previous_manifest.get(
        relative_path
    )

    if not previous_info:
        return 1

    previous_version = previous_info.get(
        "version",
        1,
    )

    previous_md5 = previous_info.get(
        "md5"
    )

    if previous_md5 == current_md5:
        return previous_version

    return previous_version + 1


# ============================================================
# MANIFEST
# ============================================================

def build_manifest(
    source_directory,
    previous_manifest=None,
    include_patterns=None,
    exclude_patterns=None,
):
    """Build a manifest containing information about selected files."""

    source_directory = Path(source_directory)

    if not source_directory.exists():

        raise FileNotFoundError(
            f"Source directory does not exist: "
            f"{source_directory}"
        )

    if not source_directory.is_dir():

        raise NotADirectoryError(
            f"Source path is not a directory: "
            f"{source_directory}"
        )

    previous_manifest = previous_manifest or {}

    manifest = {}

    for file_path in source_directory.rglob("*"):

        if not file_path.is_file():
            continue

        relative_path = file_path.relative_to(
            source_directory
        )

        relative_string = relative_path.as_posix()

        if not should_include_file(
            relative_path,
            include_patterns,
            exclude_patterns,
        ):
            continue

        current_md5 = calculate_md5(
            file_path
        )

        version = determine_file_version(
            relative_string,
            current_md5,
            previous_manifest,
        )

        manifest[relative_string] = get_file_info(
            file_path,
            source_directory,
            version=version,
        )

    return manifest


def save_manifest(
    manifest,
    output_file,
):
    """Save a manifest as JSON."""

    output_file = Path(output_file)

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        output_file,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            manifest,
            file,
            indent=4,
        )


def load_manifest(manifest_file):
    """Load a manifest from JSON."""

    manifest_file = Path(manifest_file)

    with open(
        manifest_file,
        "r",
        encoding="utf-8",
    ) as file:

        return json.load(file)


# ============================================================
# MANIFEST COMPARISON
# ============================================================

def compare_manifests(
    previous_manifest,
    current_manifest,
):
    """Compare two manifests."""

    previous_paths = set(
        previous_manifest
    )

    current_paths = set(
        current_manifest
    )

    new_files = current_paths - previous_paths

    deleted_files = previous_paths - current_paths

    common_files = (
        previous_paths & current_paths
    )

    modified_files = set()
    unchanged_files = set()

    for path in common_files:

        previous_md5 = previous_manifest[path]["md5"]
        current_md5 = current_manifest[path]["md5"]

        if previous_md5 != current_md5:

            modified_files.add(path)

        else:

            unchanged_files.add(path)

    return {
        "new": sorted(new_files),
        "modified": sorted(modified_files),
        "unchanged": sorted(unchanged_files),
        "deleted": sorted(deleted_files),
    }


def get_incremental_files(changes):
    """Return files changed since the previous backup."""

    return (
        changes["new"]
        + changes["modified"]
    )


# ============================================================
# BACKUP IDs / DIRECTORIES
# ============================================================

def generate_backup_id():
    """Generate a unique backup ID."""

    timestamp = datetime.now().strftime(
        "%Y-%m-%d-%H%M%S"
    )

    return f"BKP-{timestamp}"


def create_backup_directory(
    destination,
    backup_id,
):
    """Create and return a backup directory."""

    destination = Path(destination)

    destination.mkdir(
        parents=True,
        exist_ok=True,
    )

    backup_directory = (
        destination / backup_id
    )

    backup_directory.mkdir(
        parents=True,
        exist_ok=False,
    )

    return backup_directory


# ============================================================
# FILE COPYING
# ============================================================

def copy_files(
    source_directory,
    backup_directory,
    manifest,
    selected_files=None,
):
    """Copy selected files into a backup directory."""

    source_directory = Path(
        source_directory
    )

    if selected_files is None:
        selected_files = manifest.keys()

    files_copied = 0
    total_size = 0

    for relative_path in selected_files:

        file_info = manifest[
            relative_path
        ]

        relative_path = Path(
            relative_path
        )

        source_file = (
            source_directory
            / relative_path
        )

        destination_file = (
            backup_directory
            / relative_path
        )

        destination_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        shutil.copy2(
            source_file,
            destination_file,
        )

        files_copied += 1
        total_size += file_info["size"]

    return files_copied, total_size


# ============================================================
# ARCHIVING
# ============================================================

def create_tar_gz(
    source_directory,
    archive_path,
):
    """Create a tar.gz archive."""

    source_directory = Path(
        source_directory
    )

    archive_path = Path(
        archive_path
    )

    with tarfile.open(
        archive_path,
        "w:gz",
    ) as archive:

        archive.add(
            source_directory,
            arcname=source_directory.name,
        )


def create_zip(
    source_directory,
    archive_path,
):
    """Create a ZIP archive."""

    source_directory = Path(
        source_directory
    )

    archive_path = Path(
        archive_path
    )

    with zipfile.ZipFile(
        archive_path,
        "w",
        zipfile.ZIP_DEFLATED,
    ) as archive:

        for file_path in source_directory.rglob("*"):

            if file_path.is_file():

                archive.write(
                    file_path,
                    arcname=(
                        Path(
                            source_directory.name
                        )
                        / file_path.relative_to(
                            source_directory
                        )
                    ),
                )


def get_archive_extension(compression):
    """Return the archive extension."""

    if compression == "tar.gz":
        return ".tar.gz"

    if compression == "zip":
        return ".zip"

    raise ValueError(
        "Unsupported compression format. "
        "Choose 'tar.gz' or 'zip'."
    )


def create_archive(
    source_directory,
    archive_path,
    compression="tar.gz",
):
    """Create an archive using the selected format."""

    compression = compression.lower()

    if compression == "tar.gz":

        create_tar_gz(
            source_directory,
            archive_path,
        )

    elif compression == "zip":

        create_zip(
            source_directory,
            archive_path,
        )

    else:

        raise ValueError(
            "Unsupported compression format. "
            "Choose 'tar.gz' or 'zip'."
        )


# ============================================================
# AES ENCRYPTION
# ============================================================

def derive_encryption_key(
    password,
    salt,
):
    """Derive a 256-bit AES key from a password."""

    kdf = Scrypt(
        salt=salt,
        length=KEY_SIZE,
        n=SCRYPT_N,
        r=SCRYPT_R,
        p=SCRYPT_P,
    )

    return kdf.derive(
        password.encode("utf-8")
    )


def encrypt_file(
    input_file,
    output_file,
    password,
):
    """Encrypt a file using AES-256-GCM."""

    input_file = Path(input_file)
    output_file = Path(output_file)

    plaintext = input_file.read_bytes()

    salt = os.urandom(
        SALT_SIZE
    )

    nonce = os.urandom(
        NONCE_SIZE
    )

    key = derive_encryption_key(
        password,
        salt,
    )

    aes = AESGCM(key)

    ciphertext = aes.encrypt(
        nonce,
        plaintext,
        ENCRYPTION_MAGIC,
    )

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        output_file,
        "wb",
    ) as file:

        file.write(
            ENCRYPTION_MAGIC
        )

        file.write(salt)

        file.write(nonce)

        file.write(ciphertext)

    return output_file


def decrypt_file(
    encrypted_file,
    output_file,
    password,
):
    """Decrypt an AES-256-GCM encrypted file."""

    encrypted_file = Path(
        encrypted_file
    )

    output_file = Path(
        output_file
    )

    data = encrypted_file.read_bytes()

    header_size = (
        len(ENCRYPTION_MAGIC)
        + SALT_SIZE
        + NONCE_SIZE
    )

    if len(data) < header_size:

        raise ValueError(
            "Invalid encrypted backup."
        )

    magic = data[
        :len(ENCRYPTION_MAGIC)
    ]

    if magic != ENCRYPTION_MAGIC:

        raise ValueError(
            "Invalid encryption format."
        )

    offset = len(
        ENCRYPTION_MAGIC
    )

    salt = data[
        offset:
        offset + SALT_SIZE
    ]

    offset += SALT_SIZE

    nonce = data[
        offset:
        offset + NONCE_SIZE
    ]

    offset += NONCE_SIZE

    ciphertext = data[offset:]

    key = derive_encryption_key(
        password,
        salt,
    )

    aes = AESGCM(key)

    try:

        plaintext = aes.decrypt(
            nonce,
            ciphertext,
            ENCRYPTION_MAGIC,
        )

    except InvalidTag:

        raise ValueError(
            "Incorrect password or "
            "corrupted encrypted backup."
        )

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_file.write_bytes(
        plaintext
    )

    return output_file


# ============================================================
# METADATA
# ============================================================

def create_backup_metadata(
    backup_id,
    mode,
    source,
    files,
    size_original,
    duration,
    compression,
    encrypted,
    include_patterns,
    exclude_patterns,
):
    """Create metadata describing a backup."""

    return {
        "backup_id": backup_id,
        "mode": mode,
        "source": str(source),
        "files": files,
        "size_original": size_original,
        "compression": compression,
        "encrypted": encrypted,
        "include_patterns": (
            include_patterns or []
        ),
        "exclude_patterns": (
            exclude_patterns or []
        ),
        "timestamp": datetime.now().isoformat(),
        "duration_seconds": round(
            duration,
            2,
        ),
    }


def save_backup_metadata(
    metadata,
    backup_directory,
):
    """Save backup metadata as JSON."""

    metadata_file = (
        Path(backup_directory)
        / "metadata.json"
    )

    with open(
        metadata_file,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            metadata,
            file,
            indent=4,
        )

    return metadata_file


# ============================================================
# VERSION TRACKING
# ============================================================

def build_version_history(manifest):
    """Build file-version information."""

    versions = {}

    for path, info in manifest.items():

        versions[path] = {
            "version": info.get(
                "version",
                1,
            ),
            "md5": info["md5"],
            "size": info["size"],
            "modified": info["modified"],
        }

    return versions


def save_version_history(
    manifest,
    output_file,
):
    """Save version tracking information."""

    versions = build_version_history(
        manifest
    )

    save_manifest(
        versions,
        output_file,
    )


# ============================================================
# SIZE REPORTING
# ============================================================

def calculate_directory_size(
    directory,
):
    """Calculate the total size of files in a directory."""

    directory = Path(directory)

    total = 0

    for file_path in directory.rglob("*"):

        if file_path.is_file():
            total += file_path.stat().st_size

    return total


def calculate_compression_ratio(
    original_size,
    compressed_size,
):
    """Calculate compression ratio."""

    if original_size == 0:
        return 0.0

    return round(
        compressed_size / original_size * 100,
        2,
    )


# ============================================================
# COMMON BACKUP FINALIZATION
# ============================================================

def finalize_backup(
    backup_directory,
    destination,
    backup_id,
    compression,
    encrypted,
    password,
    metadata,
):
    """Create archive, optionally encrypt it, and report statistics."""

    archive_extension = get_archive_extension(
        compression
    )

    archive_path = (
        Path(destination)
        / f"{backup_id}{archive_extension}"
    )

    print(
        "📦 Creating compressed archive..."
    )

    create_archive(
        backup_directory,
        archive_path,
        compression,
    )

    compressed_size = archive_path.stat().st_size

    checksum = calculate_md5(
        archive_path
    )

    final_archive = archive_path

    if encrypted:

        print(
            "🔐 Encrypting archive..."
        )

        encrypted_path = (
            Path(destination)
            / f"{backup_id}{archive_extension}.enc"
        )

        encrypt_file(
            archive_path,
            encrypted_path,
            password,
        )

        archive_path.unlink()

        final_archive = encrypted_path

        compressed_size = (
            encrypted_path.stat().st_size
        )

        checksum = calculate_md5(
            encrypted_path
        )

    metadata["compressed_size"] = (
        compressed_size
    )

    metadata["compression_ratio_percent"] = (
        calculate_compression_ratio(
            metadata["size_original"],
            compressed_size,
        )
    )

    metadata["checksum_md5"] = checksum

    metadata["archive"] = str(
        final_archive
    )

    save_backup_metadata(
        metadata,
        backup_directory,
    )

    return {
        "metadata": metadata,
        "archive": str(final_archive),
        "compressed_size": compressed_size,
        "checksum": checksum,
    }


# ============================================================
# FULL BACKUP
# ============================================================

def create_full_backup(
    source_directory,
    destination,
    compression="tar.gz",
    encrypted=False,
    password=None,
    include_patterns=None,
    exclude_patterns=None,
):
    """Create a complete full backup."""

    source_directory = Path(
        source_directory
    )

    destination = Path(
        destination
    )

    logger = configure_logger(
        destination
    )

    print()
    print("=" * 60)
    print("💾 CREATING FULL BACKUP")
    print("=" * 60)

    start_time = time.time()

    manifest = build_manifest(
        source_directory,
        include_patterns=include_patterns,
        exclude_patterns=exclude_patterns,
    )

    backup_id = generate_backup_id()

    logger.info(
        "Starting full backup: %s",
        backup_id,
    )

    print(
        f"Backup ID: {backup_id}"
    )

    print(
        f"Source: {source_directory}"
    )

    print(
        f"Files found: {len(manifest)}"
    )

    print(
        f"Compression: {compression}"
    )

    print(
        f"Encryption: "
        f"{'AES-256-GCM' if encrypted else 'disabled'}"
    )

    backup_directory = (
        create_backup_directory(
            destination,
            backup_id,
        )
    )

    print()
    print("📁 Copying files...")

    files_copied, total_size = copy_files(
        source_directory,
        backup_directory,
        manifest,
    )

    manifest_file = (
        backup_directory
        / "manifest.json"
    )

    save_manifest(
        manifest,
        manifest_file,
    )

    versions_file = (
        backup_directory
        / "versions.json"
    )

    save_version_history(
        manifest,
        versions_file,
    )

    duration = (
        time.time()
        - start_time
    )

    metadata = create_backup_metadata(
        backup_id=backup_id,
        mode="full",
        source=source_directory,
        files=files_copied,
        size_original=total_size,
        duration=duration,
        compression=compression,
        encrypted=encrypted,
        include_patterns=include_patterns,
        exclude_patterns=exclude_patterns,
    )

    metadata_file = save_backup_metadata(
        metadata,
        backup_directory,
    )

    result = finalize_backup(
        backup_directory=backup_directory,
        destination=destination,
        backup_id=backup_id,
        compression=compression,
        encrypted=encrypted,
        password=password,
        metadata=metadata,
    )

    compressed_size = result[
        "compressed_size"
    ]

    checksum = result[
        "checksum"
    ]

    print()
    print("=" * 60)
    print("📊 BACKUP STATISTICS")
    print("=" * 60)
    print(
        f"Files copied: {files_copied}"
    )
    print(
        f"Original size: "
        f"{total_size:,} bytes"
    )
    print(
        f"Compressed size: "
        f"{compressed_size:,} bytes"
    )
    print(
        f"Compression: {compression}"
    )
    print(
        f"Encryption: "
        f"{'AES-256-GCM' if encrypted else 'disabled'}"
    )
    print(
        f"Duration: {duration:.2f} seconds"
    )
    print(
        f"MD5: {checksum}"
    )
    print()
    print(
        f"📋 Metadata: {metadata_file}"
    )
    print(
        f"📋 Manifest: {manifest_file}"
    )
    print(
        f"📦 Archive: {result['archive']}"
    )

    logger.info(
        "Full backup completed: %s",
        backup_id,
    )

    return result


# ============================================================
# INCREMENTAL BACKUP
# ============================================================

def create_incremental_backup(
    source_directory,
    destination,
    previous_backup,
    compression="tar.gz",
    encrypted=False,
    password=None,
    include_patterns=None,
    exclude_patterns=None,
):
    """Create an incremental backup."""

    source_directory = Path(
        source_directory
    )

    destination = Path(
        destination
    )

    previous_backup = Path(
        previous_backup
    )

    logger = configure_logger(
        destination
    )

    print()
    print("=" * 60)
    print("💾 CREATING INCREMENTAL BACKUP")
    print("=" * 60)

    start_time = time.time()

    previous_manifest = load_manifest(
        previous_backup
        / "manifest.json"
    )

    current_manifest = build_manifest(
        source_directory,
        previous_manifest=previous_manifest,
        include_patterns=include_patterns,
        exclude_patterns=exclude_patterns,
    )

    changes = compare_manifests(
        previous_manifest,
        current_manifest,
    )

    incremental_files = (
        get_incremental_files(
            changes
        )
    )

    backup_id = generate_backup_id()

    logger.info(
        "Starting incremental backup: %s",
        backup_id,
    )

    print(
        f"Backup ID: {backup_id}"
    )

    print(
        f"Previous backup: "
        f"{previous_backup}"
    )

    print(
        f"New files: "
        f"{len(changes['new'])}"
    )

    print(
        f"Modified files: "
        f"{len(changes['modified'])}"
    )

    print(
        f"Deleted files: "
        f"{len(changes['deleted'])}"
    )

    print(
        f"Unchanged files: "
        f"{len(changes['unchanged'])}"
    )

    backup_directory = (
        create_backup_directory(
            destination,
            backup_id,
        )
    )

    print()
    print("📁 Copying changed files...")

    files_copied, total_size = copy_files(
        source_directory,
        backup_directory,
        current_manifest,
        incremental_files,
    )

    manifest_file = (
        backup_directory
        / "manifest.json"
    )

    save_manifest(
        current_manifest,
        manifest_file,
    )

    changes_file = (
        backup_directory
        / "changes.json"
    )

    save_manifest(
        changes,
        changes_file,
    )

    versions_file = (
        backup_directory
        / "versions.json"
    )

    save_version_history(
        current_manifest,
        versions_file,
    )

    duration = (
        time.time()
        - start_time
    )

    metadata = create_backup_metadata(
        backup_id=backup_id,
        mode="incremental",
        source=source_directory,
        files=files_copied,
        size_original=total_size,
        duration=duration,
        compression=compression,
        encrypted=encrypted,
        include_patterns=include_patterns,
        exclude_patterns=exclude_patterns,
    )

    metadata_file = save_backup_metadata(
        metadata,
        backup_directory,
    )

    result = finalize_backup(
        backup_directory=backup_directory,
        destination=destination,
        backup_id=backup_id,
        compression=compression,
        encrypted=encrypted,
        password=password,
        metadata=metadata,
    )

    print()
    print("=" * 60)
    print("📊 INCREMENTAL BACKUP STATISTICS")
    print("=" * 60)
    print(
        f"Files copied: {files_copied}"
    )
    print(
        f"Original size: "
        f"{total_size:,} bytes"
    )
    print(
        f"Compressed size: "
        f"{result['compressed_size']:,} bytes"
    )
    print(
        f"MD5: {result['checksum']}"
    )
    print()
    print(
        f"📋 Metadata: {metadata_file}"
    )
    print(
        f"📋 Manifest: {manifest_file}"
    )
    print(
        f"📋 Changes: {changes_file}"
    )
    print(
        f"📦 Archive: {result['archive']}"
    )

    logger.info(
        "Incremental backup completed: %s",
        backup_id,
    )

    return result


# ============================================================
# DIFFERENTIAL BACKUP
# ============================================================

def create_differential_backup(
    source_directory,
    destination,
    full_backup,
    compression="tar.gz",
    encrypted=False,
    password=None,
    include_patterns=None,
    exclude_patterns=None,
):
    """Create a differential backup from the last full backup."""

    source_directory = Path(
        source_directory
    )

    destination = Path(
        destination
    )

    full_backup = Path(
        full_backup
    )

    logger = configure_logger(
        destination
    )

    print()
    print("=" * 60)
    print("💾 CREATING DIFFERENTIAL BACKUP")
    print("=" * 60)

    start_time = time.time()

    full_manifest = load_manifest(
        full_backup
        / "manifest.json"
    )

    current_manifest = build_manifest(
        source_directory,
        previous_manifest=full_manifest,
        include_patterns=include_patterns,
        exclude_patterns=exclude_patterns,
    )

    changes = compare_manifests(
        full_manifest,
        current_manifest,
    )

    differential_files = (
        get_incremental_files(
            changes
        )
    )

    backup_id = generate_backup_id()

    logger.info(
        "Starting differential backup: %s",
        backup_id,
    )

    print(
        f"Backup ID: {backup_id}"
    )

    print(
        f"Full backup: {full_backup}"
    )

    print(
        f"New files: "
        f"{len(changes['new'])}"
    )

    print(
        f"Modified files: "
        f"{len(changes['modified'])}"
    )

    print(
        f"Deleted files: "
        f"{len(changes['deleted'])}"
    )

    print(
        f"Unchanged files: "
        f"{len(changes['unchanged'])}"
    )

    backup_directory = (
        create_backup_directory(
            destination,
            backup_id,
        )
    )

    print()
    print("📁 Copying changed files...")

    files_copied, total_size = copy_files(
        source_directory,
        backup_directory,
        current_manifest,
        differential_files,
    )

    manifest_file = (
        backup_directory
        / "manifest.json"
    )

    save_manifest(
        current_manifest,
        manifest_file,
    )

    changes_file = (
        backup_directory
        / "changes.json"
    )

    save_manifest(
        changes,
        changes_file,
    )

    versions_file = (
        backup_directory
        / "versions.json"
    )

    save_version_history(
        current_manifest,
        versions_file,
    )

    duration = (
        time.time()
        - start_time
    )

    metadata = create_backup_metadata(
        backup_id=backup_id,
        mode="differential",
        source=source_directory,
        files=files_copied,
        size_original=total_size,
        duration=duration,
        compression=compression,
        encrypted=encrypted,
        include_patterns=include_patterns,
        exclude_patterns=exclude_patterns,
    )

    metadata_file = save_backup_metadata(
        metadata,
        backup_directory,
    )

    result = finalize_backup(
        backup_directory=backup_directory,
        destination=destination,
        backup_id=backup_id,
        compression=compression,
        encrypted=encrypted,
        password=password,
        metadata=metadata,
    )

    print()
    print("=" * 60)
    print("📊 DIFFERENTIAL BACKUP STATISTICS")
    print("=" * 60)
    print(
        f"Files copied: {files_copied}"
    )
    print(
        f"Original size: "
        f"{total_size:,} bytes"
    )
    print(
        f"Compressed size: "
        f"{result['compressed_size']:,} bytes"
    )
    print(
        f"MD5: {result['checksum']}"
    )
    print()
    print(
        f"📋 Metadata: {metadata_file}"
    )
    print(
        f"📋 Manifest: {manifest_file}"
    )
    print(
        f"📋 Changes: {changes_file}"
    )
    print(
        f"📦 Archive: {result['archive']}"
    )

    logger.info(
        "Differential backup completed: %s",
        backup_id,
    )

    return result


# ============================================================
# INTEGRITY VERIFICATION
# ============================================================

def verify_backup(
    backup_directory,
    save_report=True,
):
    """Verify every file against its manifest MD5 hash."""

    backup_directory = Path(
        backup_directory
    )

    manifest_file = (
        backup_directory
        / "manifest.json"
    )

    if not manifest_file.exists():

        raise FileNotFoundError(
            "manifest.json was not found."
        )

    manifest = load_manifest(
        manifest_file
    )

    verified = []
    corrupted = []
    missing = []
    extra = []

    for relative_path, info in manifest.items():

        file_path = (
            backup_directory
            / relative_path
        )

        if not file_path.exists():

            missing.append(
                relative_path
            )

            continue

        actual_md5 = calculate_md5(
            file_path
        )

        expected_md5 = info[
            "md5"
        ]

        if actual_md5 == expected_md5:

            verified.append(
                relative_path
            )

        else:

            corrupted.append(
                {
                    "path": relative_path,
                    "expected": expected_md5,
                    "actual": actual_md5,
                }
            )

    expected_files = set(
        manifest
    )

    ignored_files = {
        "manifest.json",
        "metadata.json",
        "changes.json",
        "versions.json",
    }

    actual_files = set()

    for file_path in backup_directory.rglob("*"):

        if not file_path.is_file():
            continue

        relative = (
            file_path.relative_to(
                backup_directory
            ).as_posix()
        )

        if relative in ignored_files:
            continue

        actual_files.add(relative)

    extra = sorted(
        actual_files - expected_files
    )

    report = {
        "backup_directory": str(
            backup_directory
        ),
        "timestamp": datetime.now().isoformat(),
        "total_expected": len(manifest),
        "verified": len(verified),
        "corrupted": len(corrupted),
        "missing": len(missing),
        "extra": len(extra),
        "status": (
            "PASS"
            if not corrupted and not missing
            else "FAIL"
        ),
        "corrupted_files": corrupted,
        "missing_files": missing,
        "extra_files": extra,
    }

    if save_report:

        report_file = (
            backup_directory
            / "integrity_report.json"
        )

        with open(
            report_file,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                report,
                file,
                indent=4,
            )

    print()
    print("=" * 60)
    print("🔎 INTEGRITY VERIFICATION")
    print("=" * 60)
    print(
        f"Expected files: "
        f"{report['total_expected']}"
    )
    print(
        f"Verified: "
        f"{report['verified']}"
    )
    print(
        f"Corrupted: "
        f"{report['corrupted']}"
    )
    print(
        f"Missing: "
        f"{report['missing']}"
    )
    print(
        f"Extra: "
        f"{report['extra']}"
    )
    print(
        f"Status: "
        f"{report['status']}"
    )

    return report


# ============================================================
# SAFE ARCHIVE EXTRACTION
# ============================================================

def safe_extract_archive(
    archive_path,
    target_directory,
):
    """Safely extract an archive without path traversal."""

    archive_path = Path(
        archive_path
    )

    target_directory = Path(
        target_directory
    )

    target_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    target_resolved = (
        target_directory.resolve()
    )

    if archive_path.name.endswith(
        ".tar.gz"
    ):

        with tarfile.open(
            archive_path,
            "r:gz",
        ) as archive:

            for member in archive.getmembers():

                destination = (
                    target_directory
                    / member.name
                )

                if not str(
                    destination.resolve()
                ).startswith(
                    str(target_resolved)
                ):

                    raise ValueError(
                        "Unsafe archive path detected."
                    )

            archive.extractall(
                target_directory
            )

    elif archive_path.suffix == ".zip":

        with zipfile.ZipFile(
            archive_path,
            "r",
        ) as archive:

            for member in archive.namelist():

                destination = (
                    target_directory
                    / member
                )

                if not str(
                    destination.resolve()
                ).startswith(
                    str(target_resolved)
                ):

                    raise ValueError(
                        "Unsafe archive path detected."
                    )

            archive.extractall(
                target_directory
            )

    else:

        raise ValueError(
            "Unsupported archive format."
        )


# ============================================================
# RESTORE
# ============================================================

def restore_from_directory(
    backup_directory,
    target_directory,
    selected_files=None,
):
    """Restore files from an uncompressed backup directory."""

    backup_directory = Path(
        backup_directory
    )

    target_directory = Path(
        target_directory
    )

    manifest = load_manifest(
        backup_directory
        / "manifest.json"
    )

    if selected_files is None:

        selected_files = manifest.keys()

    restored = 0

    for relative_path in selected_files:

        if relative_path not in manifest:
            raise FileNotFoundError(
                f"File not found in manifest: "
                f"{relative_path}"
            )

        source_file = (
            backup_directory
            / relative_path
        )

        target_file = (
            target_directory
            / relative_path
        )

        target_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        shutil.copy2(
            source_file,
            target_file,
        )

        restored += 1

    return restored


def restore_backup(
    backup_source,
    target_directory,
    password=None,
    selected_files=None,
):
    """Restore a full backup from a directory or archive."""

    backup_source = Path(
        backup_source
    )

    target_directory = Path(
        target_directory
    )

    if backup_source.is_dir():

        restored = restore_from_directory(
            backup_source,
            target_directory,
            selected_files,
        )

        print(
            f"✅ Restored {restored} files."
        )

        return restored

    if not backup_source.is_file():

        raise FileNotFoundError(
            f"Backup source does not exist: "
            f"{backup_source}"
        )

    temporary_directory = Path(
        tempfile.mkdtemp(
            prefix="backup_restore_"
        )
    )

    try:

        archive_to_extract = (
            backup_source
        )

        if backup_source.suffix == ".enc":

            if not password:

                raise ValueError(
                    "A password is required "
                    "for an encrypted backup."
                )

            original_name = (
                backup_source.name[:-4]
            )

            decrypted_archive = (
                temporary_directory
                / original_name
            )

            decrypt_file(
                backup_source,
                decrypted_archive,
                password,
            )

            archive_to_extract = (
                decrypted_archive
            )

        extract_directory = (
            temporary_directory
            / "extracted"
        )

        safe_extract_archive(
            archive_to_extract,
            extract_directory,
        )

        backup_directories = [
            path
            for path in extract_directory.iterdir()
            if path.is_dir()
        ]

        if not backup_directories:

            raise ValueError(
                "Backup archive contains "
                "no backup directory."
            )

        actual_backup_directory = (
            backup_directories[0]
        )

        restored = restore_from_directory(
            actual_backup_directory,
            target_directory,
            selected_files,
        )

        print(
            f"✅ Restored {restored} files."
        )

        return restored

    finally:

        shutil.rmtree(
            temporary_directory,
            ignore_errors=True,
        )


# ============================================================
# BACKUP CHAIN RESTORE
# ============================================================

def apply_changes_to_restore(
    backup_directory,
    target_directory,
):
    """Apply an incremental/differential backup to a restore."""

    backup_directory = Path(
        backup_directory
    )

    target_directory = Path(
        target_directory
    )

    manifest = load_manifest(
        backup_directory
        / "manifest.json"
    )

    changes_file = (
        backup_directory
        / "changes.json"
    )

    if not changes_file.exists():

        return 0

    changes = load_manifest(
        changes_file
    )

    restored = 0

    changed_files = (
        changes["new"]
        + changes["modified"]
    )

    for relative_path in changed_files:

        source_file = (
            backup_directory
            / relative_path
        )

        if not source_file.exists():
            continue

        target_file = (
            target_directory
            / relative_path
        )

        target_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        shutil.copy2(
            source_file,
            target_file,
        )

        restored += 1

    for relative_path in changes[
        "deleted"
    ]:

        target_file = (
            target_directory
            / relative_path
        )

        if target_file.exists():

            target_file.unlink()

    return restored


def restore_backup_chain(
    full_backup,
    additional_backups,
    target_directory,
):
    """Restore a full backup followed by incremental/differential backups."""

    target_directory = Path(
        target_directory
    )

    target_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    restored = restore_from_directory(
        full_backup,
        target_directory,
    )

    for backup in additional_backups:

        restored += (
            apply_changes_to_restore(
                backup,
                target_directory,
            )
        )

    print(
        f"✅ Backup chain restored."
    )

    print(
        f"Files copied/updated: "
        f"{restored}"
    )

    return restored


# ============================================================
# RETENTION
# ============================================================

def parse_backup_timestamp(
    backup_directory,
):
    """Read a backup timestamp from metadata."""

    metadata_file = (
        Path(backup_directory)
        / "metadata.json"
    )

    if metadata_file.exists():

        try:

            metadata = load_manifest(
                metadata_file
            )

            return datetime.fromisoformat(
                metadata["timestamp"]
            )

        except (
            KeyError,
            ValueError,
            TypeError,
        ):
            pass

    return datetime.fromtimestamp(
        Path(backup_directory).stat().st_mtime
    )


def apply_retention_policy(
    destination,
    retention_days=DEFAULT_RETENTION_DAYS,
):
    """Delete backups older than the retention period."""

    destination = Path(
        destination
    )

    cutoff = (
        datetime.now()
        - timedelta(
            days=retention_days
        )
    )

    removed = []

    for backup_directory in destination.iterdir():

        if not backup_directory.is_dir():
            continue

        if not backup_directory.name.startswith(
            "BKP-"
        ):
            continue

        timestamp = parse_backup_timestamp(
            backup_directory
        )

        if timestamp >= cutoff:
            continue

        backup_id = (
            backup_directory.name
        )

        shutil.rmtree(
            backup_directory
        )

        for archive in destination.glob(
            f"{backup_id}*"
        ):

            if archive.is_file():

                archive.unlink()

        removed.append(
            backup_id
        )

    return removed


# ============================================================
# SCHEDULING
# ============================================================

def is_backup_due(
    last_backup,
    schedule,
    now=None,
):
    """Determine whether a scheduled backup is due."""

    if now is None:
        now = datetime.now()

    if last_backup is None:
        return True

    schedule = schedule.lower()

    if schedule == "daily":

        return now.date() > last_backup.date()

    if schedule == "weekly":

        return (
            now - last_backup
        ) >= timedelta(days=7)

    if schedule == "monthly":

        return (
            now.year,
            now.month,
        ) != (
            last_backup.year,
            last_backup.month,
        )

    raise ValueError(
        "Schedule must be daily, weekly, or monthly."
    )


def get_next_backup_time(
    last_backup,
    schedule,
):
    """Calculate the next scheduled backup time."""

    if last_backup is None:
        return datetime.now()

    schedule = schedule.lower()

    if schedule == "daily":

        return last_backup + timedelta(
            days=1
        )

    if schedule == "weekly":

        return last_backup + timedelta(
            days=7
        )

    if schedule == "monthly":

        year = last_backup.year
        month = last_backup.month + 1

        if month == 13:

            month = 1
            year += 1

        return last_backup.replace(
            year=year,
            month=month,
        )

    raise ValueError(
        "Schedule must be daily, weekly, or monthly."
    )


# ============================================================
# DISPLAY
# ============================================================

def display_manifest(manifest):
    """Display manifest information."""

    print()
    print("=" * 60)
    print("📋 FILE MANIFEST")
    print("=" * 60)

    if not manifest:

        print("No files found.")

        return

    total_size = 0

    for file_info in manifest.values():

        print(
            f"📄 {file_info['path']}"
        )

        print(
            f"   Size: "
            f"{file_info['size']} bytes"
        )

        print(
            f"   Version: "
            f"{file_info.get('version', 1)}"
        )

        print(
            f"   MD5: "
            f"{file_info['md5']}"
        )

        print()

        total_size += file_info[
            "size"
        ]

    print("-" * 60)

    print(
        f"Files: {len(manifest)}"
    )

    print(
        f"Total size: "
        f"{total_size:,} bytes"
    )

    print("=" * 60)


# ============================================================
# INPUT HELPERS
# ============================================================

def parse_patterns(value):
    """Convert comma-separated patterns into a list."""

    if not value.strip():
        return None

    return [
        pattern.strip()
        for pattern in value.split(",")
        if pattern.strip()
    ]


def ask_encryption():
    """Ask the user whether to encrypt."""

    answer = input(
        "Encrypt backup with AES-256-GCM? (y/n): "
    ).strip().lower()

    if answer not in {
        "y",
        "yes",
    }:

        return False, None

    password = getpass(
        "Encryption password: "
    )

    confirmation = getpass(
        "Confirm password: "
    )

    if password != confirmation:

        raise ValueError(
            "Passwords do not match."
        )

    if not password:

        raise ValueError(
            "Password cannot be empty."
        )

    return True, password


# ============================================================
# INTERACTIVE APPLICATION
# ============================================================

def main():
    """Run the interactive backup utility."""

    print(
        f"💾 BACKUP UTILITY v{BACKUP_VERSION} 💾"
    )

    print()

    print("1. Full backup")
    print("2. Incremental backup")
    print("3. Differential backup")
    print("4. Verify backup")
    print("5. Restore backup")
    print("6. Apply retention policy")
    print("7. Check backup schedule")
    print("8. Display manifest")
    print("9. Exit")

    print()

    choice = input(
        "Select an option: "
    ).strip()

    try:

        # ----------------------------------------------------
        # FULL BACKUP
        # ----------------------------------------------------

        if choice == "1":

            source = input(
                "Source directory: "
            ).strip()

            destination = input(
                "Backup destination: "
            ).strip()

            compression = input(
                "Compression (tar.gz/zip) "
                "[tar.gz]: "
            ).strip().lower()

            if not compression:
                compression = "tar.gz"

            if compression not in {
                "tar.gz",
                "zip",
            }:

                raise ValueError(
                    "Compression must be "
                    "'tar.gz' or 'zip'."
                )

            include_patterns = parse_patterns(
                input(
                    "Include patterns "
                    "(comma-separated, optional): "
                )
            )

            exclude_patterns = parse_patterns(
                input(
                    "Exclude patterns "
                    "(comma-separated, optional): "
                )
            )

            encrypted, password = (
                ask_encryption()
            )

            result = create_full_backup(
                source,
                destination,
                compression=compression,
                encrypted=encrypted,
                password=password,
                include_patterns=include_patterns,
                exclude_patterns=exclude_patterns,
            )

            print()
            print(
                "🔐 BACKUP COMPLETED SUCCESSFULLY"
            )

            print(
                json.dumps(
                    result,
                    indent=4,
                )
            )

        # ----------------------------------------------------
        # INCREMENTAL BACKUP
        # ----------------------------------------------------

        elif choice == "2":

            source = input(
                "Source directory: "
            ).strip()

            destination = input(
                "Backup destination: "
            ).strip()

            previous = input(
                "Previous backup directory: "
            ).strip()

            compression = input(
                "Compression (tar.gz/zip) "
                "[tar.gz]: "
            ).strip().lower()

            if not compression:
                compression = "tar.gz"

            include_patterns = parse_patterns(
                input(
                    "Include patterns "
                    "(comma-separated, optional): "
                )
            )

            exclude_patterns = parse_patterns(
                input(
                    "Exclude patterns "
                    "(comma-separated, optional): "
                )
            )

            encrypted, password = (
                ask_encryption()
            )

            result = create_incremental_backup(
                source,
                destination,
                previous,
                compression=compression,
                encrypted=encrypted,
                password=password,
                include_patterns=include_patterns,
                exclude_patterns=exclude_patterns,
            )

            print(
                json.dumps(
                    result,
                    indent=4,
                )
            )

        # ----------------------------------------------------
        # DIFFERENTIAL BACKUP
        # ----------------------------------------------------

        elif choice == "3":

            source = input(
                "Source directory: "
            ).strip()

            destination = input(
                "Backup destination: "
            ).strip()

            full_backup = input(
                "Full backup directory: "
            ).strip()

            compression = input(
                "Compression (tar.gz/zip) "
                "[tar.gz]: "
            ).strip().lower()

            if not compression:
                compression = "tar.gz"

            include_patterns = parse_patterns(
                input(
                    "Include patterns "
                    "(comma-separated, optional): "
                )
            )

            exclude_patterns = parse_patterns(
                input(
                    "Exclude patterns "
                    "(comma-separated, optional): "
                )
            )

            encrypted, password = (
                ask_encryption()
            )

            result = create_differential_backup(
                source,
                destination,
                full_backup,
                compression=compression,
                encrypted=encrypted,
                password=password,
                include_patterns=include_patterns,
                exclude_patterns=exclude_patterns,
            )

            print(
                json.dumps(
                    result,
                    indent=4,
                )
            )

        # ----------------------------------------------------
        # VERIFY
        # ----------------------------------------------------

        elif choice == "4":

            backup = input(
                "Backup directory to verify: "
            ).strip()

            verify_backup(
                backup
            )

        # ----------------------------------------------------
        # RESTORE
        # ----------------------------------------------------

        elif choice == "5":

            backup = input(
                "Backup directory/archive: "
            ).strip()

            target = input(
                "Restore destination: "
            ).strip()

            selected = input(
                "Selective files "
                "(comma-separated, leave empty for all): "
            ).strip()

            if selected:

                selected_files = [
                    item.strip()
                    for item in selected.split(",")
                    if item.strip()
                ]

            else:

                selected_files = None

            password = None

            if backup.endswith(".enc"):

                password = getpass(
                    "Backup password: "
                )

            restore_backup(
                backup,
                target,
                password=password,
                selected_files=selected_files,
            )

        # ----------------------------------------------------
        # RETENTION
        # ----------------------------------------------------

        elif choice == "6":

            destination = input(
                "Backup destination: "
            ).strip()

            days_input = input(
                "Retention days [30]: "
            ).strip()

            days = (
                int(days_input)
                if days_input
                else 30
            )

            removed = apply_retention_policy(
                destination,
                days,
            )

            print()
            print(
                f"🗑️ Removed backups: "
                f"{len(removed)}"
            )

            for backup_id in removed:

                print(
                    f"   {backup_id}"
                )

        # ----------------------------------------------------
        # SCHEDULE
        # ----------------------------------------------------

        elif choice == "7":

            schedule = input(
                "Schedule (daily/weekly/monthly): "
            ).strip().lower()

            last_backup_text = input(
                "Last backup time "
                "(YYYY-MM-DD HH:MM:SS, "
                "leave empty if none): "
            ).strip()

            if last_backup_text:

                last_backup = datetime.strptime(
                    last_backup_text,
                    "%Y-%m-%d %H:%M:%S",
                )

            else:

                last_backup = None

            due = is_backup_due(
                last_backup,
                schedule,
            )

            print()

            if due:

                print(
                    "⏰ Backup is due."
                )

            else:

                next_time = (
                    get_next_backup_time(
                        last_backup,
                        schedule,
                    )
                )

                print(
                    "⏳ Backup is not due yet."
                )

                print(
                    f"Next backup: "
                    f"{next_time}"
                )

        # ----------------------------------------------------
        # MANIFEST
        # ----------------------------------------------------

        elif choice == "8":

            manifest_file = input(
                "Manifest JSON file: "
            ).strip()

            manifest = load_manifest(
                manifest_file
            )

            display_manifest(
                manifest
            )

        # ----------------------------------------------------
        # EXIT
        # ----------------------------------------------------

        elif choice == "9":

            print(
                "Goodbye."
            )

            return

        else:

            print(
                "❌ Invalid option."
            )

    except (
        FileNotFoundError,
        NotADirectoryError,
        ValueError,
        OSError,
    ) as error:

        print()
        print(
            f"❌ {error}"
        )


if __name__ == "__main__":
    main()