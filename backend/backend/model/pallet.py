from sqlalchemy import Column, Integer, String, Text
from backend.model import db

class Pallet(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    datetime = Column(DateTime, nullable=False)
    trip = Column(Integer)
    label = Column(Integer)
    hold = Column(Integer)
    space = Column(Integer)
    layer = Column(Integer)

    def to_dict(self):
        return {
            'id': self.id,
            'datetime': self.datetime,
            'trip': self.trip,
            'label': self.label,
            'hold': self.hold,
            'space': self.space,
            'layer': self.layer
        }
