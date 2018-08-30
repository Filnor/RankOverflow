from datetime import date
from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    current_year = date.today().year
    return render_template('index.html', current_year=current_year)

@app.route('/scoreboard')
def scoreboard():
    current_year = date.today().year
    return render_template('scoreboard.html')

@app.route('/blank')
def blank():
    return ""
