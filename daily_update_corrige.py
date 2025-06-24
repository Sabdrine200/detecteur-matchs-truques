
import requests
import json
import datetime

API-Key: d99f9adb8fefff08f04486c14b23e6b8
HEADERS = {
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": "api-football-v1.p.rapidapi.com"
}

def get_matches_today():
    today = datetime.date.today().strftime("%Y-%m-%d")
    url = f"https://api-football-v1.p.rapidapi.com/v3/fixtures?date={today}"
    response = requests.get(url, headers=HEADERS)
    return response.json().get("response", [])

def generer_conseils(matches):
    conseils = []
    for match in matches:
        try:
            fixture = match.get("fixture", {})
            teams = match.get("teams", {})
            league = match.get("league", {})

            match_id = fixture.get("id")
            home = teams.get("home", {}).get("name")
            away = teams.get("away", {}).get("name")
            league_name = league.get("name")

            odds_url = f"https://api-football-v1.p.rapidapi.com/v3/odds?fixture={match_id}"
            odds_response = requests.get(odds_url, headers=HEADERS)
            odds_data = odds_response.json().get("response", [])

            for book in odds_data:
                for bet in book.get("bets", []):
                    if bet.get("name") == "Over/Under":
                        for value in bet.get("values", []):
                            label = value.get("value")
                            odd = float(value.get("odd", 0))

                            if label == "Over 2.5" and odd >= 2.0:
                                conseils.append({
                                    "match": f"{home} vs {away}",
                                    "conseil": "Plus de 2.5 buts",
                                    "cote": odd,
                                    "justification": f"{home} attaque fort, {away} défend mal. Bon pari selon cotes."
                                })
                            elif label == "Under 2.5" and odd >= 2.0:
                                conseils.append({
                                    "match": f"{home} vs {away}",
                                    "conseil": "Moins de 2.5 buts",
                                    "cote": odd,
                                    "justification": f"Match fermé prévu entre {home} et {away}. Défenses solides."
                                })

        except Exception as e:
            print(f"Erreur pour le match {home} vs {away} : {e}")
            continue

    return conseils[:5]

# Création du fichier JSON
with open("data/conseils.json", "w", encoding="utf-8") as f:
    json.dump(generer_conseils(get_matches_today()), f, indent=2, ensure_ascii=False)
