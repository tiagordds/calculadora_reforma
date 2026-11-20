from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread
from time import monotonic, sleep

import pytest

from adapters import regular
from adapters.manifest import EngineError


def test_slots_reject_without_queue():
    with regular._SLOTS, regular._SLOTS:
        with pytest.raises(EngineError, match="ocupado"):
            regular.call({})


@pytest.mark.parametrize("idle", [False, True], ids=["global", "idle"])
def test_web_deadline(monkeypatch, client, idle):
    """A real, local HTTP body either trickles within the idle limit or stalls."""
    class SlowBody(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            try:
                if idle:
                    sleep(3)
                for _ in range(30):
                    self.wfile.write(b" ")
                    self.wfile.flush()
                    sleep(.25)
                self.wfile.write(b"{}")
            except OSError:
                pass

        def log_message(self, *args):
            pass

    with ThreadingHTTPServer(("127.0.0.1", 0), SlowBody) as server:
        thread = Thread(target=server.serve_forever, daemon=True)
        thread.start()
        child = (
            "from adapters import transport as t; from types import SimpleNamespace; "
            f"t.ORIGIN='http://127.0.0.1:{server.server_port}'; "
            "s=t.EngineSession(); s.trust_env=False; t.verify_artifacts=lambda:None; "
            "t.READY=SimpleNamespace(read_text=lambda **k:'instance-test'); "
            "t.exchange=lambda payload, credentials:t.read_json(s,'/'); t.main()"
        )
        spawn = regular.subprocess.Popen

        def start(args, **kwargs):
            return spawn([args[0], "-c", child], **kwargs)

        monkeypatch.setattr(regular.subprocess, "Popen", start)
        started = monotonic()
        try:
            result = client.post("/operacao/caneta/", "confirm_cbs=yes",
                                 content_type="application/x-www-form-urlencoded")
            elapsed = monotonic() - started
            print(f"POST deadline (idle={idle}): {elapsed:.3f} s")
            assert result.status_code == 503 and "excedeu o prazo" in result.content.decode()
            if idle:
                assert 2 <= elapsed < 4
            else:
                assert 4.7 <= elapsed < 5
        finally:
            server.shutdown()
