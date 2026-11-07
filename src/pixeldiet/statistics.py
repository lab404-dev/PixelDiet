"""Formatting helpers for compression statistics."""


def format_bytes(size: int) -> str:
    if size < 1000:
        return f"{size} B"
    if size < 1_000_000:
        return f"{size / 1000:.1f} KB"
    return f"{size / 1_000_000:.2f} MB"


def savings_percent(before: int, after: int) -> float:
    return (before - after) * 100 / before if before else 0.0
