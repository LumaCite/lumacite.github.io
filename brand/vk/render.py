# Рендер обложки (1920x768) и аватара (1500x1500) группы ВК из HTML.
# Запуск: python3 render.py  (нужен Playwright с Chromium)
# Новая игра: положить иконку рядом и добавить блок .g в cover.html.
import os
from playwright.sync_api import sync_playwright
from PIL import Image
here = os.path.dirname(os.path.abspath(__file__))
jobs = [("cover.html", 1920, 768, "cover_1920x768"), ("avatar.html", 1500, 1500, "avatar_1500")]
with sync_playwright() as p:
    b = p.chromium.launch()
    for html, w, h, out in jobs:
        pg = b.new_page(viewport={"width": w, "height": h})
        pg.goto("file://" + os.path.join(here, html))
        pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(500)
        png = os.path.join(here, out + ".png"); pg.screenshot(path=png)
        if out.startswith("cover"):
            Image.open(png).convert("RGB").save(os.path.join(here, out + ".jpg"), quality=92); os.remove(png)
    b.close()
