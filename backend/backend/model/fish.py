from backend.model import db
from sqlalchemy.sql import func


class Fish(db.Model):
    __tablename__ = 'fish'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    weight = db.Column(db.Float)
    bin = db.Column(db.Integer)
    product = db.Column(db.Integer)
    ip = db.Column(db.Integer)
    datetime = db.Column(db.DateTime, default=func.now(), index=True)

    def to_dict(self):
        return {
            'id': self.id,
	        'weight': self.weight,
            'bin': self.bin,
            'product': self.product,
            'ip': self.ip,
            'datetime': self.datetime.isoformat()
        }