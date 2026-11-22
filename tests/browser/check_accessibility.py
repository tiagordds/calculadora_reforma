"""Inspect the keyboard path, accessible names, error links and reflow in local Chrome."""
import argparse
import json
import re

from playwright.sync_api import expect, sync_playwright


def audit(page):
    expect(page.get_by_role("heading", level=1)).to_have_count(1)
    for field in page.locator("input:visible, select:visible").all():
        expect(field).to_have_accessible_name(re.compile(r"\S"))
    assert page.locator("html").evaluate("e => e.scrollWidth === e.clientWidth")
    assert page.locator("[id]").evaluate_all("els => new Set(els.map(e => e.id)).size === els.length")
    for field in page.locator("[aria-invalid=true]").all():
        for error_id in field.get_attribute("aria-describedby").split():
            expect(page.locator("#" + error_id)).to_have_count(1)


def run(port):
    origin = f"http://127.0.0.1:{port}"
    with sync_playwright() as driver:
        browser = driver.chromium.launch(channel="chrome")
        for width in (1366, 320):
            ctx = browser.new_context(viewport={"width": width, "height": 800}, java_script_enabled=False)
            page = ctx.new_page()
            for path in ("/", "/operacao/caneta/", "/simples/tradicional/", "/simples/comparar/"):
                page.goto(origin + path)
                page.keyboard.press("Tab")
                assert page.locator(":focus").evaluate("e => getComputedStyle(e).outlineStyle !== 'none'")
                audit(page)
                if width == 1366:
                    page.locator("html").evaluate("e => e.style.zoom = '200%'")
                    audit(page)
            page.locator("summary", has_text="Experimentar o caso").focus()
            page.keyboard.press("Enter")
            page.get_by_role("button", name="Intermediário").press("Enter")
            expect(page.locator("#result-heading")).to_be_focused()
            # Walk the full tab order, including controls in every expanded group.
            closed = page.locator("details:not([open]) > summary:visible")
            while closed.count():
                closed.first.press("Enter")
            audit(page)
            expected = page.locator("a[href]:visible, button:visible, input:visible, select:visible, summary:visible")
            expected.first.focus()
            for field in expected.all()[1:]:
                for _ in range(6):  # Chrome exposes subfields of native month/date widgets.
                    page.keyboard.press("Tab")
                    if field.evaluate("e => e === document.activeElement"):
                        break
                expect(field).to_be_focused()
            page.locator("#id_cbs_rate").fill("101")
            page.get_by_role("button", name="Comparar as modalidades").press("Enter")
            expect(page.locator("#result-heading")).to_be_focused()
            audit(page)
            page.locator('a[href="#id_cbs_rate"]').press("Enter")
            expect(page.locator("#id_cbs_rate")).to_be_focused()
            print(json.dumps(dict(width=width, chrome=browser.version, keyboard=True,
                                  names=True, error_link=True, javascript=False)))
            ctx.close()
        browser.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, choices=(8055, 8003), required=True)
    run(parser.parse_args().port)
