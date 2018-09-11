import gzip
import io
import json
import urllib.error
import logging
from urllib.request import urlopen
from flask import jsonify, request
from app import Score, db
from app.api import bp
from config import Config
import werkzeug.exceptions as ex

@bp.route('/scoreboard', methods=['POST'])
def scoreboard():
    data = request.get_json()

    if data is None or data["fkey"] != Config().fkey:
        return ex.Forbidden()

    scoreboard_map = []

    scores = Score.query.order_by(Score.flag_count.desc()).all()
    for score in scores:
        scoreboard_map.append({"username": _get_user_name(score.user_id), "flag_count": score.flag_count})

    response = jsonify(scoreboard_map)
    response.status_code = 200
    return response

@bp.route('/scoreboard/add', methods=['POST'])
def add_scoreboard():
    data = request.get_json()

    if data is None or data["fkey"] != Config().fkey:
        return ex.Forbidden()

    #keep IDs low
    existing_record = False

    #Skip if flag count is unchanged
    if Score.query.filter_by(user_id=data['user_id']).count() > 0:
        existing_record = True
        if Score.query.filter_by(user_id=data['user_id']).all()[0].flag_count == data['flag_count']:
            response = jsonify({"message": "Flag count unchanged. Nothing was changed."})
            response.status_code = 200
            return response

    #Delete existing records for this user
    if existing_record:
        db.engine.execute(f"UPDATE score SET flag_count = {data['flag_count']} WHERE user_id = {data['user_id']}")
    else:
        db.engine.execute(f"DELETE FROM score WHERE user_id = {data['user_id']}")

    #Create new enty
    if not existing_record:
        score = Score(user_id=data['user_id'], flag_count=data['flag_count'])
        db.session.add(score)
        db.session.commit()

    response = jsonify({"message": f"Scoreboard entry {'added' if not existing_record else 'updated'}."})
    response.status_code = 200
    return response

def _get_user_name(user_id):
    """
    Get an user object for the specified user id from the API
    """
    try:
        response = urlopen(f"https://api.stackexchange.com/2.2/users/{user_id}?order=desc&sort=reputation&site=stackoverflow&key=K8pani4F)SeUn0QlbHQsbA((").read()
        buffer = io.BytesIO(response)
        gzipped_file = gzip.GzipFile(fileobj=buffer)
        content = gzipped_file.read()
        users = json.loads(content.decode("utf-8"))
        return users["items"][0]["display_name"]
    except urllib.error.HTTPError as e:
        return None