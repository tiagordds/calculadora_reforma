"""Local, synthetic comparison journeys using the installed Chrome without JavaScript."""
import argparse
import json
from pathlib import Path

from playwright.sync_api import expect, sync_playwright

from check_traditional import submit


def expand(page, label):
    summary = page.get_by_text(label, exact=True)
    if summary.locator("..").get_attribute("open") is None:
        summary.focus()
        page.keyboard.press("Enter")


def run(origin, output):
    output.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(channel="chrome", headless=True)
        for width, height in ((1366, 900), (320, 720)):
            context = browser.new_context(viewport={"width":width, "height":height}, java_script_enabled=False)
            page = context.new_page()
            requests = []
            page.on("request", lambda req: requests.append((req.method, req.url)))
            page.goto(origin + "/")
            for _ in range(4):
                page.keyboard.press("Tab")
            expect(page.get_by_role("link", name="Comparar Simples tradicional e híbrido")).to_be_focused()
            page.keyboard.press("Enter")
            url = origin + "/simples/comparar/"
            expect(page).to_have_url(url)
            page.locator("#id_revenue").fill("100000")
            page.locator("#id_opening").fill("2023-01")
            for field, code in (("activity", "retail"), ("place", "local"), ("profile", "ordinary")):
                page.locator("#id_" + field).select_option(code)
            page.locator("#id_income").fill("100000")
            page.locator("#id_accept_history").focus()
            page.keyboard.press("Space")
            submit(page, "Comparar as modalidades", 200)
            expect(page.locator(".result")).to_contain_text("R$ 8.825,00")
            expect(page.locator(".result")).to_contain_text("Comparação após créditos em aberto")
            expect(page.locator("#id_exclusions")).to_have_value("")
            for case, label, expected in (("zero", "Sem crédito", "15.717,31"),
                                        ("high", "Alto", "12.687,31"),
                                        ("middle", "Intermediário", "14.202,31")):
                page.goto(url)
                expect(page.locator("#id_cbs_rate")).to_have_value("")
                expect(page.locator("#id_exclusions")).to_have_value("")
                expand(page, "Experimentar o caso sintético da 00B")
                submit(page, label, 200)
                expect(page.locator("#result-heading")).to_be_focused()
                expect(page.locator(".result")).to_contain_text("R$ " + expected)
                expand(page, "Premissas, estados e memória de cálculo")
                expand(page, "Memória JSON para copiar e reproduzir localmente")
                saved = json.loads(page.locator(".result pre").inner_text())
                assert saved["engines"] == [] and saved["inputs"]["example_origin"] == case
                if width == 1366:
                    (output / (case + ".json")).write_text(json.dumps(saved, indent=2, ensure_ascii=False)+"\n",encoding="utf-8")
            page.locator("summary", has_text="Premissas, estados").focus()
            page.keyboard.press("Enter")
            page.locator(".result .options").first.screenshot(path=output / f"modalidades-{width}.png")
            expand(page, "Compras e créditos próprios")
            page.locator("#id_cbs_credit").fill("")
            submit(page, "Comparar as modalidades", 200)
            expect(page.locator(".result")).to_contain_text("Comparação após créditos em aberto")
            expect(page.locator(".result")).to_contain_text("R$ 15.717,31")
            expect(page.locator("#id_exclusions")).to_have_value("2700")
            expand(page, "Compras e créditos próprios")
            page.locator("#id_cbs_credit").fill("1500")
            page.locator("#id_history_basis").select_option("real")
            expand(page, "Históricos próprios e limites anuais")
            for i, field in enumerate(page.locator('input[id^="id_hybrid_202"]').all()):
                field.fill("80000" if i == 0 else "100000")
            submit(page, "Comparar as modalidades", 200)
            expect(page.locator(".result")).to_contain_text("R$ 1.180.000,00")
            expect(page.locator(".result")).to_contain_text("R$ 1.200.000,00")
            expect(page.locator("#id_cbs_credit")).to_have_value("1500")
            page.locator("#id_cbs_rate").fill("10,1234567")
            submit(page, "Comparar as modalidades", 400)
            expect(page.locator("#result-heading")).to_be_focused()
            expect(page.locator("#id_revenue")).to_have_value("100000")
            page.locator("#id_cbs_rate").fill("10")
            page.locator("#id_activity").select_option("service")
            submit(page, "Comparar as modalidades", 200)
            expect(page.locator(".result")).to_contain_text("Fator R")
            expect(page.locator(".result")).to_contain_text("Comparação após créditos em aberto")
            assert all(u.startswith(origin+"/") and "?" not in u for _, u in requests)
            assert sum(m == "POST" for m,_ in requests) == 8
            print(json.dumps(dict(browser=browser.version,width=width,height=height,javascript=False,
                                  posts=8,credits="zero/high/middle/unknown",separate_history=True,
                                  invalid=400,coverage="service excluded",horizontal_overflow=False)))
            context.close()
        browser.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--origin", default="http://127.0.0.1:8005")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    run(args.origin, args.output)
