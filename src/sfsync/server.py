# src/sfsync/server.py
"""Lightweight TCP server that receives files sent by the client."""

import argparse
import sys
import threading
import socket
from pathlib import Path

from .transport import recv_file


def handle_client(conn, addr, storage_dir: Path):
    """Receive one file from the client and persist it inside ``storage_dir``."""
    try:
        print(f"[TCP] Connected {addr}")
        saved = recv_file(conn, storage_dir)
        print(f"Received {saved} from {addr}")
    except Exception as e:
        print("client handler error:", e)
    finally:
        conn.close()

def run_server(host: str, port: int, storage_dir: Path):
    """Start a blocking server loop that accepts connections on ``host:port``."""
    storage_dir.mkdir(parents=True, exist_ok=True)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(5)
        print(f"Listening on {host}:{port}")
        while True:
            conn, addr = s.accept()
            t = threading.Thread(
                target=handle_client,
                args=(conn, addr, storage_dir),
                daemon=True,
            )
            t.start()
            
def parse_args(argv: list[str]) -> argparse.Namespace:
    """Parse CLI flags for the server entrypoint."""
    parser = argparse.ArgumentParser(description="SFSync TCP server")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=5050)
    parser.add_argument(
        "--dest",
        type=Path,
        default=Path("uploads"),
        help="Directory to store incoming files",
    )
    return parser.parse_args(argv)

def main(argv: list[str] | None = None) -> int:
    """CLI entrypoint wrapper around :func:`run_server`."""
    args = parse_args(argv or sys.argv[1:])
    try:
        run_server(args.host, args.port, args.dest)
    except OSError as exc:
        print(f"Failed to start server: {exc}", file=sys.stderr)
        return 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
