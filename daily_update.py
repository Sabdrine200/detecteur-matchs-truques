import json
from datetime import datetime

API_KEY = "ba0823b863247482548df4066dd2a51f"  # Ta clé API déjà incluse

def generate_conseils():
    return [
        {"match": "Team A vs Team B", "tip": "+2.5 buts", "odds": 2.1},
        {"match": "Team C vs Team D", "tip": "-2.5 buts", "odds": 2.4}
    ]

def generate_anomalies():
    return [
        {"match": "Team X vs Team Y", "alert": "Chute de cote soudaine"},
        {"match": "Team Z vs Team W", "alert": "Activité suspecte"}
    ]

def generate_scores():
    return [
        {"match": "Team A vs Team B", "score": "2-1", "sites": 16},
        {"match": "Team C vs Team D", "score": "1-1", "sites": 15}
    ]

def save_json(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    save_json("data/conseils.json", generate_conseils())
    save_json("data/anomalies.json", generate_anomalies())
    save_json("data/scores.json", generate_scores())
    print("✅ Données mises à jour avec succès.")
