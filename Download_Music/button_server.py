"""Phone button for run-download-remote.bat. Reachable only from Tailscale (100.64.0.0/10) or this laptop.
Put your token in button_token.txt (one line) next to this file. Open: http://<laptop-tailscale-name>:8088/?token=YOUR_TOKEN
"""
import hmac, ipaddress, subprocess, threading, html, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs

HERE = Path(__file__).parent
PORT = 8088
LOG = HERE / "button_log.txt"
tf = HERE / "button_token.txt"
TOKEN = tf.read_text(encoding="utf-8").strip() if tf.exists() else ""
if len(TOKEN) < 16 or TOKEN.startswith("PASTE"):
    raise SystemExit("Put a token of at least 16 characters in button_token.txt")

TS = ipaddress.ip_network("100.64.0.0/10")
state = {"running": False, "started": None, "finished": None, "code": None}
lock = threading.Lock()

def run():
    with open(LOG, "w", encoding="utf-8", errors="replace") as f:
        p = subprocess.run(["cmd", "/c", "run-download-remote.bat"], cwd=HERE, stdout=f, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL)
    with lock:
        state.update(running=False, finished=time.strftime("%H:%M:%S"), code=p.returncode)

def allowed(ip):
    a = ipaddress.ip_address(ip)
    return a.is_loopback or a in TS

class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def send(self, body, code=200):
        b = body.encode("utf-8")
        self.send_response(code); self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)
    def auth(self):
        if not allowed(self.client_address[0]): self.send("Forbidden", 403); return None
        q = parse_qs(urlparse(self.path).query).get("token", [""])[0]
        if not hmac.compare_digest(q, TOKEN): self.send("Forbidden", 403); return None
        return q
    def page(self, tok):
        with lock: s = dict(state)
        if s["running"]: status = f"Running since {s['started']}... (refresh to update)"
        elif s["finished"]: status = f"Finished at {s['finished']} (exit code {s['code']})"
        else: status = "Idle"
        try: log = LOG.read_text(encoding="utf-8", errors="replace")[-4000:]
        except OSError: log = ""
        dis = "disabled" if s["running"] else ""
        t = html.escape(tok)
        return f"""<!doctype html><meta name=viewport content="width=device-width,initial-scale=1">
<body style="font-family:sans-serif;margin:16px;max-width:600px">
<h2>Music download</h2><p>{html.escape(status)}</p>
<form method=post action="/run?token={t}"><button {dis} style="font-size:22px;padding:18px 28px;width:100%">Download</button></form>
<p><a href="/?token={t}">Refresh</a></p><pre style="white-space:pre-wrap;font-size:12px">{html.escape(log)}</pre></body>"""
    def do_GET(self):
        tok = self.auth()
        if tok is not None: self.send(self.page(tok))
    def do_POST(self):
        tok = self.auth()
        if tok is None: return
        with lock:
            if not state["running"]:
                state.update(running=True, started=time.strftime("%H:%M:%S"), finished=None, code=None)
                threading.Thread(target=run, daemon=True).start()
        self.send_response(303); self.send_header("Location", f"/?token={tok}"); self.end_headers()

ThreadingHTTPServer(("0.0.0.0", PORT), H).serve_forever()
