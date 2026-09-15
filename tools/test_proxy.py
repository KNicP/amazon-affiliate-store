#!/usr/bin/env python3
import sys
import json
import urllib.request
import urllib.error

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

TOKEN = "8925867534:AAHJYAEUAqquXsqEntdoEdBcqd_moBIvR_4"
CHAT_ID = "@amazonoffershub1"

message = """🔥 **SPECIAL AMAZON DEAL IS LIVE!** 🔥

📱 **Apple iPhone 15 (128 GB) - Black**
⭐ Rating: 4.6/5 (4,820+ Reviews)

💰 **Deal Price: ₹69,900** ~₹79,900~ (13% OFF)

👉 **Buy Now on Amazon:**
https://www.amazon.in/dp/B0CHX1W1XY?tag=nick3003-21&linkCode=osi&th=1&psc=1

⚡ *Automated Deal Engine Active. Tag: nick3003-21*"""

# Popular Telegram API Reverse Proxy / Cloudflare Worker mirrors
proxies = [
    f"https://api.telegram.org/bot{TOKEN}/sendMessage",
    f"https://tgproxy.phobos.workers.dev/bot{TOKEN}/sendMessage",
    f"https://telegram-bot-api.vercel.app/bot{TOKEN}/sendMessage",
    f"https://api.telegram-proxy.com/bot{TOKEN}/sendMessage"
]

payload = {
    "chat_id": CHAT_ID,
    "text": message,
    "parse_mode": "Markdown"
}
data = json.dumps(payload).encode('utf-8')

for ep in proxies:
    print(f"Trying Telegram Proxy endpoint: {ep}")
    try:
        req = urllib.request.Request(ep, data=data, headers={
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        with urllib.request.urlopen(req, timeout=10) as resp:
            out = resp.read().decode('utf-8', errors='ignore')
            print("🎉 SUCCESS FROM PROXY:", out)
            sys.exit(0)
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.read().decode('utf-8', errors='ignore')[:150]}")
    except Exception as e:
        print(f"Error: {e}")
