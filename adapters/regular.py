import json
import os
import subprocess
import sys
from threading import BoundedSemaphore
from time import monotonic

from .manifest import EngineError, ROOT

BUDGET = 5.0
_SLOTS = BoundedSemaphore(2)


def call(payload, *, deadline=None, instance=None):
    """One local Django process. Reject excess work before creating a worker."""
    if deadline is None:
        deadline = monotonic() + BUDGET
    if not _SLOTS.acquire(blocking=False):
        raise EngineError("busy")
    try:
        executable = sys.executable
        env = None
        if os.name == "nt":
            # Own the interpreter PID directly so kill() also closes the pipes.
            executable = sys._base_executable
            env = {**os.environ, "__PYVENV_LAUNCHER__": sys.executable}
        with subprocess.Popen(
            [executable, "-m", "adapters.transport"], cwd=ROOT, env=env,
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
        ) as worker:
            try:
                message = json.dumps({"payload": payload, "instance": instance}).encode("ascii")
                output, _ = worker.communicate(message, timeout=max(0, deadline - monotonic()))
            except subprocess.TimeoutExpired:
                worker.kill()
                worker.communicate()
                raise EngineError("timeout") from None
            if worker.returncode:
                raise EngineError("contract")
        result = json.loads(output)
        if "error" in result:
            raise EngineError(result["error"])
        if monotonic() >= deadline:
            raise EngineError("timeout")
        return result
    finally:
        _SLOTS.release()
