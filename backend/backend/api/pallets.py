from flask import abort, request
from . import api, auth
from backend.model import Pallet, db

@api.get('/pallets')
def pallets_list():
    return {'pallets': [
        pallet.to_dict()
        for pallet in Pallet.query.order_by(Pallet.id)
    ]}

@api.post('/pallets')
def pallets_add():
    json = request.json

    # Validate the required fields
    required_fields = ['datetime', 'trip', 'label', 'hold', 'space', 'layer']
    for field in required_fields:
        if field not in json:
            abort(400, f'expected_{field}')

    new_pallet = Pallet(
        datetime=json['datetime'],
        trip=json['trip'],
        label=json['label'],
        hold=json['hold'],
        space=json['space'],
        layer=json['layer']
    )

    db.session.add(new_pallet)
    db.session.commit()

    return '', 201

@api.delete('/pallets/<int:id>')
@auth.login_required
def pallets_delete(id):
    pallet = db.session.get(Pallet, id)

    if not pallet:
        abort(404, 'invalid_pallet_id')

    db.session.delete(pallet)
    db.session.commit()

    return '', 204
