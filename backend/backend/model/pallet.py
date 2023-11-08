from sqlalchemy import Column, Integer, String, Text, DateTime
from backend.model import db

class Pallet(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    datetime = Column(DateTime, nullable=False)
    year = Column(Integer, nullable=False)
    trip = Column(Integer, nullable=False)
    label = Column(Integer, nullable=False)
    hold = Column(Integer, nullable=False)
    space = Column(Integer, nullable=False)
    layer = Column(Integer, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'datetime': self.datetime.isoformat(),
	    'year': self.year,
            'trip': self.trip,
            'hold': self.hold,
            'space': self.space,
            'layer': self.layer,
            'label': self.label
        }
