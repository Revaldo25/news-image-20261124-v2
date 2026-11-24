#!/usr/bin/env python3
"""Copy entry.png to the make.fun output directory.

Standard library only. Verifies the copy by comparing file sizes and
SHA-256 digests, and refuses to copy a source that is not a PNG.
"""

import hashlib
import os
import shutil
import sys

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
DST = os.path.join(OUT_DIR, "entry.png")


def main():
    if not os.path.isfile(SRC):
        print(f"missing source image: {SRC}", file=sys.stderr)
        sys.exit(1)
    with open(SRC, "rb") as fh:
        if fh.read(len(PNG_MAGIC)) != PNG_MAGIC:
            print(f"source is not a PNG file: {SRC}", file=sys.stderr)
            sys.exit(1)
    os.makedirs(OUT_DIR, exist_ok=True)
    shutil.copyfile(SRC, DST)
    src_size = os.path.getsize(SRC)
    dst_size = os.path.getsize(DST)
    if src_size != dst_size:
        print(f"size mismatch: source {src_size} bytes, "
              f"copy {dst_size} bytes", file=sys.stderr)
        sys.exit(1)
    src_hash = sha256_of(SRC)
    dst_hash = sha256_of(DST)
    if src_hash != dst_hash:
        print(f"sha256 mismatch: source {src_hash}, copy {dst_hash}",
              file=sys.stderr)
        sys.exit(1)
    print(f"copied entry.png ({src_size} bytes, sha256 {src_hash}) "
          f"to {DST}")


if __name__ == "__main__":
    main()
