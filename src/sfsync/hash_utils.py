# src/sfsync/hash_utils.py
"""Utility helpers to compute streaming hashes for large files."""

from pathlib import Path
import hashlib

CHUNK_BYTES = 8192

def hash_file(path: Path, algo: str = "sha256") -> str:
    """
    Stream the file and return the hex digest (lowercase).
    Raises FileNotFoundError on missing files.
    """
    h = hashlib.new(algo)
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(CHUNK_BYTES), b""):
            h.update(chunk)
    return h.hexdigest()
