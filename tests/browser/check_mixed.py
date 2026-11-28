"""Exercise C09 without JavaScript and export the memories shown to the manager."""
import argparse
from pathlib import Path

from playwright.sync_api import expect, sync_playwright


def run(origin, output):
    output.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as driver:
        browser = driver.chromium.launch(channel="chrome", headless=True)
        for width in (320, 1366):
            context = browser.new_context(viewport={"width": width, "height": 900}, java_script_enabled=False)
            page = context.new_page()
            page.goto(origin + "/")
            page.get_by_role("link", name="Estimar o DAS de atividades mistas").click()
            page.get_by_role("button", name="Preencher exemplo de comércio e serviços").click()
            calculate = page.get_by_role("button", name="Calcular o DAS consolidado")
            wages = page.locator("#id_wages_2027-01")
            for value, annex, das in (("20000", "iii", "10.507,00"), ("19999,99", "v", "12.925,00")):
                wages.fill(value)
                calculate.focus()
                with page.expect_navigation() as nav:
                    page.keyboard.press("Enter")
                assert nav.value.status == 200 and "no-store" in nav.value.headers["cache-control"]
                expect(page.locator("#result-heading")).to_be_focused()
                expect(page.locator(".summary strong")).to_have_text("R$ " + das)
                expect(page.get_by_role("heading", name="Serviços · Anexo " + annex.upper() + " · faixa 4")).to_be_visible()
                expect(wages).to_have_value(value)
                page.get_by_text("Histórico, memória de cálculo e fontes", exact=True).click()
                assert page.locator("html").evaluate("(el) => el.clientWidth === el.scrollWidth")
                if width == 1366:
                    (output / f"c09-{annex}.json").write_text(page.locator("pre").inner_text() + "\n", encoding="utf-8")
            wages.fill("")
            calculate.click()
            expect(page.locator(".summary strong")).to_have_text("Em aberto")
            expect(page.get_by_role("heading", name="Meses a completar")).to_be_visible()
            expect(page.locator(".result")).to_contain_text("R$ 5.295,00")
            expect(page.locator("#id_service_2026-02")).to_have_value("40000")
            assert "?" not in page.url
            context.close()
        browser.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("origin")
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    run(args.origin, args.output)
