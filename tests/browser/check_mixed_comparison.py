"""Exercise the mixed comparison via native POST, and save the displayed synthetic memories."""
import argparse
import json
from pathlib import Path

from playwright.sync_api import expect, sync_playwright


def exercise(page, origin, output):
    page.goto(origin + "/")
    page.get_by_role("link", name="Estimar o DAS de atividades mistas").click()
    page.get_by_role("button", name="Preencher exemplo de comércio e serviços").click()
    page.locator("#id_service").fill("40001")
    page.get_by_role("button", name="Calcular o DAS consolidado").click()
    page.get_by_role("button", name="Comparar usando estes dados").click()
    expect(page.locator("#id_service")).to_have_value("40001")
    expect(page.locator("#id_retail_2026-02")).to_have_value("60000")
    expect(page.locator("#id_hybrid_retail_2026-02")).to_have_value("")
    page.get_by_role("button", name="Explorar exemplo com históricos diferentes").click()
    calculate = page.get_by_role("button", name="Comparar trajetórias")

    def fill(name, value):
        field = page.locator(f'[name="{name}"]')
        panel = field.locator("xpath=ancestor::details[1]")
        if panel.count() and panel.get_attribute("open") is None:
            panel.locator("summary").first.click()
        field.fill(value)

    def capture(name, complete):
        expect(page.locator("#result-heading")).to_be_focused()
        expect(page.locator("#result-heading")).to_have_text("Comparação condicional completa" if complete else "Comparação parcial")
        page.get_by_text("Memória de cálculo, premissas e fontes", exact=True).click()
        assert page.locator("html").evaluate("(el) => el.clientWidth === el.scrollWidth")
        value = page.locator("pre").inner_text()
        if output:
            (output / (name + ".json")).write_bytes((value + "\n").encode("utf-8"))
        memory = json.loads(value)
        assert "?" not in page.url and (memory["difference"] is not None) == complete
        return memory

    def submit():
        calculate.focus()
        with page.expect_navigation() as nav:
            page.keyboard.press("Enter")
        assert nav.value.status == 200 and "no-store" in nav.value.headers["cache-control"]

    assert capture("fronteira-v-iii", True)["traditional"]["factor"]["annex"] == "V"
    fill("wages_2027-01", "20000")
    submit()
    assert capture("ambos-iii", True)["traditional"]["factor"]["annex"] == "III"
    fill("wages_2027-01", "19999.99")
    fill("shared-cbs_credit", "")
    submit()
    assert capture("credito-cbs-pendente", False)["hybrid"]["accounts"]["ibs"]["net"] is not None
    fill("shared-cbs_credit", "0")
    fill("iss_amount", "")
    submit()
    assert capture("iss-pendente", False)["hybrid"]["groups"][0]["das"]["displayed"] == "4090.37"
    fill("iss_amount", "1463")
    fill("retail", "")
    submit()
    assert capture("preco-comercial-pendente", False)["traditional"]["groups"][1]["amounts"]["monthly"] == "7630.00"
    fill("retail", "60001")
    submit()
    expect(page.locator("#result-heading")).to_have_text("Comparação condicional completa")
    expect(page.locator("#id_hybrid_retail_2027-01")).to_have_value("50000")


def run(origin, output):
    output.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as driver:
        browser = driver.chromium.launch(channel="chrome", headless=True)
        for width in (320, 1366):
            context = browser.new_context(viewport={"width": width, "height": 900}, java_script_enabled=False)
            exercise(context.new_page(), origin, output if width == 1366 else None)
            context.close()
        browser.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("origin")
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    run(args.origin, args.output)
