# src/sfsync/client.py
"""Simple CLI client that streams a local file to the TCP server."""

import argparse
import socket
import sys
from pathlib import Path

from .transport import send_file


def run_client(host: str, port: int, file_path: Path) -> None:
    """Connect to the server and push the contents of ``file_path``."""
    if not file_path.exists():
        raise FileNotFoundError(file_path)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn:
        conn.connect((host, port))
        send_file(conn, file_path)


def parse_args(argv: list[str]) -> argparse.Namespace:
    """Parse CLI flags for the client entrypoint."""
    parser = argparse.ArgumentParser(description="SFSync TCP client")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5050)
    parser.add_argument(
        "--file",
        type=Path,
        required=True,
        help="Path to the file to send",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """CLI entrypoint wrapper around :func:`run_client`."""
    args = parse_args(argv or sys.argv[1:])
    try:
        run_client(args.host, args.port, args.file)
    except FileNotFoundError:
        print(f"file not found: {args.file}", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"socket error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
