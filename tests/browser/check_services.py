"""Exercise the service form in local Chrome and save the two synthetic C08 memories."""
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
            page.get_by_role("link", name="Calcular o Fator R e o DAS de serviços").click()
            page.get_by_role("button", name="Preencher com o exemplo de 28%").click()
            submit = page.get_by_role("button", name="Calcular Fator R e DAS")
            wages = page.locator("#id_wages_2027-01")
            for value, annex, das in (("20000", "III", "13.030,00"), ("19999,99", "V", "19.075,00")):
                wages.fill(value)
                submit.focus()
                with page.expect_navigation() as nav:
                    page.keyboard.press("Enter")
                assert nav.value.status == 200 and "no-store" in nav.value.headers["cache-control"]
                expect(page.locator("#result-heading")).to_be_focused()
                expect(page.locator(".summary strong")).to_have_text("R$ " + das)
                expect(page.locator(".result")).to_contain_text("Anexo " + annex)
                expect(wages).to_have_value(value)
                page.locator(".result summary").click()
                assert page.locator("html").evaluate("(el) => el.clientWidth === el.scrollWidth")
                if width == 1366:
                    (output / f"c08-{annex.lower()}.json").write_text(
                        page.locator(".result pre").inner_text() + "\n", encoding="utf-8")
            wages.fill("")
            submit.click()
            expect(page.locator(".result")).to_contain_text("Meses a completar")
            expect(page.locator("#id_cpp_2026-02")).to_have_value("2000")
            assert "?" not in page.url
            context.close()
        browser.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("origin")
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    run(args.origin, args.output)
