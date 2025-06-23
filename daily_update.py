import json
import random
from datetime import datetime
from pathlib import Path

matchs = [
    ("Liverpool", "Bournemouth"),
    ("Tottenham", "Burnley"),
    ("Chelsea", "Crystal Palace"),
    ("Man City", "Wolves"),
    ("Arsenal", "Everton"),
    ("Lyon", "Marseille"),
    ("Barça", "Sevilla"),
    ("Real Madrid", "Valencia")
]

def generer_conseils():
    conseils = []
    for equipe1, equipe2 in random.sample(matchs, 5):
        buts_probables = random.choice(["Plus de 2.5 buts", "Moins de 2.5 buts"])
        justification = "Variations suspectes et écart de cotes élevé"
        conseils.append({
            "match": f"{equipe1} vs {equipe2}",
            "conseil": buts_probables,
            "justification": justification
        })
    return conseils

def generer_anomalies():
    anomalies = []
    for equipe1, equipe2 in random.sample(matchs, 4):
        anomalies.append({
            "match": f"{equipe1} vs {equipe2}",
            "equipe_suspecte": random.choice([equipe1, equipe2]),
            "ecart_cote": round(random.uniform(0.6, 2.5), 2),
            "raison": "Variation de cote anormale"
        })
    return anomalies

def generer_scores():
    scores = []
    for equipe1, equipe2 in random.sample(matchs, 5):
        score_exact = f"{random.randint(0, 3)} - {random.randint(0, 3)}"
        scores.append({
            "match": f"{equipe1} vs {equipe2}",
            "score_exact": score_exact,
            "nombre_sites": random.randint(15, 25)
        })
    return scores

# Chemin des fichiers de sortie
dossier = Path("static/data")
dossier.mkdir(parents=True, exist_ok=True)

with open(dossier / "conseils.json", "w", encoding="utf-8") as f:
    json.dump(generer_conseils(), f, indent=2, ensure_ascii=False)

with open(dossier / "anomalies.json", "w", encoding="utf-8") as f:
    json.dump(generer_anomalies(), f, indent=2, ensure_ascii=False)

with open(dossier / "scores.json", "w", encoding="utf-8") as f:
    json.dump(generer_scores(), f, indent=2, ensure_ascii=False)

print("✅ Données mises à jour avec succès :", datetime.now())
