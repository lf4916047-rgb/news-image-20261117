#!/usr/bin/env python3
"""The news-image-20261117 entry program.

The repository ships a finished poster, ``entry.png`` — a one-page
illustrated front page summing up the world news of Tuesday
17 November 2026 (see NEWS_SOURCES.md for the reporting behind it and
art/poster.html for the drawing it was rendered from).

At grading time this program runs offline in a sandbox. It locates
the shipped image, verifies that the bytes really are a PNG or JPEG
within the competition's 1 MiB cap, and copies them unchanged to
``$MAKEFUN_OUTPUT_DIR/entry.png``. It writes the same bytes on every
run, so repeated runs agree byte for byte.

Standard library only; Python 3.13.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# The competition's caps: one image, at most 1 MiB, named entry.png.
MAX_IMAGE_BYTES = 1_048_576
OUTPUT_NAME = "entry.png"
SOURCE_NAME = "entry.png"

# Magic numbers: how a PNG and a JPEG announce themselves.
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
JPEG_MAGIC = b"\xff\xd8\xff"


def find_source() -> Path:
    """Return the shipped entry.png.

    Look beside this script first (the sandbox mounts the repository
    read-only and runs the program from its root), then in the
    current working directory, so a plain local run works too.
    """
    beside_script = Path(__file__).resolve().parent / SOURCE_NAME
    if beside_script.is_file():
        return beside_script
    in_cwd = Path.cwd() / SOURCE_NAME
    if in_cwd.is_file():
        return in_cwd
    raise FileNotFoundError(
        f"{SOURCE_NAME} not found next to main.py or in the working directory"
    )


def image_format(data: bytes) -> str:
    """Identify the image format from its first bytes.

    Returns "PNG" or "JPEG"; raises ValueError for anything else,
    because the grader tells the two apart by exactly these bytes.
    """
    if data.startswith(PNG_MAGIC):
        return "PNG"
    if data.startswith(JPEG_MAGIC):
        return "JPEG"
    raise ValueError("entry.png is neither a PNG nor a JPEG (bad magic bytes)")


def verify(data: bytes) -> str:
    """Check the image against the competition's rules.

    Returns the detected format once the size cap and the signature
    have both been confirmed.
    """
    if not data:
        raise ValueError("entry.png is empty")
    if len(data) > MAX_IMAGE_BYTES:
        raise ValueError(
            f"entry.png is {len(data)} bytes, over the {MAX_IMAGE_BYTES}-byte cap"
        )
    return image_format(data)


def main() -> int:
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "out"))
    source = find_source()
    data = source.read_bytes()
    fmt = verify(data)

    output_dir.mkdir(parents=True, exist_ok=True)
    target = output_dir / OUTPUT_NAME
    target.write_bytes(data)

    print(
        f"entry.png: copied {len(data)} bytes of verified {fmt} "
        f"from {source} to {target}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
