"""Exercise the private C08 comparison without JavaScript and export its synthetic replays."""
import argparse
import json
from pathlib import Path

from playwright.sync_api import expect, sync_playwright


def run(origin, output):
    output.mkdir(exist_ok=True, parents=True)
    with sync_playwright() as driver:
        browser = driver.chromium.launch(channel="chrome", headless=True)
        for width in (320, 1366):
            context = browser.new_context(viewport={"width": width, "height": 900}, java_script_enabled=False)
            page = context.new_page()
            page.goto(origin + "/simples/servicos/")
            page.get_by_role("link", name="Comparar as duas trajetórias de serviços").click()
            page.get_by_role("button", name="Explorar exemplo com históricos diferentes").click()
            expect(page.locator("#result-heading")).to_be_focused()
            expect(page.locator(".result")).to_contain_text("As trajetórias estão em anexos diferentes")
            expect(page.locator(".result")).to_contain_text("R$ -365,48")
            for name in ("fronteira", "credito-pendente"):
                if name == "credito-pendente":
                    page.get_by_text("Créditos e movimentos de março", exact=True).click()
                    page.locator("#id_cbs_credit").fill("")
                    page.get_by_role("button", name="Comparar trajetórias").click()
                    expect(page.locator(".result")).to_contain_text("A diferença global permanece em aberto")
                    expect(page.locator("#id_hybrid_turnover_2027-01")).to_have_value("90000")
                page.get_by_text("Memória de cálculo, históricos e fontes", exact=True).click()
                assert page.locator("html").evaluate("(el) => el.scrollWidth === el.clientWidth")
                memory = page.locator(".result pre").inner_text()
                assert json.loads(memory)["engines"] == []
                if width == 1366:
                    (output / (name + ".json")).write_text(memory + "\n", encoding="utf8")
            context.close()
        browser.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("origin")
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    run(args.origin, args.output)
