from flask import Flask, render_template
import json

app = Flask(__name__)

def load_json(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/conseils")
def conseils():
    data = load_json("data/conseils.json")
    return render_template("conseils.html", conseils=data)

@app.route("/anomalies")
def anomalies():
    data = load_json("data/anomalies.json")
    return render_template("anomalies.html", anomalies=data)

@app.route("/scores")
def scores():
    data = load_json("data/scores.json")
    return render_template("scores.html", scores=data)

if __name__ == "__main__":
    app.run(debug=True)