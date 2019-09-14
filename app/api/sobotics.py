import gzip
import io
import json
import urllib.error
from operator import itemgetter
from urllib.request import urlopen
from flask import jsonify, request
from app.api import bp
from config import Config
from app.models import db
from app.models.Score import Score
import werkzeug.exceptions as ex


@bp.route('/scoreboard', methods=['POST'])
def get_scoreboard():
    data = request.get_json()

    if data is None or data["fkey"] != Config().fkey:
        return ex.Forbidden()

    objects = Score.query.all()

    scores = []
    
    for obj in objects:
        name_profile_link = _get_user_name_and_profile_link(obj.id)
        scores.append({"profile_link": name_profile_link[1], "username": name_profile_link[0], "flag_count": obj.flags})

    #Sort data
    scores = sorted(scores, key=itemgetter("flag_count"), reverse=True)

    response = jsonify(scores)
    response.status_code = 200
    return response

@bp.route('/scoreboard/store', methods=['POST'])
def store_entry():
    data = request.get_json()

    if data is None or data["fkey"] != Config().fkey:
        return ex.Forbidden()

    return_entry = {}
    if len(Score.query.filter_by(id=data["id"]).all()) == 1:
        existing_score = Score.query.filter_by(id=data["id"]).first()
        existing_score.flags = data["flags"]
        db.engine.execute("UPDATE score SET flags = '{}' WHERE id = {}".format(data["flags"], data["id"]))
        return_entry = existing_score
    else:
        scoreboard_entry = Score(id=data["id"], flags=data["flags"])
        return_entry = scoreboard_entry
        db.session.add(scoreboard_entry)
        db.session.commit()

    response = jsonify(return_entry.as_dict())
    response.status_code = 200
    return response

def _get_user_name_and_profile_link(user_id):
    """
    Get an user object for the specified user id from the API
    """
    try:
        response = urlopen(
            f"https://api.stackexchange.com/2.2/users/{user_id}?order=desc&sort=reputation&site=stackoverflow&key=K8pani4F)SeUn0QlbHQsbA((").read()
        buffer = io.BytesIO(response)
        gzipped_file = gzip.GzipFile(fileobj=buffer)
        content = gzipped_file.read()
        users = json.loads(content.decode("utf-8"))
        return users["items"][0]["display_name"], users["items"][0]["link"]
    except urllib.error.HTTPError as e:
        return None
