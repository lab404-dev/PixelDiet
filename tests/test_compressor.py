from pathlib import Path

from PIL import Image

from pixeldiet.compressor import compress_image
import pytest


def test_compress_writes_separate_target_file(tmp_path: Path):
    source = tmp_path / "photo.png"
    Image.new("RGB", (80, 60), "red").save(source)
    original = source.read_bytes()
    result = compress_image(source, 10_000)
    assert source.read_bytes() == original
    assert result.output.exists()
    assert result.reached_target


def test_jpeg_conversion_and_resize(tmp_path: Path):
    source = tmp_path / "photo.bmp"
    Image.effect_noise((256, 256), 100).convert("RGB").save(source)
    result = compress_image(source, 300, output_format="jpeg")
    assert result.output.suffix == ".jpg"
    assert result.output_bytes == result.output.stat().st_size
    assert Image.open(result.output).format == "JPEG"


def test_rejects_overwriting_source(tmp_path: Path):
    source = tmp_path / "photo.png"
    Image.new("RGB", (8, 8), "blue").save(source)
    with pytest.raises(ValueError, match="safe mode"):
        compress_image(source, 10_000, output=source)


def test_rejects_zero_target(tmp_path: Path):
    source = tmp_path / "photo.png"
    Image.new("RGB", (8, 8), "blue").save(source)
    with pytest.raises(ValueError, match="greater than zero"):
        compress_image(source, 0)


def test_supports_webp_output(tmp_path: Path):
    source = tmp_path / "photo.png"
    Image.new("RGB", (32, 32), "green").save(source)
    result = compress_image(source, 20_000, output_format="webp")
    assert result.output.suffix == ".webp"
    assert Image.open(result.output).format == "WEBP"
