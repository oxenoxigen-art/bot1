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
    url = "https://api.binance.com/api/v3/ticker/price?symbol=BCHUSDT"
    data = requests.get(url).json()

    if "price" not in data:
        print("API returned unexpected data:", data)
        return None

    return round(float(data["price"]), 2)



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
            time.sleep(10)
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
