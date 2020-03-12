from app.models.__init__ import db

class CustomRank(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    custom_message = db.Column(db.String(500), nullable=False)
    flag_count = db.Column(db.Integer, nullable=False)

    def __init__(self, id, custom_message, flag_count):
        self.id = id
        self.custom_message = custom_message
        self.flag_count = flag_count

    def get_id(self):
        # returns the id.
        return self.id

    def as_dict(self):
        return {
            "id": self.id,
            "custom_message": self.custom_message,
            "flag_count": self.flag_count,
        }

    def __repr__(self):
        return '<CustomRank {}>'.format(self.id)