#!/usr/bin/env python3
"""Entry program for news-image-20261124.

Copies the front-page image drawn in this session (entry.png, shipped in
this repository) to the output directory as entry.png, and validates it
before and after the write: PNG magic bytes, a complete PNG (IHDR present,
IEND chunk present at the end), dimensions of at most 1024x1024, and a size
of at most 1 MiB. Standard library only, no network, deterministic: the
same input bytes always produce the same output bytes.
"""
import os
import struct
import sys

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1_048_576
MAX_DIM = 1024


def check_png(data):
    """Return an error string, or None when the bytes are a valid PNG."""
    if len(data) < 8 or data[:8] != PNG_MAGIC:
        return "not a PNG file (bad magic bytes)"
    if len(data) > MAX_BYTES:
        return f"{len(data)} bytes, over the 1 MiB limit"
    if len(data) < 33 or data[12:16] != b"IHDR":
        return "missing IHDR chunk"
    width, height = struct.unpack(">II", data[16:24])
    if width > MAX_DIM or height > MAX_DIM:
        return f"dimensions {width}x{height} exceed 1024x1024"
    if width == 0 or height == 0:
        return "zero width or height"
    if data[-12:] != b"\x00\x00\x00\x00IEND\xaeB`\x82":
        return "missing IEND chunk (truncated PNG)"
    return None


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")

    try:
        with open(src, "rb") as f:
            data = f.read()
    except OSError as exc:
        print(f"error: cannot read entry.png: {exc}", file=sys.stderr)
        return 1

    err = check_png(data)
    if err is not None:
        print(f"error: entry.png invalid: {err}", file=sys.stderr)
        return 1

    with open(dst, "wb") as f:
        f.write(data)

    # Re-read the output and confirm it is byte-identical to the input.
    with open(dst, "rb") as f:
        written = f.read()
    if written != data:
        print("error: output differs from entry.png", file=sys.stderr)
        return 1

    width, height = struct.unpack(">II", data[16:24])
    print(f"wrote {dst} ({len(data)} bytes, {width}x{height} PNG)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
