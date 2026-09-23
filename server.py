from flask import Flask, request
import requests
import os
from datetime import datetime
from zoneinfo import ZoneInfo

app = Flask(__name__)

WEBHOOK = os.environ["DISCORD_WEBHOOK"]


@app.route("/opened")
def opened():
    ip = request.remote_addr or "Desconocida"
    user_agent = request.user_agent.string or "Desconocido"

    # Obtener ubicación aproximada mediante la IP
    location = {}

    try:
        response = requests.get(
            f"https://ipapi.co/{ip}/json/",
            timeout=5
        )

        if response.ok:
            location = response.json()

    except requests.RequestException:
        pass

    city = location.get("city", "Desconocida")
    region = location.get("region", "Desconocida")
    country = location.get("country_name", "Desconocido")
    postal = location.get("postal", "Desconocido")
    latitude = location.get("latitude")
    longitude = location.get("longitude")
    org = location.get("org", "Desconocida")
    timezone = location.get("timezone", "Desconocida")

    hora = datetime.now(
        ZoneInfo("America/Bogota")
    ).strftime("%d/%m/%Y %I:%M:%S %p")

    mapa = "No disponible"

    if latitude is not None and longitude is not None:
        mapa = f"https://www.google.com/maps?q={latitude},{longitude}"

    message = (
        "💌 **Alguien ha abierto la carta**\n\n"

        "📍 **Ubicación aproximada**\n"
        f"🏙️ Ciudad: `{city}`\n"
        f"🗺️ Región: `{region}`\n"
        f"🌎 País: `{country}`\n"
        f"📮 Código postal: `{postal}`\n"
        f"📌 Coordenadas aproximadas: `{latitude}, {longitude}`\n"
        f"🗺️ Mapa: {mapa}\n\n"

        "🌐 **Conexión**\n"
        f"IP: `{ip}`\n"
        f"🏢 Organización/ISP: `{org}`\n"
        f"🕐 Zona horaria: `{timezone}`\n\n"

        "📱 **Navegador / dispositivo**\n"
        f"`{user_agent}`\n\n"

        f"⏰ **Hora:** `{hora}`"
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