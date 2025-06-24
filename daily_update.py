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

def generate_tips(matches):
    tips = []
    if "bets" in book:
    for bet in book["bets"]:
        bookmakers = match.get("bookmakers", [])
        for bookmaker in bookmakers:
            markets = bookmaker.get("markets", [])
            for market in markets:
                if "bets" in market:
                    for bet in market["bets"]:
                        if bet.get("name") == "Over/Under 2.5":
                            tips.append({
                                "match": f"{match['teams']['home']['name']} vs {match['teams']['away']['name']}",
                                "tip": "Over 2.5 goals",
                                "justification": "Based on real-time odds analysis"
                            })
    return tips

def generate_anomalies(matches):
    anomalies = []
    for match in matches:
        bookmakers = match.get("bookmakers", [])
        for bookmaker in bookmakers:
            markets = bookmaker.get("markets", [])
            for market in markets:
                if "bets" in market:
                    for bet in market["bets"]:
                        odd_value = bet.get("value", 0)
                        if odd_value > 1.5:  # Example threshold for anomaly
                            anomalies.append({
                                "match": f"{match['teams']['home']['name']} vs {match['teams']['away']['name']}",
                                "suspect_team": bookmaker.get("title", "Unknown"),
                                "odd_difference": odd_value,
                                "reason": "Abnormal odds variation"
                            })
    return anomalies

def generate_scores(matches):
    scores = []
    for match in matches:
        goals = match.get("goals", {})
        home_goals = goals.get("home", 0)
        away_goals = goals.get("away", 0)
        scores.append({
            "match": f"{match['teams']['home']['name']} vs {match['teams']['away']['name']}",
            "exact_score": f"{home_goals} - {away_goals}",
            "sites_count": 15  # Placeholder
        })
    return scores

def save_json(data, filename):
    folder = Path("static/data")
    folder.mkdir(parents=True, exist_ok=True)
    filepath = folder / filename
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    try:
        matches = get_matches_today()
        save_json(generate_tips(matches), "conseils.json")
        save_json(generate_anomalies(matches), "anomalies.json")
        save_json(generate_scores(matches), "scores.json")
        print("✅ Data updated successfully:", datetime.now())
    except Exception as e:
        print(f"❌ Error during update: {e}")
