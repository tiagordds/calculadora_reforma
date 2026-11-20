"""Local Chrome journey with JavaScript disabled. Only synthetic inputs are written."""
import argparse
import json
from pathlib import Path

from playwright.sync_api import expect, sync_playwright


def submit(page, name, status):
    button = page.get_by_role("button", name=name)
    button.focus()
    with page.expect_navigation() as navigation:
        page.keyboard.press("Enter")
    response = navigation.value
    assert response.status == status and "no-store" in response.headers["cache-control"]
    assert response.headers["x-robots-tag"] == "noindex, nofollow"
    assert page.locator("html").evaluate("(el) => el.scrollWidth === el.clientWidth")


def run(origin, output):
    output.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as driver:
        browser = driver.chromium.launch(channel="chrome", headless=True)
        for width, height in ((1366, 900), (320, 720)):
            context = browser.new_context(viewport={"width": width, "height": height},
                                          java_script_enabled=False)
            page = context.new_page()
            requests = []
            page.on("request", lambda request: requests.append((request.method, request.url)))
            page.goto(origin + "/")
            for _ in range(3):
                page.keyboard.press("Tab")
            expect(page.get_by_role("link", name="Estimar o Simples Nacional tradicional")).to_be_focused()
            page.keyboard.press("Enter")
            expect(page).to_have_url(origin + "/simples/tradicional/")
            page.locator("#id_opening").fill("2023-01")
            for _ in range(4):
                page.keyboard.press("Tab")
                if page.locator("#id_activity").evaluate("(el) => el === document.activeElement"):
                    break
            expect(page.locator("#id_activity")).to_be_focused()
            page.keyboard.press("ArrowDown")
            page.keyboard.press("Tab")
            page.keyboard.press("ArrowDown")
            page.keyboard.press("Tab")
            page.keyboard.press("ArrowDown")
            page.locator("#id_income").focus()
            page.keyboard.type("100.000,00")
            page.keyboard.press("Tab")
            page.keyboard.press("Space")
            page.keyboard.press("Tab")
            page.keyboard.type("100000")
            page.screenshot(path=output / f"formulario-{width}.png", full_page=True)
            submit(page, "Estimar com a média", 200)
            expect(page.locator("#result-heading")).to_be_focused()
            expect(page.locator(".summary strong")).to_have_text("R$ 8.825,00")
            expect(page.locator(".result")).to_contain_text("R$ 8.825,01")
            expect(page.locator(".result")).to_contain_text("R$ 105.900,00")
            page.locator(".result").screenshot(path=output / f"c01-{width}.png")
            page.keyboard.press("Tab")
            expect(page.locator(".result > details > summary")).to_be_focused()
            page.keyboard.press("Enter")
            page.locator(".result details details summary").focus()
            page.keyboard.press("Enter")
            replay = json.loads(page.locator("pre").inner_text())
            assert replay["engines"] == [] and replay["history"]["origin"] == "estimado"
            if width == 1366:
                (output / "c01.json").write_text(json.dumps(replay,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
            page.get_by_role("link", name="Refinar com meu histórico real").click()
            real = page.locator("#historico")
            if real.get_attribute("open") is None:
                real.locator("summary").focus()
                page.keyboard.press("Enter")
            for i, field in enumerate(real.locator("input").all()):
                field.fill("80000" if i == 0 else "100000")
            submit(page, "Calcular com histórico real", 200)
            expect(page.locator(".summary strong")).to_have_text("R$ 8.793,22")
            expect(page.locator(".result")).to_contain_text("R$ 1.180.000,00")
            expect(page.locator("#id_revenue")).to_have_value("100000")
            page.locator(".result").screenshot(path=output / f"historico-real-{width}.png")
            page.locator("#id_revenue").fill("1,234")
            submit(page, "Calcular com histórico real", 400)
            expect(page.get_by_role("heading", name="Revise os dados do formulário")).to_be_focused()
            expect(page.locator(".summary")).to_have_count(0)
            page.locator("#id_revenue").fill("100000")
            page.locator("#id_activity").select_option("service")
            submit(page, "Calcular com histórico real", 200)
            expect(page.locator("#result-heading")).to_have_text("Apuração não calculada")
            expect(page.locator(".result")).to_contain_text("Fator R")
            expect(page.locator(".summary")).to_have_count(0)
            assert all(url.startswith(origin+"/") and "?" not in url for _,url in requests)
            assert sum(method=="POST" for method,_ in requests)==4
            print(json.dumps(dict(browser=browser.version,width=width,height=height,javascript=False,
                                  estimated="8825.00",actual="8793.22",invalid=400,service="fora da cobertura",
                                  posts=4,horizontal_overflow=False),ensure_ascii=False))
            context.close()
        browser.close()


if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--origin",default="http://127.0.0.1:8004")
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    run(args.origin,args.output)
