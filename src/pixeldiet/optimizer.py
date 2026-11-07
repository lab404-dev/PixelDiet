"""Encoding and size-search routines."""

from __future__ import annotations

from io import BytesIO

from PIL import Image

LOSSY = {"JPEG", "WEBP"}


def encode(image: Image.Image, fmt: str, quality: int, source_format: str | None = None) -> bytes:
    buffer = BytesIO()
    frame = image
    if fmt == "JPEG":
        if frame.mode not in ("RGB", "L"):
            background = Image.new("RGB", frame.size, "white")
            if "A" in frame.getbands():
                background.paste(frame, mask=frame.getchannel("A"))
            else:
                background.paste(frame.convert("RGB"))
            frame = background
        frame.save(buffer, format=fmt, quality=quality, optimize=True, progressive=True)
    elif fmt == "WEBP":
        frame.save(buffer, format=fmt, quality=quality, method=6)
    elif fmt == "PNG":
        frame.save(buffer, format=fmt, optimize=True, compress_level=9)
    elif fmt == "GIF":
        frame.convert("P", palette=Image.Palette.ADAPTIVE, colors=256).save(buffer, format=fmt, optimize=True)
    elif fmt == "TIFF":
        frame.save(buffer, format=fmt, compression="tiff_adobe_deflate")
    else:
        frame.save(buffer, format=fmt)
    return buffer.getvalue()


def best_quality(image: Image.Image, fmt: str, target: int) -> tuple[bytes, int]:
    """Find the highest quality in [20, 95] that fits; otherwise lowest quality."""
    low, high = 20, 95
    candidate = encode(image, fmt, low)
    if len(candidate) > target:
        return candidate, low
    best = candidate
    best_q = low
    while low <= high:
        mid = (low + high) // 2
        data = encode(image, fmt, mid)
        if len(data) <= target:
            best, best_q = data, mid
            low = mid + 1
        else:
            high = mid - 1
    return best, best_q
