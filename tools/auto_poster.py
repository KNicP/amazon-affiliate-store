#!/usr/bin/env python3
"""
Standalone Automated Amazon Affiliate Publisher
Tag ID: nick3003-21
Target Channel: @amazonoffershub1
"""

import sys
import json
import time
import random
import urllib.request
import urllib.error

# Force UTF-8 output encoding for Windows & Linux
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

TAG_ID = "nick3003-21"
BOT_TOKEN = "8925867534:AAHJYAEUAqquXsqEntdoEdBcqd_moBIvR_4"
CHAT_ID = "@amazonoffershub1"
DOMAIN = "amazon.in"

PRODUCTS = [
    {
        "asin": "B0CHX1W1XY",
        "title": "Apple iPhone 15 (128 GB) - Black",
        "price": 69900,
        "original_price": 79900,
        "discount": "13% OFF",
        "rating": 4.6,
        "reviews": 4820,
        "highlights": [
            "Dynamic Island bubbles up alerts & live activities",
            "48MP Main Camera for ultra-high resolution photos",
            "Superfast A16 Bionic chip & USB-C port"
        ]
    },
    {
        "asin": "B0CQRW81X5",
        "title": "Sony WH-1000XM5 Wireless Noise Canceling Headphones",
        "price": 26990,
        "original_price": 34990,
        "discount": "23% OFF",
        "rating": 4.7,
        "reviews": 3150,
        "highlights": [
            "Industry leading Active Noise Cancellation",
            "Up to 30-hour battery life with quick charging",
            "Ultra-lightweight design & crystal clear mic calls"
        ]
    },
    {
        "asin": "B0CWPC6KFT",
        "title": "Samsung Galaxy Watch6 Bluetooth (44mm, Graphite)",
        "price": 18499,
        "original_price": 33999,
        "discount": "46% OFF",
        "rating": 4.4,
        "reviews": 1890,
        "highlights": [
            "20% larger display with slimmer bezel",
            "Advanced sleep coaching & body composition analysis",
            "Durable Sapphire Crystal Glass with IP68 water resistance"
        ]
    },
    {
        "asin": "B0CDLRFDFV",
        "title": "Echo Dot (5th Gen) Smart Speaker with Alexa",
        "price": 4499,
        "original_price": 5499,
        "discount": "18% OFF",
        "rating": 4.5,
        "reviews": 8940,
        "highlights": [
            "Best sounding Echo Dot with vibrant audio & deep bass",
            "Control lights, plugs, and AC with simple voice commands",
            "Built-in motion & temperature sensors"
        ]
    },
    {
        "asin": "B0CL5KFRM8",
        "title": "Apple iPad Air (5th Gen) M1 Chip (64GB, Wi-Fi)",
        "price": 54900,
        "original_price": 59900,
        "discount": "8% OFF",
        "rating": 4.8,
        "reviews": 2300,
        "highlights": [
            "M1 desktop-class chip performance",
            "10.9-inch Liquid Retina display with True Tone",
            "12MP Ultra Wide front camera with Center Stage"
        ]
    }
]

def format_post(product):
    aff_link = f"https://www.{DOMAIN}/dp/{product['asin']}?tag={TAG_ID}&linkCode=osi&th=1&psc=1"
    orig_str = f" ~₹{product['original_price']:,}~" if product.get('original_price') else ""
    disc_str = f" 🔥 ({product['discount']})" if product.get('discount') else ""

    text = f"🔥 **LOOT DEAL OF THE DAY** 🔥\n\n"
    text += f"📱 **{product['title']}**\n"
    text += f"⭐ Rating: {product['rating']}/5 ({product['reviews']}+ Reviews)\n\n"
    text += f"💰 **Deal Price: ₹{product['price']:,}**{orig_str}{disc_str}\n\n"
    text += "📌 **Key Highlights:**\n"
    for h in product['highlights']:
        text += f"• {h}\n"
    text += f"\n👉 **Buy Now on Amazon:**\n{aff_link}\n\n"
    text += f"⚡ *Price valid for limited time. Tag: {TAG_ID}*"
    return text

def send_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            res_str = resp.read().decode('utf-8', errors='ignore')
            print("SUCCESS:", res_str)
            return True
    except urllib.error.HTTPError as e:
        err = e.read().decode('utf-8', errors='ignore')
        print(f"HTTP Error {e.code}: {err[:300]}")
        return False
    except Exception as e:
        print("ERROR:", e)
        return False

def main():
    prod = random.choice(PRODUCTS)
    print(f"Publishing deal for: {prod['title']}")
    msg = format_post(prod)
    success = send_telegram(msg)
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
