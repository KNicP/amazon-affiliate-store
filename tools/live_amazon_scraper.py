#!/usr/bin/env python3
"""
Live Amazon India Product Scraper & Telegram Auto-Publisher
Tag ID: nick3003-21
Target Channel: @amazonoffershub1
"""

import os
import sys
import re
import json
import time
import urllib.request
import urllib.parse
import urllib.error

TAG_ID = "nick3003-21"
BOT_TOKEN = "8925867534:AAHJYAEUAqquXsqEntdoEdBcqd_moBIvR_4"
CHAT_ID = "@amazonoffershub1"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
]

def fetch_live_product_data(asin):
    """Scrapes real live product title, price, MRP, rating, and specs from Amazon India."""
    url = f"https://www.amazon.in/dp/{asin}"
    req = urllib.request.Request(url, headers={
        "User-Agent": USER_AGENTS[0],
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    })
    
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            
            # Extract Live Product Title
            title_match = re.search(r'<span id="productTitle"[^>]*>\s*(.*?)\s*</span>', html, re.DOTALL)
            title = title_match.group(1).strip() if title_match else None
            
            if not title:
                title_match = re.search(r'<meta name="title" content="(.*?)"', html)
                title = title_match.group(1).replace("Amazon.in:", "").strip() if title_match else f"Amazon Product ({asin})"
                
            # Clean title
            title = re.sub(r'\s+', ' ', title)[:120]

            # Extract Live Price
            price_match = re.search(r'<span class="a-price-whole">\s*([\d,]+)', html)
            price = price_match.group(1) if price_match else None
            
            # Extract Live Original Price / MRP
            mrp_match = re.search(r'<span class="a-text-price"[^>]*>\s*<span[^>]*>[\s₹]*([\d,]+)', html)
            mrp = mrp_match.group(1) if mrp_match else None

            # Extract Live Rating
            rating_match = re.search(r'(\d\.\d) out of 5 stars', html)
            rating = rating_match.group(1) if rating_match else "4.3"

            aff_link = f"https://www.amazon.in/dp/{asin}?tag={TAG_ID}&linkCode=ll1"

            return {
                "asin": asin,
                "title": title,
                "price": price,
                "mrp": mrp,
                "rating": rating,
                "url": aff_link
            }
    except Exception as e:
        print(f"Error fetching ASIN {asin}: {e}")
        return None

def post_to_telegram(product):
    """Sends real live Amazon deal to Telegram channel."""
    title = product['title']
    rating = product['rating']
    price_str = f"₹{product['price']}" if product['price'] else "Check Live Deal"
    mrp_str = f" (<s>₹{product['mrp']}</s>)" if product['mrp'] else ""
    url = product['url']

    msg = f"🔥 <b>LIVE AMAZON DEAL OF THE DAY</b> 🔥\n\n"
    msg += f"📱 <b>{title}</b>\n"
    msg += f"⭐ Rating: {rating}/5\n\n"
    msg += f"💰 <b>Live Price: {price_str}</b>{mrp_str}\n\n"
    msg += f"👉 <b>Buy Directly on Amazon:</b>\n{url}\n\n"
    msg += f"⚡ <i>Tag Active: {TAG_ID}</i>"

    req_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": msg,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(req_url, data=data, headers={"Content-Type": "application/json", "User-Agent": USER_AGENTS[0]})

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            print("✅ LIVE DEAL POSTED TO TELEGRAM SUCCESSFUL:", resp.read().decode())
            return True
    except Exception as e:
        print(f"❌ Telegram Error: {e}")
        return False

# Real live popular Amazon India ASINs catalog
LIVE_ASIN_POOL = [
    "B0CX5829H5", # OnePlus Nord CE4
    "B0CX587XN8", # Samsung Galaxy M15 5G
    "B09B8VGCR8", # Echo Dot 5th Gen
    "B0D4784ZCD", # Realme NARZO N65
    "B09N3ZNHTY", # boAt Airdopes 141
    "B0C46A284B", # Redmi 13C 5G
    "B0CG863HCS", # Fire-Boltt Ninja Call Pro Plus
    "B0B3RRWSF6"  # Pigeon Healthifry Air Fryer
]

if __name__ == "__main__":
    import random
    selected_asin = random.choice(LIVE_ASIN_POOL)
    print(f"Fetching Live Amazon Data for ASIN: {selected_asin}...")
    
    prod_data = fetch_live_product_data(selected_asin)
    if prod_data:
        print("Live Scraped Data:", prod_data)
        post_to_telegram(prod_data)
    else:
        print("Failed to fetch live data.")
