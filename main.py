#!/usr/bin/env python3
"""Entrypoint for the Thursday 19 November 2026 front-page entry (v3).

Copies the rendered ``entry.png`` (built by ``gen_image.py``) into the
output directory named by the ``MAKEFUN_OUTPUT_DIR`` environment
variable, defaulting to ``/output``, and verifies the copy landed
there with a non-zero size.

Usage:
    python3 gen_image.py     # render entry.png in this directory first
    python3 main.py          # copy it to $MAKEFUN_OUTPUT_DIR/entry.png
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LOCAL_ENTRY = os.path.join(HERE, "entry.png")


def resolve_output_dir():
    """Read the output directory from the environment, with a default."""
    configured = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    if configured:
        return configured
    return "/output"


def copy_entry(output_dir):
    """Copy entry.png into output_dir and verify the result."""
    if not os.path.isfile(LOCAL_ENTRY):
        raise FileNotFoundError(
            "entry.png not found in %s — run 'python3 gen_image.py' "
            "first to render it." % HERE)
    os.makedirs(output_dir, exist_ok=True)
    destination = os.path.join(output_dir, "entry.png")
    shutil.copyfile(LOCAL_ENTRY, destination)
    if not os.path.isfile(destination):
        raise RuntimeError("copy failed: %s was not created" % destination)
    size = os.path.getsize(destination)
    if size == 0:
        raise RuntimeError("copy failed: %s is empty" % destination)
    return destination, size


def main():
    output_dir = resolve_output_dir()
    try:
        destination, size = copy_entry(output_dir)
    except (FileNotFoundError, RuntimeError, OSError) as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 1
    print("copied entry.png -> %s (%d bytes)" % (destination, size))
    return 0


if __name__ == "__main__":
    sys.exit(main())
