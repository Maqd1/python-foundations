"""Password generation and strength analysis."""

from __future__ import annotations

import hashlib
import math
import random
import re
import secrets
import string
from collections import Counter

from .config import load_words


# ---------- Character sets ----------
LOWERCASE = string.ascii_lowercase
UPPERCASE = string.ascii_uppercase
DIGITS = string.digits
SPECIALS = "!@#$%^&*()-_=+[]{};:,.<>?/"

AMBIGUOUS = set("O0Il1|`'\"")
SIMILAR = set("il1Lo0O")


# ---------- Generator ----------
def _build_charset(
    uppercase: bool = True,
    lowercase: bool = True,
    digits: bool = True,
    specials: bool = True,
    exclude_ambiguous: bool = False,
    exclude_similar: bool = False,
    custom_chars: str | None = None,
) -> str:
    pools = []
    if lowercase:
        pools.append(LOWERCASE)
    if uppercase:
        pools.append(UPPERCASE)
    if digits:
        pools.append(DIGITS)
    if specials:
        pools.append(SPECIALS)
    if custom_chars:
        pools.append(custom_chars)

    chars = "".join(pools)
    if exclude_ambiguous:
        chars = "".join(c for c in chars if c not in AMBIGUOUS)
    if exclude_similar:
        chars = "".join(c for c in chars if c not in SIMILAR)
    return chars


def generate_random(length: int = 16, **options) -> str:
    """Generate a random password using the specified character pools."""
    if length < 1:
        raise ValueError("Length must be >= 1")

    exclude_ambiguous = options.pop("exclude_ambiguous", False)
    exclude_similar = options.pop("exclude_similar", False)
    custom_chars = options.pop("custom_chars", None)

    # Defaults: everything on unless any explicit pool is requested
        # Any True → use ONLY the True pools. None True → all pools on.
    explicit = any(options.get(k) for k in
                   ("uppercase", "lowercase", "digits", "specials"))
    if explicit:
        uppercase = options.get("uppercase", False)
        lowercase = options.get("lowercase", False)
        digits = options.get("digits", False)
        specials = options.get("specials", False)
    else:
        uppercase = lowercase = digits = specials = True

    charset = _build_charset(
        uppercase=uppercase, lowercase=lowercase,
        digits=digits, specials=specials,
        exclude_ambiguous=exclude_ambiguous,
        exclude_similar=exclude_similar,
        custom_chars=custom_chars,
    )
    if not charset:
        raise ValueError("Empty character set after exclusions")

    # Ensure at least one char from each required pool
    required_pools = []
    if uppercase: required_pools.append(UPPERCASE)
    if lowercase: required_pools.append(LOWERCASE)
    if digits:    required_pools.append(DIGITS)
    if specials:  required_pools.append(SPECIALS)
    if custom_chars: required_pools.append(custom_chars)

    required_pools = [
        "".join(c for c in p if c in charset) for p in required_pools
    ]
    required_pools = [p for p in required_pools if p]

    password: list[str] = []
    for pool in required_pools[:length]:
        password.append(secrets.choice(pool))
    while len(password) < length:
        password.append(secrets.choice(charset))

    # Shuffle without using the deterministic `random` module
    secrets.SystemRandom().shuffle(password)
    return "".join(password)


def generate_memorable(words: int = 4, separator: str = "-",
                       capitalize: bool = False, add_number: bool = False) -> str:
    wordlist = load_words()
    chosen = [secrets.choice(wordlist) for _ in range(max(2, words))]
    if capitalize:
        chosen = [w.capitalize() for w in chosen]
    result = separator.join(chosen)
    if add_number:
        result += separator + str(secrets.randbelow(9000) + 1000)
    return result


def generate_pattern(pattern: str) -> str:
    """
    Pattern language:
        L = uppercase letter
        l = lowercase letter
        d = digit
        s = special
        ? = any printable
        \\x = literal x
    """
    out = []
    i = 0
    while i < len(pattern):
        ch = pattern[i]
        if ch == "\\" and i + 1 < len(pattern):
            out.append(pattern[i + 1])
            i += 2
            continue
        if ch == "L":
            out.append(secrets.choice(UPPERCASE))
        elif ch == "l":
            out.append(secrets.choice(LOWERCASE))
        elif ch == "d":
            out.append(secrets.choice(DIGITS))
        elif ch == "s":
            out.append(secrets.choice(SPECIALS))
        elif ch == "?":
            out.append(secrets.choice(UPPERCASE + LOWERCASE + DIGITS + SPECIALS))
        else:
            out.append(ch)
        i += 1
    return "".join(out)


def generate_pin(length: int = 4) -> str:
    if length < 3:
        raise ValueError("PIN must be at least 3 digits")
    return "".join(str(secrets.randbelow(10)) for _ in range(length))


_VOWELS = "aeiou"
_CONSONANTS = "bcdfghjklmnpqrstvwxyz"


def generate_pronounceable(length: int = 8) -> str:
    """Alternate consonant-vowel pairs for pronounceable output."""
    out = []
    while len(out) < length:
        out.append(secrets.choice(_CONSONANTS))
        if len(out) < length:
            out.append(secrets.choice(_VOWELS))
    return "".join(out[:length])


def batch_generate(count: int = 5, **options) -> list[str]:
    return [generate_random(**options) for _ in range(max(1, count))]


