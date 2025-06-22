from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def accueil():
    return render_template("index.html")

@app.route("/conseils")
def conseils():
    return render_template("conseils.html")

@app.route("/anomalies")
def anomalies():
    return render_template("anomalies.html")

@app.route("/scores")
def scores():
    return render_template("scores.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
