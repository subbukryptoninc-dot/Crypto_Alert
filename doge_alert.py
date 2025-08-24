
import requests
import time

BOT_TOKEN = "8255763863:AAG2aWA-44fYUucnsaXXYJDymN4ffgfxerY"
CHAT_ID = "5722899921"
THRESHOLD_LOW = 0.228
THRESHOLD_HIGH = 0.25
CHECK_INTERVAL = 180

def get_doge_price():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": "dogecoin", "vs_currencies": "usd"}
    response = requests.get(url, params=params).json()
    return response["dogecoin"]["usd"]

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, data=payload)

last_alert = None
print("🐶 Doge Price Alert Bot is running...")

while True:
    try:
        price = get_doge_price()
        print("Current DOGE price:", price)
        if price <= THRESHOLD_LOW:
            if last_alert != "low":
                send_message(f"🚨 DOGE dropped below ${THRESHOLD_LOW}! Current: ${price}")
                last_alert = "low"
        elif price >= THRESHOLD_HIGH:
            if last_alert != "high":
                send_message(f"🚀 DOGE rose above ${THRESHOLD_HIGH}! Current: ${price}")
                last_alert = "high"
        else:
            last_alert = None
    except Exception as e:
        print("Error:", e)
    time.sleep(CHECK_INTERVAL)
