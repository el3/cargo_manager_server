from flask import abort, request
from . import api, auth
from backend.model import Pallet, Trip, db

@api.get('/trips/<int:year>/')
@api.get('/trips/<int:year>/<int:trip>')
def trips_list(year, trip=None):
    # Trip is optional
    query = Trip.query.filter(Trip.year == year)

    if trip is not None:
        query = query.filter(Trip.trip == trip)
    trips = query.order_by(Trip.id).all()
    return {'trips': [trip.to_dict() for trip in trips]}


@api.post('/trips')
def trips_add():
    json = request.json

    # Validate the required fields
    required_fields = ['year', 'trip']
    for field in required_fields:
        if field not in json:
            abort(400, f'expected_{field}')

    new_trip = Trip(
        year=json['year'],
        trip=json['trip']
    )

    db.session.add(new_trip)
    db.session.commit()

    return {"id":new_trip.id}, 201
