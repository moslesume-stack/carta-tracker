from flask import Flask
import requests
import os

app = Flask(__name__)

WEBHOOK = os.environ["DISCORD_WEBHOOK"]


@app.route("/opened")
def opened():
    try:
        requests.post(
            WEBHOOK,
            json={
                "content": "💌 Alguien ha abierto la carta."
            },
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