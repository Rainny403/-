import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

WEBHOOK = os.environ["DISCORD_WEBHOOK"]

# 你的 Cloudflare Worker 網址（請改成你自己的）
WORKER_URL = "https://mhwilds-discord.toptoonisgood5.workers.dev"

response = requests.get(WORKER_URL, timeout=30)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

print("成功取得 HTML")
