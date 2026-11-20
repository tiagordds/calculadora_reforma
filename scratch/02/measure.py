"""Measure end-to-end latency of the synthetic C03 on the native Django server."""
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import json
from math import ceil
from time import perf_counter

import requests


URL = "http://127.0.0.1:8002/operacao/caneta/"


def submit(count):
    with requests.Session() as session:
        session.trust_env = False
        session.get(URL, timeout=5).raise_for_status()
        fields = {"confirm_cbs": "yes", "csrfmiddlewaretoken": session.cookies["csrftoken"]}
        results = []
        for _ in range(count):
            start = perf_counter()
            reply = session.post(URL, data=fields, timeout=7, allow_redirects=False)
            elapsed = perf_counter() - start
            if reply.status_code == 200:
                assert "R$ 10,10" in reply.text
            else:
                assert reply.status_code == 429 and "ocupado" in reply.text
            results.append((reply.status_code, elapsed))
        return results


if __name__ == "__main__":
    for concurrency in (1, 4):
        start = perf_counter()
        with ThreadPoolExecutor(concurrency) as pool:
            results = [entry for group in pool.map(submit, [100 // concurrency] * concurrency)
                       for entry in group]
        duration = perf_counter() - start
        times = sorted(elapsed for status, elapsed in results if status == 200)
        print(json.dumps({
            "concurrency": concurrency, "http": dict(Counter(code for code, _ in results)),
            "successful_p50_s": round(times[ceil(.50 * len(times)) - 1], 3),
            "successful_p95_s": round(times[ceil(.95 * len(times)) - 1], 3),
            "successful_per_s": round(len(times) / duration, 2),
        }), flush=True)
