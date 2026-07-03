import os
import requests
from playwright.sync_api import sync_playwright

WEBHOOK = os.environ.get("DISCORD_WEBHOOK")

URL = "https://info.monsterhunter.com/wilds/event-quest/zh-hant/schedule"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto(URL, wait_until="networkidle")

    # 等 JS 完全渲染
    page.wait_for_timeout(5000)

    # 直接抓「可見文字」
    text = page.inner_text("body")

    browser.close()

requests.post(WEBHOOK, json={
    "content": "🎯 DOM 抓取結果（前3000字）\n\n" + text[:3000]
})
