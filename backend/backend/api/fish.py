from . import api
from backend.model import Fish, Bin, db
from sqlalchemy import text
from datetime import datetime

@api.get('/last_fish')
@api.get('/last_fish/<int:n>')
def last_fish(n=None):
    if n is None:
        n = 10
    fishes = db.session.query(Fish).order_by(Fish.id.desc()).limit(n).all()
    return {'fish': [fish.to_dict() for fish in fishes]}


@api.get('/binstats')
@api.get('/binstats/<int:resetbin>')
def bin_stats(resetbin=None):
    if resetbin is not None:
        query = "UPDATE bin SET weight=0, count=0" if resetbin == 0 else f"UPDATE bin SET weight=0, count=0 WHERE bin_name='[12.38] DualGrader Bin {resetbin}'"
        db.session.execute(text(query), {})
        db.session.commit()
    bins = db.session.query(Bin).order_by(Bin.id).all()
    return {'bins': [bin.to_dict() for bin in bins]}


@api.get('/fish/<int:last_id>')
def fish(last_id=0):
    query = text("SELECT * FROM fish WHERE id > :last_id")
    results = db.session.execute(query, {"last_id": last_id}).fetchall()
    result_list = [
        [row[0], row[1], row[2], row[3], row[4], int(row[5].timestamp())] if isinstance(row[5], datetime) else row[5]
        for row in results
    ]
    return {'fish': result_list}, 200
