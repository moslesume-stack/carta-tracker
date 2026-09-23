from flask import Flask, request
import requests
import os
from datetime import datetime
from zoneinfo import ZoneInfo

app = Flask(__name__)

WEBHOOK = os.environ["DISCORD_WEBHOOK"]


def get_device():
    ua = request.user_agent.string.lower()

    if "iphone" in ua:
        return "IPHONE", "iPhone"

    if "ipad" in ua:
        return "IPAD", "iPad"

    if "android" in ua:
        device = "ANDROID"

        if "samsung" in ua:
            brand = "Samsung"
        elif "xiaomi" in ua:
            brand = "Xiaomi"
        elif "huawei" in ua:
            brand = "Huawei"
        elif "oppo" in ua:
            brand = "OPPO"
        elif "oneplus" in ua:
            brand = "OnePlus"
        elif "google" in ua or "pixel" in ua:
            brand = "Google Pixel"
        elif "motorola" in ua:
            brand = "Motorola"
        elif "realme" in ua:
            brand = "Realme"
        elif "vivo" in ua:
            brand = "vivo"
        else:
            brand = "Android"

        return device, brand

    if "windows" in ua:
        return "WINDOWS PC", "Desktop"

    if "macintosh" in ua:
        return "MAC", "Mac"

    if "linux" in ua:
        return "LINUX PC", "Desktop"

    return "UNKNOWN", "Unknown"


@app.route("/opened")
def opened():
    device, model = get_device()

    time = datetime.now(
        ZoneInfo("America/Bogota")
    ).strftime("%H:%M:%S")

    message = (
        "```text\n"
        "╔══════════════════════════╗\n"
        "       ⚡ LETTER ACCESS\n"
        "╚══════════════════════════╝\n\n"
        f"[+] STATUS  : OPENED\n"
        f"[+] DEVICE  : {device}\n"
        f"[+] MODEL   : {model}\n"
        f"[+] TIME    : {time}\n"
        "```"
    )

    try:
        requests.post(
            WEBHOOK,
            json={"content": message},
            timeout=5
        )
    except requests.RequestException:
        pass

    return "OK"


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )