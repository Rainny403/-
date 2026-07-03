import os
import time
from playwright.sync_api import sync_playwright

WEBHOOK = os.environ.get("DISCORD_WEBHOOK")

if not WEBHOOK:
    raise Exception("DISCORD_WEBHOOK 沒有設定")

URL = "https://info.monsterhunter.com/wilds/event-quest/zh-hant/schedule"

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=[
            "--no-sandbox",
            "--disable-blink-features=AutomationControlled"
        ]
    )

    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36",
        locale="zh-TW"
    )

    page = context.new_page()

    page.goto(URL, wait_until="networkidle", timeout=60000)

    time.sleep(3)

    html = page.content()

    browser.close()

import requests

requests.post(WEBHOOK, json={
    "content": "成功抓到網頁（CloudFront bypass 測試）\n\n" + html[:1500]
})
