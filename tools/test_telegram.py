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

print("--- TESTING TELEGRAM BOT API CONNECTION ---")

url_get_me = f"https://api.telegram.org/bot{TOKEN}/getMe"
try:
    req = urllib.request.Request(url_get_me, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp:
        print("getMe Success:", resp.read().decode('utf-8', errors='ignore'))
except urllib.error.HTTPError as e:
    err_body = e.read().decode('utf-8', errors='ignore')
    print(f"getMe HTTP Error {e.code}: {err_body[:500]}")
except Exception as e:
    print(f"getMe Connection Error: {e}")
