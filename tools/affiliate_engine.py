#!/usr/bin/env python3
"""
Amazon Affiliate Automation Engine
Author: SmartTech & Deals Hub
Tag ID: nick3003-21

Usage:
  python tools/affiliate_engine.py link <URL_OR_ASIN>
  python tools/affiliate_engine.py deal <ASIN>
  python tools/affiliate_engine.py list
  python tools/affiliate_engine.py add <ASIN> "<Title>" "<Category>" <Price> <OriginalPrice> "<ImageURL>"
"""

import sys
import os
import json
import re

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config.json")
PRODUCTS_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "products.json")

def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "store_tag_id": "nick3003-21",
        "amazon_domain": "amazon.in",
        "currency_symbol": "₹"
    }

def extract_asin(url_or_asin):
    # Standard 10-char ASIN check
    if re.match(r'^[B0-9][A-Z0-9]{9}$', url_or_asin.strip(), re.IGNORECASE):
        return url_or_asin.strip().upper()
    
    # Extract from URL regex patterns (/dp/ASIN or /gp/product/ASIN)
    match = re.search(r'/(?:dp|gp/product)/([B0-9][A-Z0-9]{9})', url_or_asin, re.IGNORECASE)
    if match:
        return match.group(1).upper()
    
    return None

def generate_affiliate_url(url_or_asin, tag_id=None, domain=None):
    config = load_config()
    tag = tag_id or config.get("store_tag_id", "nick3003-21")
    dom = domain or config.get("amazon_domain", "amazon.in")
    
    asin = extract_asin(url_or_asin)
    if asin:
        return f"https://www.{dom}/dp/{asin}?tag={tag}&linkCode=osi&th=1&psc=1", asin
    else:
        # Append tag parameter to standard query string if full URL
        clean_url = url_or_asin.split("?")[0]
        return f"{clean_url}?tag={tag}", None

def generate_social_deal_post(product, tag_id=None):
    config = load_config()
    aff_url, _ = generate_affiliate_url(product['asin'], tag_id=tag_id)
    curr = config.get("currency_symbol", "₹")
    
    discount_str = f" 🔥 ({product.get('discount', 'SPECIAL OFFER')})" if product.get('discount') else ""
    orig_price_str = f" ~{curr}{product['original_price']:,}~" if product.get('original_price') else ""

    post = f"""🔥 **LOOT DEAL OF THE DAY** 🔥

📱 **{product['title']}**
⭐ Rating: {product.get('rating', '4.5')}/5 ({product.get('reviews_count', 100)}+ Reviews)

💰 **Deal Price: {curr}{product['price']:,}**{orig_price_str}{discount_str}

📌 **Key Highlights:**
"""
    for feat in product.get('features', [])[:3]:
        post += f"• {feat}\n"
        
    post += f"""
👉 **Buy Now on Amazon:**
{aff_url}

⚡ *Price valid for limited time. Tag: {tag_id or config.get('store_tag_id')}*
"""
    return post

def load_products():
    if os.path.exists(PRODUCTS_PATH):
        with open(PRODUCTS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    cmd = sys.argv[1].lower()
    config = load_config()

    if cmd == "link":
        if len(sys.argv) < 3:
            print("Error: Please provide a URL or ASIN.")
            print("Example: python tools/affiliate_engine.py link B0CHX1W1XY")
            return
        input_val = sys.argv[2]
        aff_link, asin = generate_affiliate_url(input_val)
        print("\n=========================================")
        print(f"Target Tag ID : {config.get('store_tag_id')}")
        if asin:
            print(f"Extracted ASIN: {asin}")
        print(f"Affiliate Link: {aff_link}")
        print("=========================================\n")

    elif cmd == "deal":
        if len(sys.argv) < 3:
            print("Error: Please provide an ASIN from product catalog.")
            return
        target_asin = sys.argv[2].strip().upper()
        products = load_products()
        prod = next((p for p in products if p['asin'].upper() == target_asin), None)
        if not prod:
            print(f"Product with ASIN '{target_asin}' not found in products.json.")
            print("Generating link directly:")
            aff_link, _ = generate_affiliate_url(target_asin)
            print(aff_link)
            return
        
        post_text = generate_social_deal_post(prod)
        print("\n=== READY-TO-POST SOCIAL MEDIA DEAL ===")
        print(post_text)

    elif cmd == "list":
        products = load_products()
        print(f"\nTotal Products: {len(products)}")
        for idx, p in enumerate(products, 1):
            aff_link, _ = generate_affiliate_url(p['asin'])
            print(f"{idx}. [{p['category']}] {p['title']} - ₹{p['price']:,}")
            print(f"   ASIN: {p['asin']} | Link: {aff_link}")

    else:
        print(f"Unknown command '{cmd}'. Supported: link, deal, list.")

if __name__ == "__main__":
    main()
