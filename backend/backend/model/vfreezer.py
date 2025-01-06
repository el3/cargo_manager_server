from backend.model import db
from sqlalchemy.sql import func
from sqlalchemy import UniqueConstraint


class Storage(db.Model):
    __tablename__ = 'storage'

    id = db.Column(db.Integer, primary_key=True)
    freezer = db.Column(db.Integer)
    space = db.Column(db.Integer)
    tow = db.Column(db.Integer)
    product = db.Column(db.Integer)
    datetime = db.Column(db.DateTime, default=func.now())

    # Define the unique constraint for freezer and space
    __table_args__ = (UniqueConstraint('freezer', 'space', name='unique_freezer_space'),)

    def to_dict(self):
        return {
            'id': self.id,
	        'freezer': self.freezer,
            'space': self.space,
            'tow': self.tow,
            'product': self.product,
            'datetime': self.datetime.isoformat()
        }
