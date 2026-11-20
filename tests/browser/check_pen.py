"""Exercise the complete local form with real Chrome, with page JavaScript disabled."""
import argparse
import json
from pathlib import Path

from playwright.sync_api import expect, sync_playwright


def run(origin, online, directory):
    directory.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as driver:
        browser = driver.chromium.launch(channel="chrome", headless=True)
        for width, height in ((1366, 900), (320, 720)):
            context = browser.new_context(viewport={"width": width, "height": height},
                                          java_script_enabled=False)
            page = context.new_page()
            replies = []
            page.on("response", lambda r: replies.append((r.request.method, r.url, r.status)))
            page.goto(origin + "/")
            page.keyboard.press("Tab")
            expect(page.get_by_role("link", name="Conhecer a calculadora")).to_be_focused()
            page.keyboard.press("Enter")
            page.keyboard.press("Tab")
            expect(page.get_by_role("link", name="Calcular a revenda")).to_be_focused()
            page.keyboard.press("Enter")
            expect(page).to_have_url(origin + "/operacao/caneta/")
            check = page.get_by_role("checkbox")
            expect(check).not_to_be_checked()
            for _ in range(3):
                page.keyboard.press("Tab")
            expect(check).to_be_focused()
            page.keyboard.press("Space")
            page.keyboard.press("Tab")
            expect(page.get_by_role("button", name="Calcular a operação")).to_be_focused()
            with page.expect_navigation() as navigation:
                page.keyboard.press("Enter")
            reply = navigation.value
            assert reply.status == (200 if online else 503), reply.status
            assert "private" in reply.headers["cache-control"] and "no-store" in reply.headers["cache-control"]
            assert "noindex" in reply.headers["x-robots-tag"]
            expect(page.locator("#result-heading")).to_be_focused()
            if online:
                expect(page.locator(".summary strong")).to_have_text("R$ 10,10")
                assert page.locator(".amounts dd").all_text_contents() == [
                    "R$ 10,00", "R$ 0,05", "R$ 0,05", "R$ 0,10"]
            else:
                expect(page.get_by_text("Motor indisponível.", exact=False)).to_be_visible()
                expect(page.locator(".summary, .amounts")).to_have_count(0)
            assert page.locator("html").evaluate("(el) => el.scrollWidth === el.clientWidth")
            assert all(url.startswith(origin + "/") for _, url, _ in replies)
            assert sum(method == "POST" for method, _, _ in replies) == 1
            state = "sucesso" if online else "indisponivel"
            page.screenshot(path=directory / f"{state}-{width}.png", full_page=True)
            page.keyboard.press("Tab")
            summary = page.get_by_text("Memória de cálculo e estados", exact=True)
            expect(summary).to_be_focused()
            page.keyboard.press("Enter")
            expect(page.get_by_text("Elegibilidade não confirmada", exact=True)).to_be_visible()
            if online:
                expect(page.get_by_text("CALCULO_SIMULADO", exact=False).first).to_be_visible()
                page.keyboard.press("Tab")
                page.keyboard.press("Enter")
                expect(page.locator("pre")).to_contain_text("memoriaCalculo")
            assert page.locator("html").evaluate("(el) => el.scrollWidth === el.clientWidth")
            print(json.dumps({"browser": browser.version, "viewport": [width, height], "state": state,
                              "requests": replies, "keyboard": True, "javascript": False}))
            context.close()
        browser.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--origin", default="http://127.0.0.1:8002")
    parser.add_argument("--state", choices=["online", "offline"], required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(args.origin, args.state == "online", args.output)
