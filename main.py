import requests
import time
import os

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


STEP = 0.5
last_trigger_price = None

UP_EMOJI = "🟢"
DOWN_EMOJI = "🔴"


def get_price():
    url = "https://www.okx.com/api/v5/market/ticker?instId=BCH-USDT"
    r = requests.get(url)

    try:
        data = r.json()
    except:
        print("API returned non-JSON:", r.text[:200])
        return None

    if "data" not in data or len(data["data"]) == 0:
        print("API returned unexpected data:", data)
        return None

    price = data["data"][0]["last"]
    return round(float(price), 2)







def send_message(emoji, price, direction):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    text = f"{emoji} Bitcoin Cash {direction} to {price}$ @bitcoin_cash_price"

    r = requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": text
    })

    print("Telegram response:", r.text)


while True:
    try:
        price = get_price()

        if price is None:
            time.sleep(30)
            continue

        # первая цена — просто запоминаем
        if last_trigger_price is None:
            last_trigger_price = price

        # если цена изменилась больше чем на STEP — отправляем ОДНО сообщение
        if price >= last_trigger_price + STEP:
            send_message(UP_EMOJI, price, "increased")
            last_trigger_price = price

        elif price <= last_trigger_price - STEP:
            send_message(DOWN_EMOJI, price, "decreased")
            last_trigger_price = price

        time.sleep(20)

    except Exception as e:
        print("Error:", e)
        time.sleep(30)
