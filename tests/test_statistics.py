import pytest

from pixeldiet.statistics import format_bytes, savings_percent


@pytest.mark.parametrize(("size", "expected"), [(0, "0 B"), (999, "999 B"), (1500, "1.5 KB"), (1_250_000, "1.25 MB")])
def test_format_bytes(size, expected):
    assert format_bytes(size) == expected


def test_savings_percent():
    assert savings_percent(1000, 250) == 75


def test_savings_percent_for_empty_file():
    assert savings_percent(0, 0) == 0
