import json
import requests
from datetime import datetime

API_KEY = "ba0823b863247482548df4066dd2a51f"
API_HOST = "api-football-v1.p.rapidapi.com"
DATE_TODAY = datetime.today().strftime('%Y-%m-%d')

HEADERS = {
    "x-rapidapi-host": API_HOST,
    "x-rapidapi-key": API_KEY
}

def get_matches_today():
    url = "https://api-football-v1.p.rapidapi.com/v3/odds"
    params = {
        "date": DATE_TODAY,
        "bet": "Over/Under"
    }

    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code == 200:
        return response.json().get("response", [])
    else:
        print(f"Erreur API : {response.status_code}")
        return []

def generer_conseils(matches):
    conseils = []
    for match in matches:
        fixture = match.get("fixture", {})
        teams = match.get("teams", {})
        home = teams.get("home", {}).get("name", "")
        away = teams.get("away", {}).get("name", "")
        match_name = f"{home} vs {away}"

        bookmakers = match.get("bookmakers", [])
        for book in bookmakers:
            bets = book.get("bets", [])
            for bet in bets:
                if bet.get("name") != "Over/Under":
                    continue

                for value in bet.get("values", []):
                    if value.get("value") == "Over 2.5" and float(value.get("odd", 0)) >= 2.0:
                        conseils.append({
                            "match": match_name,
                            "tip": "Over 2.5",
                            "odds": value["odd"]
                        })
    return conseils

def save_json(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    print("🔁 Récupération des matchs en cours...")
    matchs = get_matches_today()
    if not matchs:
        print("⚠️ Aucun match trouvé.")
    else:
        print(f"✅ {len(matchs)} matchs récupérés.")
        conseils = generer_conseils(matchs)
        save_json("data/conseils.json", conseils)
        print(f"💾 {len(conseils)} conseils sauvegardés.")
