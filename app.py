from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)

@app.route('/')
def accueil():
    return render_template('index.html')

@app.route('/conseils')
def conseils():
    with open("static/data/conseils.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return render_template("conseils.html", conseils=data)

@app.route('/anomalies')
def anomalies():
    with open("static/data/anomalies.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return render_template("anomalies.html", anomalies=data)

@app.route('/scores')
def scores():
    with open("static/data/scores.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return render_template("scores.html", scores=data)

if __name__ == '__main__':
    app.run(debug=True)
