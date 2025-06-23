from flask import Blueprint, render_template
from datetime import datetime

conseils_bp = Blueprint('conseils', __name__)

@conseils_bp.route('/conseils')
def afficher_conseils():
    conseils_du_jour = [
        {
            "match": "Liverpool vs Bournemouth",
            "conseil": "Plus de 2.5 buts",
            "justification": "Favori très fort et outsider fragile avec variations suspectes"
        },
        {
            "match": "Tottenham vs Burnley",
            "conseil": "Plus de 2.5 buts",
            "justification": "Historique de buts élevé et cotes en baisse"
        }
    ]
    date_du_jour = datetime.now().strftime('%d/%m/%Y')
    return render_template("conseils.html", conseils=conseils_du_jour, date=date_du_jour)
