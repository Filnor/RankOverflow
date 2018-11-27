import gzip
import io
import json
import urllib.error
from operator import itemgetter
from urllib.request import urlopen
from flask import jsonify, request
from app.api import bp
from app import db
from config import Config
import werkzeug.exceptions as ex


@bp.route('/scoreboard', methods=['POST'])
def scoreboard():
    data = request.get_json()

    if data is None or data["fkey"] != Config().fkey:
        return ex.Forbidden()

    scoreboard_map = []

    #Load data
    docs = db.collection(u"scores").get()
    for doc in docs:
        score = doc.to_dict()
        if int(score["flag_count"]) <= 499:
            continue
        user_name_and_profile_link = _get_user_name_and_profile_link(score["user_id"])
        scoreboard_map.append({"profile_link": user_name_and_profile_link[1], "username": user_name_and_profile_link[0], "flag_count": score["flag_count"]})

    #Sort data
    scoreboard_map = sorted(scoreboard_map, key=itemgetter("flag_count"))

    response = jsonify(scoreboard_map)
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
