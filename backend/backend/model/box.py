from backend.model import db
from sqlalchemy.sql import func


class Box(db.Model):
    __tablename__ = 'box'
    id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Float)
    bin = db.Column(db.String(64))
    product = db.Column(db.Integer)
    datetime = db.Column(db.DateTime, default=func.now())

