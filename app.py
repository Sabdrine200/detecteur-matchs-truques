from flask import Flask, render_template

application = Flask(__name__)

@application.route('/')
def accueil():
    return render_template('home.html')

@application.route('/conseils')
def conseils():
    return render_template('conseils.html')

@application.route('/anomalies')
def anomalies():
    return render_template('anomalies.html')

@application.route('/scores')
def scores():
    return render_template('scores.html')

if __name__ == '__main__':
    application.run()
