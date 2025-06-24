import requests
import os
from datetime import datetime

API_KEY = os.getenv("API_FOOTBALL_KEY")  # Ta clé API-Football depuis les variables Render

BASE_URL = "https://v3.football.api-sports.io/fixtures"

def get_matches_today():
    headers = {
        "x-apisports-key": API_KEY
    }

    params = {
        "date": datetime.today().strftime("%Y-%m-%d"),
        "timezone": "Europe/Paris"
    }

    try:
        response = requests.get(BASE_URL, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        return [match["fixture"] | {
            "homeTeam": match["teams"]["home"]["name"],
            "awayTeam": match["teams"]["away"]["name"],
            "bookmakers": match.get("bookmakers", [])
        } for match in data.get("response", [])]

    except Exception as e:
        print(f"Erreur API : {e}")
        return []
