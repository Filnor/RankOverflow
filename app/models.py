from app import db

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(90), index=True)
    flag_count = db.Column(db.Integer, index=True)
