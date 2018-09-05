from flask import jsonify, request

from app import Score, db
from app.api import bp
import werkzeug.exceptions as ex
from config import Config

@bp.route('/scoreboard', methods=['POST'])
def scoreboard():
    data = request.get_json()

    if data is None or data["fkey"] != Config().fkey:
        return ex.Forbidden()

    scoreboard_map = []

    scores = Score.query.order_by(Score.flag_count.desc()).all()
    for score in scores:
        scoreboard_map.append({"username": score.username, "flag_count": score.flag_count})

    response = jsonify(scoreboard_map)
    response.status_code = 200
    return response

@bp.route('/scoreboard/add', methods=['POST'])
def add_scoreboard():
    data = request.get_json()

    if data is None or data["fkey"] != Config().fkey:
        return ex.Forbidden()

    #Delete existing records for this user
    db.engine.execute(f"DELETE FROM score WHERE username LIKE '%%{data['username']}%%'")

    #Create new enty
    score = Score(username=data['username'], flag_count=data['flag_count'])
    db.session.add(score)
    db.session.commit()

    response = jsonify({"message": "Scoreboard entry added."})
    response.status_code = 200
    return response