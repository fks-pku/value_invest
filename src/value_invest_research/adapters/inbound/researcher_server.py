"""Loopback-only, single-project interactive research workbench (stdlib server)."""
import argparse
import fcntl
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import secrets
import shutil
from urllib.parse import urlsplit, unquote

from value_invest_research.application.use_cases.interactive_research import InteractiveResearch
from value_invest_research.adapters.outbound.codex_research_runner import CodexResearchRunner
from value_invest_research.adapters.outbound.filesystem_interactive_research import FileSystemInteractiveResearch

ASSETS = Path(__file__).parents[1] / "outbound/report_templates"


def handler_for(service, project, token):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *_args):
            pass  # No question bodies, tokens or URL query strings in access logs.

        def origin(self):
            return f"http://127.0.0.1:{self.server.server_port}"

        def trusted(self):
            return self.headers.get("Host") == f"127.0.0.1:{self.server.server_port}" and self.headers.get("Sec-Fetch-Site") not in {"cross-site"}

        def respond(self, data, status=200, mime="application/json; charset=utf-8"):
            payload = json.dumps(data, ensure_ascii=False).encode() if isinstance(data, (dict, list)) else data
            if isinstance(payload, str):
                payload = payload.encode()
            self.send_response(status)
            self.send_header("Content-Type", mime)
            self.send_header("Content-Length", str(len(payload)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Referrer-Policy", "no-referrer")
            self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self'; frame-ancestors 'self'; base-uri 'none'; form-action 'none'")
            self.end_headers()
            self.wfile.write(payload)

        def do_GET(self):
            if not self.trusted():
                return self.respond({"error": "仅允许本机同源访问。"}, 403)
            path = unquote(urlsplit(self.path).path)
            try:
                if path == "/":
                    return self.respond((ASSETS / "researcher.html").read_text().replace("__CSRF_TOKEN__", token), mime="text/html; charset=utf-8")
                if path in {"/assets/researcher.js", "/assets/researcher.css"}:
                    name = path.rsplit("/", 1)[1]
                    return self.respond((ASSETS / name).read_bytes(), mime="text/javascript; charset=utf-8" if name.endswith(".js") else "text/css; charset=utf-8")
                if path == "/api/state":
                    state = service.state()
                    job = state["job"]
                    if job:
                        state["job"] = {k: job[k] for k in ("id", "status", "message", "created_at", "updated_at", "proposal") if k in job}
                    state["engine"] = "Codex CLI · 已连接执行适配器" if shutil.which("codex") else "Codex CLI 不可用"
                    return self.respond(state)
                if path == "/api/process":
                    return self.respond(service.process())
                if path in {"/report", "/professional_report.html"}:
                    with service.lock:
                        html = (project / "professional_report.html").read_text()
                    if path == "/report":
                        html = html.replace("</head>", "<style>.report-header,.tree-pane,.audit-footer{display:none}.workspace{display:block}.page{width:100%;padding:0}.detail-pane{border:0;border-radius:0;box-shadow:none;padding:34px 42px}.source-index{margin:20px}body{background:#fffdfa}@media(max-width:760px){.detail-pane{padding:24px 20px}}</style></head>")
                        bridge = "<script>document.addEventListener('click',e=>{const a=e.target.closest('a[href^=\"#\"]');if(a){const id=decodeURIComponent(a.hash.slice(1));if(document.getElementById(id)?.classList.contains('node-detail'))parent.postMessage({type:'research-node',node:id},'*');}});</script>"
                        html = html.replace("</body>", bridge + "</body>")
                    return self.respond(html, mime="text/html; charset=utf-8")
                if path in {"/professional_report.md", "/research_plan.md"}:
                    with service.lock:
                        return self.respond((project / path[1:]).read_bytes(), mime="text/plain; charset=utf-8")
                if path.startswith("/source/"):
                    candidate = (project / path[1:]).resolve()
                    if candidate.is_relative_to(project / "source") and candidate.suffix.lower() == ".pdf" and candidate.is_file():
                        return self.respond(candidate.read_bytes(), mime="application/pdf")
                self.respond({"error": "不存在的资源。"}, 404)
            except (ValueError, OSError, KeyError):
                self.respond({"error": "无法读取研究项目，请检查本地文件。"}, 500)

        def do_POST(self):
            if not self.trusted() or self.headers.get("Origin") != self.origin() or not secrets.compare_digest(self.headers.get("X-Research-Token", ""), token):
                return self.respond({"error": "请求来源校验失败，请从本机研究器页面操作。"}, 403)
            if self.headers.get("Content-Type") != "application/json":
                return self.respond({"error": "只接受 JSON。"}, 415)
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if not 0 < length <= 16000:
                    return self.respond({"error": "请求大小无效。"}, 413)
                request = json.loads(self.rfile.read(length))
                if not isinstance(request, dict):
                    raise ValueError("请求必须是对象。")
                path = urlsplit(self.path).path
                if path == "/api/preview":
                    proposal = service.preview(request)
                    return self.respond({k: proposal[k] for k in ("affected_ids", "research_ids", "rollup_ids", "removed_ids")})
                if path == "/api/research":
                    job = service.submit(request)
                    return self.respond({"id": job["id"], "status": "queued"}, 202)
                if path == "/api/cancel":
                    service.cancel()
                    return self.respond({"ok": True})
                self.respond({"error": "不存在的操作。"}, 404)
            except (ValueError, KeyError) as exc:
                self.respond({"error": str(exc)}, 409)
            except OSError:
                self.respond({"error": "本地写入失败，未启动研究。"}, 500)
    return Handler


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path)
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    project = args.project.resolve()
    if not (project / "question_tree_report.json").is_file():
        parser.error("需要已有 question-tree-v1 研究项目。")
    root = Path(__file__).resolve().parents[4]
    # Hold the OS lock for the entire server lifetime, including recovery.
    (project / ".researcher").mkdir(exist_ok=True)
    with (project / ".researcher/server.lock").open("a") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            parser.error("该项目的研究器已经运行。")
        service = InteractiveResearch(FileSystemInteractiveResearch(project), CodexResearchRunner(root))
        server = ThreadingHTTPServer(("127.0.0.1", args.port), handler_for(service, project, secrets.token_hex(32)))
        print(f"研究器已启动：http://127.0.0.1:{server.server_port} · {project.name}", flush=True)
        try:
            server.serve_forever(poll_interval=.5)
        except KeyboardInterrupt:
            pass
        finally:
            server.server_close()
            service.close()


if __name__ == "__main__":
    main()
