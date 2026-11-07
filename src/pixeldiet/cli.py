"""Command line interface."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from PIL import Image

from .compressor import compress_image
from .formats import extension_for, supported_formats
from .statistics import format_bytes, savings_percent

SIZE_PATTERN = re.compile(r"^\s*(\d+(?:\.\d+)?)\s*(B|KB|KIB|MB|MIB)?\s*$", re.IGNORECASE)


def parse_size(value: str) -> int:
    match = SIZE_PATTERN.match(value)
    if not match:
        raise argparse.ArgumentTypeError("Use a size such as 500KB, 1MB, or 200000B")
    number = float(match.group(1))
    unit = (match.group(2) or "B").upper()
    factor = {"B": 1, "KB": 1000, "KIB": 1024, "MB": 1_000_000, "MIB": 1_048_576}[unit]
    size = int(number * factor)
    if size < 1:
        raise argparse.ArgumentTypeError("Target size must be at least 1 byte")
    return size


def _images(path: Path):
    if path.is_file():
        yield path
        return
    for item in sorted(path.rglob("*")):
        if not item.is_file():
            continue
        try:
            with Image.open(item):
                yield item
        except (OSError, Image.DecompressionBombError):
            continue


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="pixeldiet", description="Compress images to a maximum file size.")
    parser.add_argument("input", type=Path, help="Image file or folder to process")
    parser.add_argument("--target", required=True, type=parse_size, help="Maximum output size (e.g. 500KB, 1MB)")
    formats = {fmt.lower() for fmt in supported_formats()} | {"jpg", "jpeg", "tif", "tiff"}
    parser.add_argument("--format", type=str.lower, choices=tuple(sorted(formats)),
                        help="Output format (defaults to the input format)")
    parser.add_argument("--output", type=Path, help="Output file for one image, or output folder for a directory")
    parser.add_argument("--verbose", action="store_true", help="Show per-image size and savings")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not args.input.exists():
        parser.error(f"Input does not exist: {args.input}")
    if args.input.is_dir() and args.output and args.output.exists() and args.output.is_file():
        parser.error("For a directory input, --output must be a directory")
    paths = list(_images(args.input))
    if not paths:
        print("No readable images found.", file=sys.stderr)
        return 1
    totals_before = totals_after = count = failures = 0
    for source in paths:
        try:
            output = None
            if args.output:
                suffix = extension_for((args.format or source.suffix.lstrip(".")).upper())
                if args.input.is_dir():
                    output = args.output / source.relative_to(args.input).parent / f"{source.stem}.optimized{suffix}"
                else:
                    output = args.output
            result = compress_image(source, args.target, output, args.format)
            count += 1
            totals_before += result.original_bytes
            totals_after += result.output_bytes
            if args.verbose or not result.reached_target:
                status = "target met" if result.reached_target else "target unreachable at minimum quality/resolution"
                resized = ", resized" if result.resized else ""
                print(f"{source} -> {result.output}: {format_bytes(result.original_bytes)} -> "
                      f"{format_bytes(result.output_bytes)} ({savings_percent(result.original_bytes, result.output_bytes):.1f}% saved, {status}{resized})")
        except (OSError, ValueError) as exc:
            failures += 1
            print(f"Error: {source}: {exc}", file=sys.stderr)
    if args.verbose:
        print(f"Processed {count} image(s): {format_bytes(totals_before)} -> {format_bytes(totals_after)} "
              f"({savings_percent(totals_before, totals_after):.1f}% saved).")
    return 1 if failures or not count else 0


if __name__ == "__main__":
    raise SystemExit(main())
