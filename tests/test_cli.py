import pytest
from argparse import ArgumentTypeError

from pixeldiet.cli import parse_size


@pytest.mark.parametrize(
    ("value", "expected"),
    [("500KB", 500_000), ("1MB", 1_000_000), ("1MiB", 1_048_576), ("2048B", 2048), ("2.5KB", 2500)],
)
def test_parse_size(value, expected):
    assert parse_size(value) == expected


@pytest.mark.parametrize("value", ["", "abc", "-1MB", "0B", "10GB"])
def test_parse_size_rejects_invalid_values(value):
    with pytest.raises(ArgumentTypeError):
        parse_size(value)
