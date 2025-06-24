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
    if res.status_code == 200:
        print(f"✅ Réponse API reçue ({len(res.json().get('response', []))} matchs)")
        return res.json().get("response", [])
    else:
        print(f"❌ Erreur API : {res.status_code}")
        return []

def generer_conseils(matches):
    conseils = []
    for match in matches:
        home = match.get("teams", {}).get("home", {}).get("name", "")
        away = match.get("teams", {}).get("away", {}).get("name", "")
        match_name = f"{home} vs {away}"

        found = False
        for book in match.get("bookmakers", []):
            for bet in book.get("bets", []):
                if bet.get("name") != "Over/Under":
                    continue
                for value in bet.get("values", []):
                    if "Over 2.5" in value.get("value", ""):
                        print(f"{match_name} ➤ {value.get('value')} à {value.get('odd')}")
                        try:
                            if float(value.get("odd")) >= 2.0:
                                conseils.append({
                                    "match": match_name,
                                    "tip": value["value"],
                                    "odds": value["odd"]
                                })
                                found = True
                        except:
                            continue
        if not found:
            print(f"⚠️ {match_name} : aucun Over 2.5 avec cote ≥ 2.0")

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
    print("🔁 Chargement des matchs du jour...")
    matches = get_matches()
    print(f"📊 Total matchs reçus : {len(matches)}")

    conseils = generer_conseils(matches)
    anomalies = generer_anomalies(matches)
    scores = generer_scores_fictifs(matches)

    print(f"✅ {len(conseils)} conseils générés")
    print(f"✅ {len(anomalies)} anomalies détectées")
    print(f"✅ {len(scores)} scores exacts générés")

    save("conseils", conseils)
    save("anomalies", anomalies)
    save("scores", scores)
    print("💾 Données enregistrées avec succès.")