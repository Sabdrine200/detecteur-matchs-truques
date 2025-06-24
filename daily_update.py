import requests
import json
from datetime import datetime
from pathlib import Path

API_KEY = "ba0823b863247482548df4066dd2a51f"
BASE_URL = "https://v3.football.api-sports.io"
HEADERS = {"x-apisports-key": API_KEY}

def get_matches_today():
    today = datetime.now().strftime('%Y-%m-%d')
    url = f"{BASE_URL}/fixtures?date={today}"
    res = requests.get(url, headers=HEADERS)
    return res.json().get("response", [])

def get_odds_over_under(fixture_id):
    url = f"{BASE_URL}/odds?fixture={fixture_id}&bet=5"  # bet=5 = Over/Under 2.5
    res = requests.get(url, headers=HEADERS)
    return res.json().get("response", [])

def generer_conseils(matchs):
    conseils = []
    for match in matchs:
        home = match["teams"]["home"]["name"]
        away = match["teams"]["away"]["name"]
        fixture_id = match["fixture"]["id"]

        odds = get_odds_over_under(fixture_id)
        for book in odds:
            for bet in book["bets"]:
                for val in bet["values"]:
                    if val["value"] in ["Over 2.5", "Under 2.5"]:
                        conseil = {
                            "match": f"{home} vs {away}",
                            "conseil": val["value"].replace("Over", "Plus de").replace("Under", "Moins de"),
                            "cote": val["odd"],
                            "justification": "Analyse des cotes en temps réel"
                        }
                        conseils.append(conseil)
                        break
            break
        if len(conseils) >= 5:
            break
    return conseils

def generer_anomalies(matchs):
    anomalies = []
    for match in matchs:
        home = match["teams"]["home"]["name"]
        away = match["teams"]["away"]["name"]
        fixture_id = match["fixture"]["id"]

        odds = get_odds_over_under(fixture_id)
        for book in odds:
            for bet in book["bets"]:
                values = bet["values"]
                if len(values) >= 2:
                    ecart = abs(float(values[0]["odd"]) - float(values[1]["odd"]))
                    if ecart >= 1.5:  # seuil d’anomalie
                        anomalies.append({
                            "match": f"{home} vs {away}",
                            "equipe_suspecte": home if float(values[0]["odd"]) < float(values[1]["odd"]) else away,
                            "ecart_cote": round(ecart, 2),
                            "raison": "Variation de cote anormale"
                        })
        if len(anomalies) >= 4:
            break
    return anomalies

def generer_scores(matchs):
    scores = []
    for match in matchs[:5]:
        home = match["teams"]["home"]["name"]
        away = match["teams"]["away"]["name"]
        score = f"{datetime.now().second % 4} - {datetime.now().minute % 4}"  # score simulé
        scores.append({
            "match": f"{home} vs {away}",
            "score_exact": score,
            "nombre_sites": 15  # simulé pour l’instant
        })
    return scores

# Dossier de sortie
dossier = Path("static/data")
dossier.mkdir(parents=True, exist_ok=True)

with open(dossier / "conseils.json", "w", encoding="utf-8") as f:
    json.dump(generer_conseils(get_matches_today()), f, indent=2, ensure_ascii=False)

with open(dossier / "anomalies.json", "w", encoding="utf-8") as f:
    json.dump(generer_anomalies(get_matches_today()), f, indent=2, ensure_ascii=False)

with open(dossier / "scores.json", "w", encoding="utf-8") as f:
    json.dump(generer_scores(get_matches_today()), f, indent=2, ensure_ascii=False)

print("✅ Données mises à jour avec succès :", datetime.now())
