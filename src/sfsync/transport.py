# src/sfsync/transport.py
"""Shared helpers that implement the binary file transfer protocol."""

import struct
from pathlib import Path
from socket import socket

from .config import HEADER_FMT
from .hash_utils import hash_file

def pack_header(name_len: int, file_size: int) -> bytes:
    """Pack the fixed-width header used to describe the payload."""
    return struct.pack(HEADER_FMT, name_len, file_size)

def send_file(sock: socket, file_path: Path) -> None:
    """
    Send header + filename + file bytes. Uses sendall internally.
    Protocol:
      [header: name_len:uint32, file_size:uint64]
      [filename bytes (utf-8)]
      [file bytes]
    """
    file_size =  file_path.stat().st_size
    filename_bytes = file_path.name.encode("utf-8")
    header = pack_header(len(filename_bytes), file_size)
    sock.sendall(header)
    sock.sendall(filename_bytes)

    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sock.sendall(chunk)

def recv_exact(sock, nbytes) -> bytes:
    """Read exactly ``nbytes`` bytes or raise if the peer disconnects early."""
    buf = bytearray()
    while len(buf) < nbytes:
        chunk = sock.recv(nbytes - len(buf))
        if not chunk:
            raise ConnectionError("socket closed while reading")
        buf.extend(chunk)
    return bytes(buf)

def recv_file(sock, dest_dir: Path) -> Path:
    """Read one file from ``sock`` and save it inside ``dest_dir``."""
    header = recv_exact(sock, struct.calcsize(HEADER_FMT))
    name_len, file_size = struct.unpack(HEADER_FMT, header)
    filename = recv_exact(sock, name_len).decode("utf-8")
    dest = dest_dir / filename

    with open(dest, "wb") as f:
        remaining = file_size
        while remaining:
            chunk = sock.recv(min(8192, remaining))
            if not chunk:
                raise ConnectionError("socket closed while receiving file")
            f.write(chunk)
            remaining -= len(chunk)

    return dest
