# 🍪 PixelDiet

<p align="center">
  <strong>LAB 404 DEV</strong>
  <br>
  <em>Freshly baked tools. Carefully optimized pixels.</em>
</p>

<p align="center">
  <img src="https://github.com/lab404-dev/.github/blob/main/PixelDiet.png?raw=true" alt="PixelDiet Logo" width="160">
</p>

<p align="center">
  <strong>Less bytes. Same pixels. No crumbs left behind.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-00D9FF?style=flat-square">
  <img src="https://img.shields.io/badge/python-3.12%2B-00D9FF?style=flat-square">
  <img src="https://img.shields.io/badge/status-stable-00D9FF?style=flat-square">
</p>

---

## 🍪 The Cookie Jar — About

Welcome to **PixelDiet**, another freshly baked utility from **Lab 404 Dev**.

Images can be big. Bytes can be hungry. And nobody likes unnecessary baggage.

PixelDiet is a command-line image optimization tool that reduces image file sizes toward a specified target while keeping original files safe.

It uses Pillow, automatic JPEG/WebP quality search, and dimension reduction to get the job done.

**Our philosophy:** keep the image, lose the excess weight.

---

## 🍪 Ingredients — Features

- Target-based image compression
- Automatic JPEG/WebP quality search
- Dimension reduction when needed
- Recursive folder processing
- Image format conversion
- Safe original file preservation
- Custom output destinations
- Flexible size units

---

## 🍪 Baking Instructions — Installation

Requires Python 3.12 or newer.

```bash
git clone https://github.com/lab404-dev/PixelDiet.git
cd PixelDiet
python -m pip install -e ".[dev]"
```

## 🍪 Recipe Book — Usage

```bash
# Optimize a single image
pixeldiet photo.jpg --target 500KB

# Process an entire directory
pixeldiet ./photos --target 1MB --verbose

# Convert PNG to WebP
pixeldiet photo.png --target 300KB --format webp

# Save results to a custom folder
pixeldiet ./photos --target 500KB --output ./optimized
```

## 🍪 Cookie Sizes — Supported Units

| Unit | Meaning |
|---|---|
| `B` | Bytes |
| `KB` | Decimal kilobytes |
| `MB` | Decimal megabytes |
| `KiB` | Binary kibibytes |
| `MiB` | Binary mebibytes |

Each image in a directory receives the same individual maximum size.

## 🍪 Kitchen Rules — How It Works

1. Loads the source image using Pillow.
2. Determines the requested output format.
3. Searches JPEG/WebP quality settings from 20 to 95.
4. Reduces dimensions if necessary.
5. Saves the best available result.

By default, output keeps the source format; `--format` selects another supported output format. Original files are never overwritten. By default, optimized images are saved beside their source with an `.optimized` suffix. Use `--output` to choose a destination file for one image or a destination folder for directory input. For directory input, the relative folder structure is preserved.

### Known limitations

- Animated images currently use only their first frame.
- Multi-page TIFF files currently use only their first page.
- The minimum image dimension is 64 pixels.
- If the target cannot be reached, PixelDiet keeps the best result and reports that the target was not achieved. `--verbose` prints each image's size change and a batch total; without it, PixelDiet prints only images that miss the target.
- Available formats depend on installed Pillow decoders and encoders.

## 🍪 Bakery Information

| Property | Value |
|---|---|
| Project | PixelDiet |
| Organization | Lab 404 Dev |
| Version | 1.0.0 |
| Language | Python 3.12+ |
| Dependency | Pillow |
| Interface | CLI |
| Category | Image Processing |

## 🍪 Fresh From The Oven — Links

- [GitHub Repository](https://github.com/lab404-dev/PixelDiet)
- [Lab 404 Dev](https://github.com/lab404-dev)

---

<p align="center">
  🍪 <strong>LAB 404 DEV</strong> 🍪
  <br>
  <sub>We bake tools, not excuses.</sub>
</p>
