# PixelDiet

<p align="center">
  <strong>LAB 404 DEV</strong>
  <br>
  <em>Image Optimization Utility</em>
</p>

<p align="center">
  <img src="https://github.com/lab404-dev/.github/blob/main/PixelDiet.png?raw=true" alt="PixelDiet Logo" width="160">
</p>

<p align="center">
  <strong>Compress smarter. Keep originals safe.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-00D9FF?style=flat-square" alt="Version">
  <img src="https://img.shields.io/badge/python-3.12%2B-00D9FF?style=flat-square" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-white?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/status-stable-00D9FF?style=flat-square" alt="Status">
</p>

---

## / 01 — Overview

**PixelDiet** is a command-line image optimization tool developed by **Lab 404 Dev**.

It reduces image file sizes toward a specified per-file limit while preserving the original files. Instead of relying on a single compression setting, PixelDiet automatically searches for suitable JPEG and WebP quality levels and reduces image dimensions when necessary.

Designed for predictable output, batch processing, and straightforward integration into everyday workflows.

## / 02 — Features

- **Target-based compression** — specify the maximum desired file size.
- **Automatic quality search** — searches JPEG and WebP quality settings from 20 to 95.
- **Dimension reduction** — resizes images when quality adjustment is insufficient.
- **Recursive processing** — processes entire directory trees.
- **Format conversion** — convert supported images using `--format`.
- **Safe originals** — source files are never overwritten.
- **Flexible output** — save optimized files beside sources or in a custom destination.
- **Size units** — supports bytes, decimal and binary units.

## / 03 — Installation

**Requirements:** Python 3.12 or newer.

Clone the repository:

```bash
git clone https://github.com/lab404-dev/PixelDiet.git
cd PixelDiet
```

Install the project with development dependencies:

```bash
python -m pip install -e ".[dev]"
```

## / 04 — Usage

### Single image

```bash
pixeldiet photo.jpg --target 500KB
```

### Directory processing

```bash
pixeldiet ./photos --target 1MB --verbose
```

### Format conversion

```bash
pixeldiet photo.png --target 300KB --format webp
```

### Custom output

Use `--output` to select a destination file for a single input or a destination directory for folder processing.

```bash
pixeldiet ./photos --target 500KB --output ./optimized
```

## / 05 — Size Units

PixelDiet accepts the following size units:

| Unit | Description |
|---|---|
| `B` | Bytes |
| `KB` | Decimal kilobytes |
| `MB` | Decimal megabytes |
| `KiB` | Binary kibibytes |
| `MiB` | Binary mebibytes |

For directory input, the specified target applies independently to every image.

## / 06 — Processing Logic

PixelDiet uses Pillow's installed image decoders and encoders.

The optimization pipeline:

1. Reads the source image.
2. Determines the requested output format.
3. Searches JPEG/WebP quality settings where applicable.
4. Reduces dimensions when necessary.
5. Saves the best available result.
6. Reports whether the target size was reached.

Other formats use encoder optimization followed by dimension reduction.

### Processing limitations

- Animated images currently use their first frame.
- Multi-page TIFF files currently use their first page.
- JPEG and WebP quality search is limited to 20–95.
- The minimum image dimension is 64 pixels.
- If the target cannot be reached, PixelDiet preserves the best result and reports that the limit was not achieved.

Pillow determines which image formats are available in the installed environment.

## / 07 — Output & File Safety

By default, optimized files are saved next to their source files with an `.optimized` suffix.

Original files are never overwritten.

When a custom output location is specified, PixelDiet writes the resulting files to that destination.

## / 08 — Project Information

| Property | Value |
|---|---|
| Project | PixelDiet |
| Organization | Lab 404 Dev |
| Version | 1.0.0 |
| Language | Python |
| Minimum Python | 3.12 |
| Main dependency | Pillow |
| Interface | CLI |
| Category | Image Processing |

## / 09 — Links

- **Repository:** [lab404-dev/PixelDiet](https://github.com/lab404-dev/PixelDiet)
- **Organization:** [Lab 404 Dev](https://github.com/lab404-dev)

---

<p align="center">
  <strong>LAB 404 DEV</strong>
  <br>
  <sub>Independent development. Practical tools. No unnecessary complexity.</sub>
</p>
