#!/usr/bin/env python3
"""Serves the GIT website and stores contact-form submissions in contacts.txt (CSV).
Run:  python3 server.py   then open http://localhost:8000
No third-party packages required."""
import csv, json, os, threading
from datetime import datetime, timezone
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.abspath(__file__))
FILE = os.path.join(ROOT, "contacts.txt")
FIELDS = ["timestamp_utc", "name", "email", "phone", "company", "product_interest", "message"]
LIMITS = {"name": 100, "email": 150, "phone": 40, "company": 120, "product": 120, "message": 2000}
HIDDEN = {os.path.realpath(p) for p in (FILE, __file__, os.path.join(ROOT, "build.py"))}
lock = threading.Lock()

def clean(v, n):
    v = str(v or "").strip()[:n]
    # Neutralise spreadsheet formula injection
    return "'" + v if v[:1] in ("=", "+", "-", "@") else v

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=ROOT, **k)

    def _blocked(self):  # never expose stored data or source files
        return os.path.realpath(self.translate_path(self.path)) in HIDDEN

    def do_GET(self):
        if self._blocked():
            return self.send_error(404)
        super().do_GET()

    def do_HEAD(self):
        if self._blocked():
            return self.send_error(404)
        super().do_HEAD()

    def do_POST(self):
        if self.path not in ("/contact", "/contact.php"):  # same endpoint name as the PHP version
            return self.send_error(404)
        try:
            size = int(self.headers.get("Content-Length", 0))
            if size > 10_000:
                raise ValueError
            d = json.loads(self.rfile.read(size))
            row = {k: clean(d.get(k), n) for k, n in LIMITS.items()}
            if not row["name"] or "@" not in row["email"] or not row["message"]:
                raise ValueError
        except Exception:
            return self.send_error(400, "Invalid data")
        new = not os.path.exists(FILE)
        with lock, open(FILE, "a", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            if new:
                w.writerow(FIELDS)
            w.writerow([datetime.now(timezone.utc).isoformat(timespec="seconds"), row["name"], row["email"],
                        row["phone"], row["company"], row["product"], row["message"]])
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"ok":true}')

if __name__ == "__main__":
    print("GIT website running at http://localhost:8000  (Ctrl+C to stop)")
    ThreadingHTTPServer(("127.0.0.1", 8000), Handler).serve_forever()
