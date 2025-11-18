# src/sfsync/config.py
"""Shared constants that describe the wire format."""

from typing import Final

HEADER_FMT: Final[str] = "!I Q"  # e.g., name_len (uint32), file_size (uint64)
HEADER_SIZE: Final[int] = 4 + 8  # computed from struct.calcsize if you prefer
