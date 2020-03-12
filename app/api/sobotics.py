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

@bp.route('/scoreboard/store', methods=['POST'])
def store_entry():
    data = request.get_json()

    if data is None or data["fkey"] != Config().fkey:
        return ex.Forbidden()

    response = None
    db.session.close()
    #db.dispose()
    try:
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
    except BaseException:
        db.session.rollback()
        response.status_code = 503
    finally:
       db.session.close()
       #db.dispose()
       return response
