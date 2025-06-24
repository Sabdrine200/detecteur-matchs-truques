import requests
import json
from datetime import datetime
from pathlib import Path

API_KEY = "ba0823b863247482548df4066dd2a51f"
API_HOST = "api-football-v1.p.rapidapi.com"
DATE_TODAY = datetime.today().strftime('%Y-%m-%d')

HEADERS = {
    "x-rapidapi-host": API_HOST,
    "x-rapidapi-key": API_KEY
}

def get_matches_today():
    url = f"https://{API_HOST}/v3/fixtures?date={DATE_TODAY}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    data = response.json()
    return data.get("response", [])

def generer_conseils(matches):
    conseils = []
    for match in matches:
        # Exemple: on va lire les bookmakers, marchés et bets
        bookmakers = match.get("bookmakers", [])
        for bookmaker in bookmakers:
            markets = bookmaker.get("markets", [])
            for market in markets:
                if "bets" in market:
                    for bet in market["bets"]:
                        if bet.get("name") == "Plus de 2.5 buts":
                            conseils.append({
                                "match": f"{match['teams']['home']['name']} vs {match['teams']['away']['name']}",
                                "conseil": "Plus de 2.5 buts",
                                "justification": "Analyse des cotes en temps réel"
                            })
    return conseils

def generer_anomalies(matches):
    anomalies = []
    for match in matches:
        bookmakers = match.get("bookmakers", [])
        for bookmaker in bookmakers:
            markets = bookmaker.get("markets", [])
            for market in markets:
                if "bets" in market:
                    for bet in market["bets"]:
                        # Exemple d'anomalie fictive
                        ecart_cote = bet.get("value", 0)
                        if ecart_cote > 1.5:
                            anomalies.append({
                                "match": f"{match['teams']['home']['name']} vs {match['teams']['away']['name']}",
                                "equipe_suspecte": bookmaker.get("title", "Inconnu"),
                                "ecart_cote": ecart_cote,
                                "raison": "Variation de cote anormale"
                            })
    return anomalies

def generer_scores(matches):
    scores = []
    for match in matches:
        score_home = match.get("goals", {}).get("home", 0)
        score_away = match.get("goals", {}).get("away", 0)
        scores.append({
            "match": f"{match['teams']['home']['name']} vs {match['teams']['away']['name']}",
            "score_exact": f"{score_home} - {score_away}",
            "nombre_sites": 15  # Par défaut, fictif
        })
    return scores

def sauvegarder_json(data, nom_fichier):
    dossier = Path("static/data")
    dossier.mkdir(parents=True, exist_ok=True)
    chemin = dossier / nom_fichier
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    try:
        matches = get_matches_today()
        sauvegarder_json(generer_conseils(matches), "conseils.json")
        sauvegarder_json(generer_anomalies(matches), "anomalies.json")
        sauvegarder_json(generer_scores(matches), "scores.json")
        print("✅ Données mises à jour avec succès :", datetime.now())
    except Exception as e:
        print(f"❌ Erreur lors de la mise à jour : {e}")
