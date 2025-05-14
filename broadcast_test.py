import os
import requests
from dotenv import load_dotenv

load_dotenv()
ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

data = {
    "messages": [
        {
            "type": "text",
            "text": "📢 これはBroadcastによるテスト通知です。\nこのメッセージが届けば、全ユーザー通知は成功です！"
        }
    ]
}

response = requests.post("https://api.line.me/v2/bot/message/broadcast", headers=headers, json=data)

if response.status_code == 200:
    print("🎉 Broadcastメッセージ送信成功！")
else:
    print(f"❌ エラー発生: {response.status_code}")
    print(response.text)
