from flask import abort, request
from . import api, auth
from backend.model import Pallet, db


@api.get('/pallets/<int:year>/<int:trip>')
def pallets_list(year, trip):
    # Trip is optional
    query = Pallet.query.filter(Pallet.year == year)

    if trip is not None:
        query = query.filter(Pallet.trip == trip)
    pallets = query.order_by(Pallet.id).all()
    return {'pallets': [pallet.to_dict() for pallet in pallets]}


@api.post('/pallets')
def pallets_add():
    json = request.json

    # Validate the required fields
    required_fields = ['datetime', 'year', 'trip', 'label', 'hold', 'space', 'layer']
    for field in required_fields:
        if field not in json:
            abort(400, f'expected_{field}')

    new_pallet = Pallet(
        datetime=json['datetime'],
	year=json['year'],
        trip=json['trip'],
        label=json['label'],
        hold=json['hold'],
        space=json['space'],
        layer=json['layer']
    )

    db.session.add(new_pallet)
    db.session.commit()

    return {"id":new_pallet.id}, 201

@api.delete('/pallets/<int:id>')
#@auth.login_required
def pallets_delete(id):
    pallet = db.session.get(Pallet, id)

    if not pallet:
        abort(404, 'invalid_pallet_data')

    db.session.delete(pallet)
    db.session.commit()

    return '', 204
