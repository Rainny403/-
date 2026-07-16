import os
import requests
from bs4 import BeautifulSoup

WEBHOOK = os.environ["DISCORD_WEBHOOK"]

WORKER_URL = "https://mhwilds-discord.toptoonisgood5.workers.dev"

response = requests.get(WORKER_URL, timeout=30)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

message = """📅 測試訊息

Cloudflare Worker 已成功取得 HTML！
"""

r = requests.post(
    WEBHOOK,
    json={"content": message}
)

print("HTML 取得成功")
print("Discord 狀態碼：", r.status_code)
print("Discord 回應：", r.text)
