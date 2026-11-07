from pixeldiet.optimizer import best_quality
from PIL import Image


def test_best_quality_respects_target_when_possible():
    image = Image.effect_noise((64, 64), 100).convert("RGB")
    data, quality = best_quality(image, "JPEG", 10_000)
    assert len(data) <= 10_000
    assert 20 <= quality <= 95
