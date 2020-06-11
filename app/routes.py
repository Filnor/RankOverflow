from datetime import date
from flask import render_template
from app import app
from config import Config
from app.models.Score import Score
from urllib.request import urlopen
import io
import gzip
import json
import urllib
from operator import itemgetter

def _get_user_name_and_profile_link(user_id):
    """
    Get an user object for the specified user id from the API
    """
    try:
        response = urlopen(f"https://api.stackexchange.com/2.2/users/{user_id}?order=desc&sort=reputation&site=stackoverflow&key=K8pani4F)SeUn0QlbHQsbA((").read()
        buffer = io.BytesIO(response)
        gzipped_file = gzip.GzipFile(fileobj=buffer)
        content = gzipped_file.read()
        users = json.loads(content.decode("utf-8"))
        return users["items"][0]["display_name"], users["items"][0]["link"]
    except urllib.error.HTTPError as e:
        return None

@app.route('/')
@app.route('/index')
def index():
    current_year = date.today().year
    return render_template('index.html', current_year=current_year)

@app.route('/scoreboard')
def scoreboard():
    objects = Score.query.all()

    scores = []
    
    for obj in objects:
        name_profile_link = _get_user_name_and_profile_link(obj.id)
        if obj.flags >= 50:
            scores.append({"profile_link": name_profile_link[1], "username": name_profile_link[0], "flag_count": obj.flags})

    #Sort data
    scores = sorted(scores, key=itemgetter("flag_count"), reverse=True)
    return render_template('scoreboard.html', scores=scores)

@app.route('/blank')
def blank():
    return ""
