"""Image format helpers backed by Pillow's installed decoders and encoders."""

from pathlib import Path

from PIL import Image

FORMAT_ALIASES = {"jpg": "JPEG", "jpeg": "JPEG", "tif": "TIFF", "tiff": "TIFF"}
EXTENSIONS = {"JPEG": ".jpg", "PNG": ".png", "WEBP": ".webp", "BMP": ".bmp", "TIFF": ".tiff", "GIF": ".gif"}


def supported_formats() -> tuple[str, ...]:
    """Return formats Pillow can currently encode."""
    Image.init()
    return tuple(sorted(Image.SAVE))


def resolve_format(value: str | None, source: Path) -> str:
    """Resolve an explicit format or infer it from a source extension."""
    raw = (value or source.suffix.lstrip(".")).lower()
    fmt = FORMAT_ALIASES.get(raw, raw.upper())
    Image.init()
    if fmt not in Image.SAVE:
        raise ValueError(f"Unsupported output format: {raw}. Available: {', '.join(supported_formats())}")
    return fmt


def extension_for(fmt: str) -> str:
    return EXTENSIONS.get(fmt, "." + fmt.lower())
