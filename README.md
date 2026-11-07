# PixelDiet

PixelDiet compresses images toward a per-file size limit while keeping the original files safe. It uses Pillow's installed image decoders and encoders, searches JPEG/WebP quality settings automatically, and reduces dimensions when needed.

## Install

Requires Python 3.12 or newer.

```bash
python -m pip install -e ".[dev]"
```

## Use

```bash
pixeldiet photo.jpg --target 500KB
pixeldiet ./photos --target 1MB --verbose
pixeldiet photo.png --target 300KB --format webp
```

Sizes accept bytes (`B`), decimal kilobytes/megabytes (`KB`, `MB`), or binary units (`KiB`, `MiB`). Folder input is recursive; each image receives the same maximum size. Output files use an `.optimized` suffix next to each source. `--output` selects a destination file for one input or a destination directory for a folder.

The original is never overwritten. By default output keeps the source format; `--format` converts it. Pillow determines which decoders/encoders are available in the installed environment. Animated images and multi-page TIFFs currently use their first frame/page. JPEG and WebP quality is searched from 20 to 95. Other formats use encoder optimization, then dimension reduction. If the target remains impossible at the minimum quality and 64-pixel minimum dimension, PixelDiet keeps the best result and reports that the target was not reached.

## GitHub Actions

The workflow in `.github/workflows/tests.yml` runs the test suite on pushes and pull requests. To run it locally:

```bash
python -m pytest
```

## Git commands

Run these from the project folder. Replace the remote URL with your GitHub repository URL when setting up `origin` for the first time.

```bash
git status
git add README.md pyproject.toml src tests .github
git commit -m "Add image compression tests and CI workflow"
git push
```

Other commit message examples:

```text
Add target size parsing tests
Cover image format conversion
Configure GitHub Actions for Python 3.12
Document PixelDiet installation and usage
```
