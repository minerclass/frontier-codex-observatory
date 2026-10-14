"""Serve only the generated observatory at http://127.0.0.1:8766.

This always binds to loopback, disables directory listings, and blocks dotfiles,
repository metadata, traversal, and symlinks that leave the generated directory.
Run: python tools/serve.py --output dist --port 8767
"""

from __future__ import annotations

import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit

from build import resolve_output
from validate_data import DEFAULT_ROOT, ValidationError


PUBLIC_EXTENSIONS = {".html", ".css", ".js", ".json", ".svg", ".png", ".jpg", ".jpeg",
                     ".webp", ".gif", ".ico", ".woff", ".woff2"}


class ObservatoryHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, directory: str, **kwargs):
        self.output_root = Path(directory).resolve()
        super().__init__(*args, directory=str(self.output_root), **kwargs)

    def validated_path(self, request_path: str) -> Path | None:
        try:
            path = unquote(urlsplit(request_path).path)
        except (ValueError, UnicodeError):
            return None
        if not path.startswith("/") or "\\" in path or "\x00" in path:
            return None
        parts = [part for part in path.split("/") if part]
        if any(part.startswith(".") or ":" in part for part in parts):
            return None
        try:
            candidate = self.output_root.joinpath(*parts).resolve()
        except (OSError, ValueError):
            return None
        if not candidate.is_relative_to(self.output_root):
            return None
        if candidate.is_dir():
            index = (candidate / "index.html").resolve()
            if not index.is_relative_to(self.output_root) or not index.is_file():
                return None
        elif candidate.suffix.lower() not in PUBLIC_EXTENSIONS:
            return None
        return candidate

    def translate_path(self, path: str) -> str:
        candidate = self.validated_path(path)
        # send_head denies invalid requests before the base handler uses this.
        return str(candidate if candidate else self.output_root / ".blocked-resource")

    def send_head(self):
        if self.validated_path(self.path) is None:
            self.send_error(404, "Resource not available")
            return None
        return super().send_head()

    def list_directory(self, path):
        self.send_error(404, "Directory listing is disabled")
        return None

    def end_headers(self):
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()


def create_server(output: Path, port: int = 8766) -> ThreadingHTTPServer:
    output = Path(output).resolve()
    for required in ("index.html", "data.json", "notes.html"):
        target = (output / required).resolve()
        if not target.is_relative_to(output) or not target.is_file():
            raise ValidationError(f"generated observatory is incomplete: {required}; run the builder first")
    return ThreadingHTTPServer(("127.0.0.1", port), partial(ObservatoryHandler, directory=str(output)))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT, help="Repository root (default: parent of tools)")
    parser.add_argument("--output", type=Path, help="Generated observatory directory (default: <root>/dist)")
    parser.add_argument("--port", type=int, default=8767, help="Loopback port (default: 8767)")
    args = parser.parse_args()
    if not 1 <= args.port <= 65535:
        parser.error("port must be between 1 and 65535")
    try:
        output = resolve_output(args.root, args.output)
        server = create_server(output, args.port)
    except (ValueError, OSError) as error:
        parser.exit(1, f"Cannot serve: {error}\n")
    print(f"Serving {output} at http://127.0.0.1:{args.port}/ (Ctrl+C to stop)", flush=True)
    try:
        server.serve_forever(poll_interval=0.25)
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
