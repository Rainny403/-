import os
import requests
from bs4 import BeautifulSoup

# Discord Webhook
WEBHOOK = os.environ["DISCORD_WEBHOOK"]

# Cloudflare Worker
WORKER_URL = "https://mhwilds-discord.toptoonisgood5.workers.dev"

# 取得 HTML
response = requests.get(WORKER_URL, timeout=30)
response.raise_for_status()

# 解析 HTML
soup = BeautifulSoup(response.text, "lxml")

print("✅ HTML 取得成功")

# 找所有 tr
rows = soup.select("tr")

print(f"找到 {len(rows)} 個 tr")
