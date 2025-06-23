from flask import Blueprint, render_template
from datetime import datetime

scores_bp = Blueprint('scores', __name__)

@scores_bp.route('/scores')
def afficher_scores():
    scores = [
        {
            "match": "Liverpool vs Bournemouth",
            "score": "2-1",
            "nb_sites": 17
        },
        {
            "match": "Tottenham vs Burnley",
            "score": "3-0",
            "nb_sites": 18
        },
        {
            "match": "Chelsea vs Crystal Palace",
            "score": "1-1",
            "nb_sites": 16
        }
    ]
    date_du_jour = datetime.now().strftime('%d/%m/%Y')
    return render_template("scores.html", scores=scores, date=date_du_jour)
