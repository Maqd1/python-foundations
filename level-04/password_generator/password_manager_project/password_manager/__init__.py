"""Enterprise Password Manager."""
from .core import (
    generate_random, generate_memorable, generate_pattern,
    generate_pin, generate_pronounceable, batch_generate,
    check_strength, get_entropy, estimate_crack_time,
    check_common_passwords, get_weakness_report,
    calculate_password_complexity,
)
from .storage import Vault, History, backup_vault, restore_vault

__version__ = "3.0.0"
__all__ = [
    "generate_random", "generate_memorable", "generate_pattern",
    "generate_pin", "generate_pronounceable", "batch_generate",
    "check_strength", "get_entropy", "estimate_crack_time",
    "check_common_passwords", "get_weakness_report",
    "calculate_password_complexity",
    "Vault", "History", "backup_vault", "restore_vault",
]