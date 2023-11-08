from sqlalchemy import Column, Integer, String, Text, DateTime
from backend.model import db
from sqlalchemy import UniqueConstraint
from sqlalchemy.ext.hybrid import hybrid_property

class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    year = db.Column(db.Integer, nullable=False)
    trip = db.Column(db.Integer, nullable=False)
    started = db.Column(db.DateTime, nullable=True)
    finished = db.Column(db.DateTime, nullable=True)

    __table_args__ = (UniqueConstraint('year', 'trip'),)

    @hybrid_property
    def active(self):
        # Trip is active if started is set but finished is not
        return self.started is not None and self.finished is None

    @active.expression
    def active(cls):
        # Use SQLAlchemy's and_ for combining conditions
        return and_(cls.started is not None, cls.finished is None)

    def to_dict(self):
        return {
            'id': self.id,
	    'year': self.year,
            'trip': self.trip,
            'started': self.started.isoformat() if self.started else None,
            'finished': self.finished.isoformat() if self.finished else None,
            'active': self.active,
        }
