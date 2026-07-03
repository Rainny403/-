import os
from playwright.sync_api import sync_playwright

WEBHOOK = os.environ.get("DISCORD_WEBHOOK")

if not WEBHOOK:
    raise Exception("DISCORD_WEBHOOK 沒有設定")

URL = "https://info.monsterhunter.com/wilds/event-quest/zh-hant/schedule"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(URL)

    content = page.content()
    browser.close()

# Discord 測試先送 raw（確認抓得到）
import requests

requests.post(WEBHOOK, json={
    "content": "成功抓到網頁（下一步才解析）\n\n" + content[:1500]
})
