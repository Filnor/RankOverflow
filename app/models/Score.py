from app.models.__init__ import db

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    flags = db.Column(db.Integer, nullable=False)

    def __init__(self, id, flags):
        self.id = id
        self.flags = flags

    def get_id(self):
        # returns the id.
        return self.id

    def as_dict(self):
        return {
            "id": self.id,
            "flags": self.flags,
        }

    def __repr__(self):
        return '<Score {}>'.format(self.id)