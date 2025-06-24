
import json
import requests
from datetime import datetime

API_KEY = "ba0823b863247482548df4066dd2a51f"
API_HOST = "api-football-v1.p.rapidapi.com"
TODAY = datetime.today().strftime('%Y-%m-%d')

HEADERS = {
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": API_HOST
}

def get_matches():
    url = "https://api-football-v1.p.rapidapi.com/v3/odds"
    params = {"date": TODAY, "bet": "Over/Under"}
    res = requests.get(url, headers=HEADERS, params=params)
    return res.json().get("response", []) if res.status_code == 200 else []

def generer_conseils(matches):
    conseils = []
    for match in matches:
        home = match.get("teams", {}).get("home", {}).get("name", "")
        away = match.get("teams", {}).get("away", {}).get("name", "")
        match_name = f"{home} vs {away}"
        for book in match.get("bookmakers", []):
            for bet in book.get("bets", []):
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

def generer_anomalies(matches):
    anomalies = []
    for match in matches:
        if len(match.get("bookmakers", [])) >= 3:
            anomalies.append({
                "match": f"{match['teams']['home']['name']} vs {match['teams']['away']['name']}",
                "alert": "Activité de cotes anormale"
            })
    return anomalies

def generer_scores_fictifs(matches):
    scores = []
    for match in matches[:5]:
        scores.append({
            "match": f"{match['teams']['home']['name']} vs {match['teams']['away']['name']}",
            "score": "1-1",
            "sites": 16
        })
    return scores

def save(name, data):
    with open(f"data/{name}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    print("🔁 Chargement des matchs...")
    matches = get_matches()
    print(f"✔️ {len(matches)} matchs chargés")

    conseils = generer_conseils(matches)
    anomalies = generer_anomalies(matches)
    scores = generer_scores_fictifs(matches)

    save("conseils", conseils)
    save("anomalies", anomalies)
    save("scores", scores)
    print("✅ Données enregistrées.")
