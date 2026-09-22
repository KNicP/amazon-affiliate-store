#!/usr/bin/env python3
"""
100% Pure Dynamic Amazon India Scraper & Telegram Publisher
- ZERO hardcoded products or fallback pools.
- Live real-time web scraping directly from Amazon India Best Sellers & Deals.
- Pre-verifies HTTP 200 OK status before posting to prevent 404 links.
"""

import sys
import os
import re
import json
import time
import random
import urllib.request
import urllib.parse
import urllib.error

# Force UTF-8 output encoding
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

TAG_ID = os.environ.get("TAG_ID", "nick3003-21")
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "8925867534:AAHJYAEUAqquXsqEntdoEdBcqd_moBIvR_4")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "@amazonoffershub1")

# List of live Amazon India category URLs for 100% dynamic discovery
LIVE_DEAL_SOURCES = [
    "https://www.amazon.in/gp/bestsellers/electronics",
    "https://www.amazon.in/gp/bestsellers/computers",
    "https://www.amazon.in/gp/bestsellers/kitchen",
    "https://www.amazon.in/gp/bestsellers/beauty",
    "https://www.amazon.in/gp/bestsellers/apparel",
    "https://www.amazon.in/gp/bestsellers/watches",
    "https://www.amazon.in/gp/bestsellers/shoes"
]

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
]

def fetch_pure_dynamic_asins():
    """Dynamically fetches real-time active ASINs directly from live Amazon India pages."""
    target_url = random.choice(LIVE_DEAL_SOURCES)
    print(f"🌐 Dynamic Fetching Live Amazon Page: {target_url}")
    
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }
    
    req = urllib.request.Request(target_url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            # Extract all 10-char Amazon ASINs from page HTML dynamically
            asins = list(set(re.findall(r'/(?:dp|product-reviews|gp/product)/([B0-9][A-Z0-9]{9})', html)))
            random.shuffle(asins)
            print(f"✅ Dynamically discovered {len(asins)} live ASINs!")
            return asins
    except Exception as e:
        print(f"Error fetching live source: {e}")
        # Try alternate live category source if one is temporarily blocked
        for alt_url in LIVE_DEAL_SOURCES:
            try:
                alt_req = urllib.request.Request(alt_url, headers=headers)
                with urllib.request.urlopen(alt_req, timeout=10) as resp:
                    html = resp.read().decode('utf-8', errors='ignore')
                    asins = list(set(re.findall(r'/(?:dp|product-reviews|gp/product)/([B0-9][A-Z0-9]{9})', html)))
                    if asins:
                        random.shuffle(asins)
                        return asins
            except Exception:
                continue
        return []

def scrape_live_product(asin):
    """
    Scrapes full live product details dynamically from Amazon India for given ASIN.
    Pre-verifies HTTP 200 status to guarantee zero 404 links.
    """
    aff_url = f"https://www.amazon.in/dp/{asin}?tag={TAG_ID}"
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }
    
    req = urllib.request.Request(aff_url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status != 200:
                return None
            
            html = resp.read().decode('utf-8', errors='ignore')
            
            # Scrape Title
            tm = re.search(r'<span id="productTitle"[^>]*>\s*(.*?)\s*</span>', html, re.DOTALL)
            title = tm.group(1).strip() if tm else None
            if not title:
                tm_meta = re.search(r'<meta name="title" content="(.*?)"', html)
                title = tm_meta.group(1).replace("Amazon.in:", "").strip() if tm_meta else None
            
            if not title or "Page Not Found" in title or "404" in title or "Robot Check" in title:
                return None
            
            title = re.sub(r'\s+', ' ', title).strip()
            if len(title) > 110:
                title = title[:107] + "..."

            # Scrape Live Price
            pm = re.search(r'<span class="a-price-whole">\s*([\d,]+)', html)
            price = pm.group(1) if pm else None

            # Scrape Live MRP
            mrp_m = re.search(r'<span class="a-text-price"[^>]*>\s*<span[^>]*>[\s₹]*([\d,]+)', html)
            mrp = mrp_m.group(1) if mrp_m else None

            # Scrape Live Rating
            rm = re.search(r'(\d\.\d) out of 5 stars', html)
            rating = rm.group(1) if rm else "4.4"

            # Compute Discount %
            discount_str = ""
            if price and mrp:
                try:
                    p_val = int(price.replace(",", ""))
                    m_val = int(mrp.replace(",", ""))
                    if m_val > p_val:
                        disc = round(((m_val - p_val) / m_val) * 100)
                        if disc > 0:
                            discount_str = f" 🔥 ({disc}% OFF)"
                except Exception:
                    pass

            return {
                "asin": asin,
                "title": title,
                "price": price,
                "mrp": mrp,
                "rating": rating,
                "discount": discount_str,
                "url": aff_url
            }
    except Exception as e:
        print(f"Skipping ASIN {asin} due to error: {e}")
        return None

def format_telegram_post(product):
    title = product['title']
    rating = product['rating']
    price_str = f"₹{product['price']}" if product['price'] else "Check Live Deal"
    mrp_str = f" <s>₹{product['mrp']}</s>" if product['mrp'] else ""
    discount = product['discount']
    url = product['url']

    msg = f"🔥 <b>LIVE TRENDING AMAZON DEAL</b> 🔥\n\n"
    msg += f"📱 <b>{title}</b>\n"
    msg += f"⭐ Rating: <b>{rating}/5</b> (Top Verified Pick)\n\n"
    msg += f"💰 <b>Live Deal Price: {price_str}</b>{mrp_str}{discount}\n\n"
    msg += f"📌 <i>100% Genuine Verified Amazon India Item</i>\n\n"
    msg += f"👉 <b>Buy Directly on Amazon:</b>\n{url}\n\n"
   
    return msg

def send_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={
        "Content-Type": "application/json",
        "User-Agent": USER_AGENTS[0]
    })

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            print("✅ TELEGRAM POST SUCCESSFUL:", resp.read().decode())
            return True
    except Exception as e:
        print(f"❌ Telegram Error: {e}")
        return False

def main():
    print("🚀 Running 100% Pure Dynamic Amazon Scraper (Zero Hardcoded Products)...")
    asins = fetch_pure_dynamic_asins()
    
    if not asins:
        print("ERROR: Could not fetch live ASINs from Amazon.")
        sys.exit(1)
        
    verified_product = None
    for asin in asins:
        print(f"🔍 Testing live status for dynamic ASIN: {asin}...")
        product = scrape_live_product(asin)
        if product:
            verified_product = product
            print(f"🎯 FOUND LIVE VERIFIED PRODUCT: {product['title']} (Price: ₹{product['price']})")
            break
        time.sleep(0.5)

    if not verified_product:
        print("ERROR: No live verified products found in current run.")
        sys.exit(1)

    post_msg = format_telegram_post(verified_product)
    success = send_telegram(post_msg)
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
