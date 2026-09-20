import os
import requests
from playwright.sync_api import sync_playwright

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
URL = "https://cryptobubbles.net/"
FOTO = "mapa.png"

def sacar_foto():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1600, "height": 1000})
        page.goto(URL, wait_until="domcontentloaded", timeout=90000)
        page.wait_for_timeout(8000)

        boton_1d = page.get_by_text("1D", exact=True)
        if boton_1d.count() > 0:
            boton_1d.first.click()

        page.keyboard.press("Escape")
        page.wait_for_timeout(2000)
        page.screenshot(path=FOTO, full_page=False)
        browser.close()

def enviar():
    with open(FOTO, "rb") as f:
        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendPhoto",
            data={
                "chat_id": CHAT_ID,
                "caption": "Actualización del mercado cripto en compresión de 1D.",
            },
            files={"photo": f},
            timeout=60,
        ).raise_for_status()

if __name__ == "__main__":
    sacar_foto()
    enviar()
    
