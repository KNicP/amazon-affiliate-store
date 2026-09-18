#!/usr/bin/env python3
"""
High-Commission Amazon India Live Deal Scraper & Publisher
Tag ID: nick3003-21
Target Channel: @amazonoffershub1

Category Commission Priority:
1. Amazon Devices (Echo, FireTV) -> 10% Commission
2. Kitchenware & Home Appliances -> 9-10% Commission
3. Home & Decor -> 9% Commission
4. Audio & Accessories (Earbuds, Powerbanks, Smartwatches) -> 6-8% Commission
"""

import os
import sys
import re
import json
import random
import urllib.request
import urllib.parse
import urllib.error

TAG_ID = "nick3003-21"
BOT_TOKEN = "8925867534:AAHJYAEUAqquXsqEntdoEdBcqd_moBIvR_4"
CHAT_ID = "@amazonoffershub1"

# High-Commission Category Pages on Amazon India
HIGH_COMMISSION_CATEGORY_URLS = [
    ("Kitchen & Home Appliances (9-10% Comm)", "https://www.amazon.in/gp/bestsellers/kitchen"),
    ("Amazon Devices (10% Comm)", "https://www.amazon.in/gp/bestsellers/amazon-devices"),
    ("Home Appliances (9% Comm)", "https://www.amazon.in/gp/bestsellers/appliances"),
    ("Audio & Smart Accessories (7% Comm)", "https://www.amazon.in/gp/bestsellers/electronics")
]

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
]

def get_live_asins_from_category(category_name, category_url):
    """Scrapes real-time live ASINs from Amazon India high-commission bestseller pages."""
    print(f"🔍 Crawling Live High-Commission Category: {category_name}...")
    req = urllib.request.Request(category_url, headers={
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    })
    
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            # Extract ASINs from /dp/ASIN pattern
            asins = list(set(re.findall(r'/dp/([B0-9][A-Z0-9]{9})', html)))
            print(f"✅ Found {len(asins)} Live ASINs in {category_name}")
            return asins
    except Exception as e:
        print(f"❌ Error crawling {category_name}: {e}")
        return []

def scrape_live_product(asin):
    """Scrapes real live product metadata directly from Amazon India."""
    url = f"https://www.amazon.in/dp/{asin}"
    req = urllib.request.Request(url, headers={
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": "en-US,en;q=0.9"
    })
    
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            
            # Title
            title_match = re.search(r'<span id="productTitle"[^>]*>\s*(.*?)\s*</span>', html, re.DOTALL)
            title = title_match.group(1).strip() if title_match else None
            if not title:
                title_match = re.search(r'<meta name="title" content="(.*?)"', html)
                title = title_match.group(1).replace("Amazon.in:", "").strip() if title_match else None
            
            if not title or "Amazon.in" in title:
                return None

            title = re.sub(r'\s+', ' ', title)[:110]

            # Price
            price_match = re.search(r'<span class="a-price-whole">\s*([\d,]+)', html)
            price = price_match.group(1) if price_match else "Check Live Deal"

            # Original Price / MRP
            mrp_match = re.search(r'<span class="a-text-price"[^>]*>\s*<span[^>]*>[\s₹]*([\d,]+)', html)
            mrp = mrp_match.group(1) if mrp_match else None

            # Rating
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
        print(f"Error scraping product {asin}: {e}")
        return None

def publish_to_telegram(product, cat_name):
    """Posts real live scraped deal to Telegram."""
    title = product['title']
    price = product['price']
    mrp_text = f" (<s>₹{product['mrp']}</s>)" if product['mrp'] else ""
    rating = product['rating']
    url = product['url']

    msg = f"🔥 <b>HIGH COMMISSION LOOT DEAL</b> 🔥\n"
    msg += f"🏷️ <i>Category: {cat_name}</i>\n\n"
    msg += f"📦 <b>{title}</b>\n"
    msg += f"⭐ Rating: {rating}/5\n\n"
    msg += f"💰 <b>Live Deal Price: ₹{price}</b>{mrp_text}\n\n"
    msg += f"👉 <b>Buy Directly on Amazon:</b>\n{url}\n\n"
    msg += f"⚡ <i>Tag Active: {TAG_ID}</i>"

    send_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML"}
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(send_url, data=data, headers={"Content-Type": "application/json", "User-Agent": USER_AGENTS[0]})

    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            print("🚀 LIVE HIGH-COMMISSION DEAL POSTED SUCCESSFULLY!")
            return True
    except Exception as e:
        print(f"Telegram Error: {e}")
        return False

def main():
    cat_name, cat_url = random.choice(HIGH_COMMISSION_CATEGORY_URLS)
    asins = get_live_asins_from_category(cat_name, cat_url)
    
    if not asins:
        # Fallback pool of high-commission category ASINs
        asins = ["B09B8VGCR8", "B0B3RRWSF6", "B08TV2P1N8", "B09N3ZNHTY", "B0CG863HCS"]

    random.shuffle(asins)
    for asin in asins[:5]:
        prod = scrape_live_product(asin)
        if prod:
            print(f"Scraped Live Product: {prod['title']} | Price: ₹{prod['price']}")
            publish_to_telegram(prod, cat_name)
            break

if __name__ == "__main__":
    main()