# ---------- Strength analysis ----------
COMMON_PASSWORDS = {
    "password", "123456", "12345678", "qwerty", "abc123", "monkey",
    "letmein", "dragon", "111111", "baseball", "iloveyou", "trustno1",
    "sunshine", "master", "welcome", "shadow", "ashley", "football",
    "jesus", "michael", "ninja", "mustang", "password1", "123456789",
    "admin", "root", "guest", "login", "pass", "test",
}


def _charset_size(password: str) -> int:
    size = 0
    if re.search(r"[a-z]", password): size += 26
    if re.search(r"[A-Z]", password): size += 26
    if re.search(r"[0-9]", password): size += 10
    if re.search(r"[^A-Za-z0-9]", password): size += len(SPECIALS)
    return max(size, 1)


def get_entropy(password: str) -> float:
    """Shannon entropy in bits: log2(charset_size) * length."""
    if not password:
        return 0.0
    return round(math.log2(_charset_size(password)) * len(password), 2)


def check_common_passwords(password: str) -> bool:
    return password.lower() in COMMON_PASSWORDS


def calculate_password_complexity(password: str) -> dict:
    return {
        "length": len(password),
        "lowercase": bool(re.search(r"[a-z]", password)),
        "uppercase": bool(re.search(r"[A-Z]", password)),
        "digits": bool(re.search(r"[0-9]", password)),
        "specials": bool(re.search(r"[^A-Za-z0-9]", password)),
        "unique_chars": len(set(password)),
        "repeated_chars": len(password) - len(set(password)),
    }


def check_strength(password: str) -> dict:
    """Return score (0-100), label, issues, improvements."""
    if not password:
        return {
            "score": 0, "label": "EMPTY", "issues": ["Empty password"],
            "improvements": ["Enter a password"],
        }

    score = 0
    issues: list[str] = []
    improvements: list[str] = []

    # Length
    n = len(password)
    score += min(40, n * 2)
    if n < 8:
        issues.append(f"Very short ({n} chars)")
        improvements.append("Increase length to at least 12")
    elif n < 12:
        issues.append(f"Length is short ({n} chars)")
        improvements.append("Increase length to 16+")
    elif n < 16:
        improvements.append("Consider 16+ characters for high security")
    else:
        score += 5

    # Character classes
    complexity = calculate_password_complexity(password)
    classes = sum([complexity["lowercase"], complexity["uppercase"],
                   complexity["digits"], complexity["specials"]])
    score += classes * 8
    if not complexity["uppercase"]:
        issues.append("No uppercase letters")
        improvements.append("Add uppercase letters")
    if not complexity["digits"]:
        issues.append("No digits")
        improvements.append("Add digits")
    if not complexity["specials"]:
        issues.append("No special characters")
        improvements.append("Add special characters")

    # Entropy
    entropy = get_entropy(password)
    score += min(15, int(entropy / 10))

    # Common password
    if check_common_passwords(password):
        issues.append("Found in common password list")
        improvements.append("Avoid common words")
        score = max(0, score - 40)

    # Common words inside
    lower = password.lower()
    for word in ("password", "admin", "user", "login", "welcome", "qwerty"):
        if word in lower and word != password.lower():
            issues.append(f"Contains common word '{word}'")
            improvements.append(f"Avoid '{word}'")
            score -= 5

    # Simple sequences
    if re.search(r"(012|123|234|345|456|567|678|789|890|abc|bcd|cde)",
                 lower):
        issues.append("Contains a simple sequence")
        improvements.append("Avoid sequential patterns")
        score -= 10

    # Repeated characters
    if re.search(r"(.)\1{2,}", password):
        issues.append("Contains repeated characters")
        improvements.append("Avoid repeating characters")
        score -= 5

    score = max(0, min(100, score))
    if score >= 90:   label = "VERY STRONG"
    elif score >= 70: label = "STRONG"
    elif score >= 50: label = "MEDIUM"
    elif score >= 30: label = "WEAK"
    else:             label = "VERY WEAK"

    if not improvements:
        improvements.append("Great password!")

    return {
        "score": score,
        "label": label,
        "issues": issues,
        "improvements": improvements,
        "entropy": entropy,
    }


def estimate_crack_time(password: str, guesses_per_second: float = 1e10) -> str:
    """Human-readable time assuming 10 billion guesses/sec."""
    if not password:
        return "instantly"
    entropy = get_entropy(password)
    combos = 2 ** entropy
    seconds = combos / (2 * guesses_per_second)  # average = half the space

    units = [
        ("seconds", 1),
        ("minutes", 60),
        ("hours", 3600),
        ("days", 86400),
        ("years", 31536000),
    ]
    if seconds < 1:
        return "instantly"
    for name, factor in reversed(units):
        if seconds >= factor:
            value = seconds / factor
            if name == "years":
                if value > 1e12:
                    return "practically uncrackable"
                if value > 1e9:
                    return f"{value / 1e9:.1f} billion years"
                if value > 1e6:
                    return f"{value / 1e6:.1f} million years"
                if value > 1e3:
                    return f"{value / 1e3:.1f} thousand years"
            return f"{value:.1f} {name}"
    return "instantly"


def get_weakness_report(password: str) -> dict:
    return check_strength(password)