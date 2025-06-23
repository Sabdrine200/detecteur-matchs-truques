from flask import Blueprint, render_template
from datetime import datetime

anomalies_bp = Blueprint('anomalies', __name__)

@anomalies_bp.route('/anomalies')
def afficher_anomalies():
    anomalies = [
        {
            "match": "Liverpool vs Bournemouth",
            "details": [
                "⚠️ Anomalie détectée sur Bournemouth (écart 3.00)",
                "⚠️ Anomalie détectée sur Draw (écart 1.05)"
            ]
        },
        {
            "match": "Tottenham vs Burnley",
            "details": [
                "⚠️ Anomalie détectée sur Burnley (écart 2.10)",
                "⚠️ Anomalie détectée sur Draw (écart 0.97)"
            ]
        }
    ]
    date_du_jour = datetime.now().strftime('%d/%m/%Y')
    return render_template("anomalies.html", anomalies=anomalies, date=date_du_jour)
