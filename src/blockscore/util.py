from __future__ import annotations

from fractions import Fraction
import re


def parse_fraction(value) -> Fraction:
    if isinstance(value, Fraction):
        return value
    if isinstance(value, int):
        return Fraction(value, 1)
    if isinstance(value, float):
        return Fraction(str(value))
    text = str(value).strip()
    if "/" in text:
        a, b = text.split("/", 1)
        return Fraction(int(a), int(b))
    return Fraction(text)


def round_fraction(value: Fraction) -> int:
    """Round to nearest integer, halves away from zero, deterministically."""
    if value >= 0:
        return (value.numerator * 2 + value.denominator) // (2 * value.denominator)
    return -round_fraction(-value)


def safe_id(value: str, fallback: str = "blockscore") -> str:
    value = re.sub(r"[^a-z0-9_.-]+", "_", value.lower()).strip("_.-")
    return value or fallback


def scoreboard_objective(namespace: str) -> str:
    # Keep legacy-safe objective names <=16 chars.
    return ("bs_" + safe_id(namespace).replace(".", "_").replace("-", "_"))[:16]
