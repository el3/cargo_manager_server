from backend.model import db
from sqlalchemy.sql import func


class Bin(db.Model):
    __tablename__ = 'bin'
    id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Float)
    grader = db.Column(db.Integer)
    fish_weight = db.Column(db.Float)
    bin = db.Column(db.Integer)
    bin_name = db.Column(db.String(64))
    count = db.Column(db.Integer, default=0)
    datetime = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'weight': self.weight,
            'grader': self.grader,
            'fish_weight': self.fish_weight,
            'bin': self.bin,
            'bin_name': self.bin_name,
            'count': self.count,
            'datetime': self.datetime.isoformat()
        }

