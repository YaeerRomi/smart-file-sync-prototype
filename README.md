# Smart File Sync — Socket Prototype

This is the early-stage prototype of my Smart File Sync system.  
It focuses on understanding the **core mechanics** of file synchronization before migrating to a REST-based design.

## Features Implemented
✅ File hashing for change detection  
✅ Basic file monitoring system  
✅ TCP socket server and client for file transfer

## Planned / In Progress
- [ ] Combine hashing + socket transfer into one pipeline  
- [ ] Add acknowledgment and retry mechanism  
- [ ] Improve file metadata handling  
- [ ] Migrate to FastAPI (Phase 2)

## Purpose
This version was built to explore **low-level networking, concurrency, and data integrity** before building a full production version.

## Usage

1. Create a virtual environment and install your dependencies (none are required for this core prototype but a venv keeps things tidy):
   ```bash
   python -m venv .venv && source .venv/bin/activate
   pip install -U pip
   ```
2. Start the TCP server so it can accept uploads. By default files are written under `uploads/`.
   ```bash
   python -m sfsync.server --host 0.0.0.0 --port 5050 --dest uploads
   ```
3. In another terminal, run the client and point it to a file you want to sync:
   ```bash
   python -m sfsync.client --host 127.0.0.1 --port 5050 --file examples/test_files/test_file.txt
   ```
4. The server log will note each connection and where the file was saved.

### Configuration flags

- `--host` / `--port`: override the bind/connect target for server or client.
- `--dest`: server option to change the folder where incoming files are stored.
- `--file`: client option that specifies which file to upload.

The server is multi-threaded so it can accept concurrent uploads, and the client will stream file contents in chunks to handle large files.
