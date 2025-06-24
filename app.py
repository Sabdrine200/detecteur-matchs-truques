from flask import Flask, render_template
import json
import os

app = Flask(__name__)

@app.route('/')
def accueil():
    return render_template('index.html')

@app.route('/conseils')
def conseils():
    try:
        with open("static/data/conseils.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        data = []
        print(f"Erreur dans /conseils : {e}")
    return render_template("conseils.html", conseils=data)

@app.route('/anomalies')
def anomalies():
    try:
        with open("static/data/anomalies.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        data = []
        print(f"Erreur dans /anomalies : {e}")
    return render_template("anomalies.html", anomalies=data)

@app.route('/scores')
def scores():
    try:
        with open("static/data/scores.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        data = []
        print(f"Erreur dans /scores : {e}")
    return render_template("scores.html", scores=data)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
