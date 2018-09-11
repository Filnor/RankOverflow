from app import db

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, index=True)
    flag_count = db.Column(db.Integer, index=True)
