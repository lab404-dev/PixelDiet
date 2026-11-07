from pathlib import Path

import pytest
from PIL import Image

from pixeldiet.formats import resolve_format


@pytest.mark.parametrize(("suffix", "expected"), [("jpg", "JPEG"), ("png", "PNG"), ("webp", "WEBP"),
                                                    ("tiff", "TIFF"), ("gif", "GIF"), ("bmp", "BMP")])
def test_resolve_common_formats(suffix: str, expected: str):
    assert resolve_format(None, Path(f"image.{suffix}")) == expected


def test_pillow_can_open_test_image():
    assert Image.registered_extensions()[".png"] == "PNG"
