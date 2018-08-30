from flask import jsonify, request
from app.api import bp
import werkzeug.exceptions as ex
import csv

@bp.route('/scoreboard', methods=['POST'])
def scoreboard():
    data = request.get_json()

    if data is None or data["fkey"] != "f0197a422ba110a461a850a54ca2475e0745fd9d":
        return ex.Forbidden()

    scoreboard_map = []

    with open("data.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=";")
        for row in csv_reader:
            scoreboard_map.append({"username": row[0] , "flag_count": row[1]})

    response = jsonify(scoreboard_map)
    response.status_code = 200
    return response

@bp.route('/scoreboard/clear', methods=['POST'])
def clear_scoreboard():
    data = request.get_json()

    if data is None or data["fkey"] != "<REDACTED>":
        return ex.Forbidden()

    filename = "data.csv"
    # opening the file with w+ mode truncates the file
    f = open(filename, "w+")
    f.close()

    response = jsonify({"message": "Scoreboard data deleted."})
    response.status_code = 200
    return response

@bp.route('/scoreboard/add', methods=['POST'])
def add_scoreboard():
    data = request.get_json()

    if data is None or data["fkey"] != "<REDACTED>":
        return ex.Forbidden()

    with open("data.csv", "a") as f:
        f.write(f"{data['username']};{data['flag_count']}\n")

    response = jsonify({"message": "Scoreboard entry added."})
    response.status_code = 200
    return response