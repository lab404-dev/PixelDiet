"""Image compression with target size and a resolution fallback."""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageOps, UnidentifiedImageError

from .formats import extension_for, resolve_format
from .optimizer import LOSSY, best_quality, encode


@dataclass(frozen=True)
class CompressionResult:
    source: Path
    output: Path
    original_bytes: int
    output_bytes: int
    target_bytes: int
    reached_target: bool
    quality: int | None
    resized: bool


def compress_image(source: Path, target_bytes: int, output: Path | None = None, output_format: str | None = None,
                   min_quality: int = 20, min_dimension: int = 64) -> CompressionResult:
    """Compress the first frame/page of an image; source is never overwritten."""
    source = Path(source)
    if target_bytes <= 0:
        raise ValueError("Target size must be greater than zero")
    if not source.is_file():
        raise FileNotFoundError(source)
    fmt = resolve_format(output_format, source)
    if output is None:
        output = source.with_name(f"{source.stem}.optimized{extension_for(fmt)}")
    output = Path(output)
    if source.resolve() == output.resolve():
        raise ValueError("Output path must differ from the source (safe mode)")
    output.parent.mkdir(parents=True, exist_ok=True)
    original_size = source.stat().st_size

    try:
        with Image.open(source) as opened:
            opened.seek(0)
            image = ImageOps.exif_transpose(opened).copy()
    except (UnidentifiedImageError, OSError) as exc:
        raise ValueError(f"Cannot decode image {source}: {exc}") from exc

    quality: int | None = None
    resized = False
    if fmt in LOSSY:
        data, quality = best_quality(image, fmt, target_bytes)
        while len(data) > target_bytes and min(image.size) > min_dimension:
            ratio = min(0.9, math.sqrt(target_bytes / len(data)) * 0.95)
            new_size = tuple(max(min_dimension, int(dim * ratio)) for dim in image.size)
            if new_size == image.size:
                break
            image = image.resize(new_size, Image.Resampling.LANCZOS)
            resized = True
            data, quality = best_quality(image, fmt, target_bytes)
    else:
        data = encode(image, fmt, 95, source_format=None)
        while len(data) > target_bytes and min(image.size) > min_dimension:
            ratio = min(0.9, math.sqrt(target_bytes / len(data)) * 0.95)
            new_size = tuple(max(min_dimension, int(dim * ratio)) for dim in image.size)
            if new_size == image.size:
                break
            image = image.resize(new_size, Image.Resampling.LANCZOS)
            resized = True
            data = encode(image, fmt, 95)

    output.write_bytes(data)
    return CompressionResult(source, output, original_size, len(data), target_bytes,
                             len(data) <= target_bytes, quality, resized)
