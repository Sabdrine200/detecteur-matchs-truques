import requests
import json
import datetime

API_KEY = "d99f9adb8fefff08f04486c14b23e6b8"
API_HOST = "api-football-v1.p.rapidapi.com"
BASE_URL = "https://api-football-v1.p.rapidapi.com/v3/odds"

HEADERS = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": API_HOST
}

def get_matches_today():
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    url = f"{BASE_URL}?date={today}&bookmaker=6"
    response = requests.get(url, headers=HEADERS)
    return response.json().get("response", [])

def analyser_match(match):
    anomalies = []
    conseils = []

    try:
        bookmakers = match.get("bookmakers", [])
        if not bookmakers:
            return anomalies, conseils

        bets = bookmakers[0].get("bets", [])
    except Exception:
        return anomalies, conseils

    for bet in bets:
        if bet["name"] == "Match Winner":
            for value in bet.get("values", []):
                try:
                    cote = float(value["odd"])
                    label = value["value"]
                    if cote >= 5.0:
                        anomalies.append({
                            "match": f'{match["teams"]["home"]["name"]} vs {match["teams"]["away"]["name"]}',
                            "choix": label,
                            "cote": cote
                        })
                except:
                    continue
        elif bet["name"] == "Over/Under":
            for value in bet.get("values", []):
                try:
                    if value["value"] == "Over 2.5" and float(value["odd"]) >= 2.00:
                        conseils.append({
                            "match": f'{match["teams"]["home"]["name"]} vs {match["teams"]["away"]["name"]}',
                            "conseil": "Plus de 2.5 buts",
                            "cote": value["odd"]
                        })
                except:
                    continue

    return anomalies, conseils

def generer_conseils(liste_matchs):
    tous_conseils = []
    for match in liste_matchs:
        _, conseils = analyser_match(match)
        tous_conseils.extend(conseils)
    return tous_conseils[:5]

def generer_anomalies(liste_matchs):
    toutes_anomalies = []
    for match in liste_matchs:
        anomalies, _ = analyser_match(match)
        toutes_anomalies.extend(anomalies)
    return toutes_anomalies

# Exécution de la génération
matches = get_matches_today()

with open("data/conseils.json", "w", encoding="utf-8") as f:
    json.dump(generer_conseils(matches), f, indent=2, ensure_ascii=False)

with open("data/anomalies.json", "w", encoding="utf-8") as f:
    json.dump(generer_anomalies(matches), f, indent=2, ensure_ascii=False)
