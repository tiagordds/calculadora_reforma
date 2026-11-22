"""Bounded synthetic HTTP campaign against the project's loopback development servers."""
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import json
from math import ceil
from pathlib import Path
from time import perf_counter

import requests


TRADITIONAL = dict(edition="sn-03-02", period="2027-03", opening="2023-01", activity="retail",
                   place="local", profile="ordinary", standing="unknown", unit="monthly",
                   income="100000", revenue="100000", accept_history="yes", mode="estimated")
MONTHS = [f"2026-{m:02}" for m in range(2, 13)] + ["2027-01"]
REFINED = dict(TRADITIONAL, mode="real", **{"month_" + m: "100000" for m in MONTHS})
REFINED["month_2026-02"] = "80000"
PARTIAL = dict(TRADITIONAL, edition="comparison-04-01", accept_history="on", history_basis="unknown",
               exclusion_origin="unknown", option_status="unknown", decision_date="2027-03-01",
               refund="unknown", supplier="unknown", credit_rule="unknown", credit_origin="unknown",
               buyer="unknown")
CASES = {
    "home": ("/", None, "Como os tributos da loja mudam?"),
    "traditional": ("/simples/tradicional/", TRADITIONAL, "R$ 8.825,00"),
    "complete": ("/simples/comparar/", {"example": "middle"}, "R$ 14.202,31"),
    "partial": ("/simples/comparar/", PARTIAL, "Comparação após créditos em aberto"),
    "refinement": ("/simples/tradicional/", REFINED, "R$ 8.793,22"),
    "operation": ("/operacao/caneta/", {"confirm_cbs": "yes"}, "R$ 10,10"),
}


def worker(origin, case, count):
    path, fields, expected = CASES[case]
    results = []
    with requests.Session() as session:
        session.trust_env = False
        url = origin + path
        if fields is not None:
            session.get(url, timeout=8).raise_for_status()
            fields = dict(fields, csrfmiddlewaretoken=session.cookies["csrftoken"])
        for _ in range(count):
            start = perf_counter()
            response = session.request("POST" if fields else "GET", url, data=fields,
                                       allow_redirects=False, timeout=8)
            elapsed = perf_counter() - start
            if response.status_code == 200:
                assert expected in response.text, case
            elif case != "operation" or response.status_code != 429 or "ocupado" not in response.text:
                raise RuntimeError(f"{case}: unexpected HTTP {response.status_code}")
            results.append((response.status_code, elapsed))
    return results


def measure(origin, case, concurrency):
    started = perf_counter()
    with ThreadPoolExecutor(max_workers=concurrency) as pool:
        batches = [pool.submit(worker, origin, case, 100 // concurrency) for _ in range(concurrency)]
        records = [r for batch in batches for r in batch.result()]
    seconds = perf_counter() - started
    times = sorted(t for status, t in records if status == 200)
    return dict(case=case, concurrency=concurrency, http=dict(Counter(s for s, _ in records)),
                duration_s=round(seconds, 3), success_per_s=round(len(times) / seconds, 2),
                p50_ms=round(1000 * times[ceil(.50 * len(times)) - 1], 2),
                p95_ms=round(1000 * times[ceil(.95 * len(times)) - 1], 2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, choices=[8003, 8055], required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    origin = f"http://127.0.0.1:{args.port}"
    with args.output.open("w", encoding="utf-8") as output:
        for case in CASES:
            worker(origin, case, 2)
            for concurrency in (1, 2, 4):
                print(json.dumps(measure(origin, case, concurrency)), file=output, flush=True)
