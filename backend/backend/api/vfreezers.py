from flask import request
from . import api
from backend.model import Storage, db
from datetime import datetime


@api.get('/storage')
@api.get('/storage/<int:storage_id>')
def storage_list(storage_id=None):
    if storage_id:
        storage = Storage.query.get(storage_id)
        if storage:
            return {'storage': [storage.to_dict()]}
        return {'message': 'Storage not found'}
    else:
        storages = Storage.query.all()
        return {'storage': [storage.to_dict() for storage in storages]}


@api.post('/storage')
def storage_add():
    data = request.json
    existing_storage = Storage.query.filter_by(freezer=data['freezer'], space=data['space']).first()
    if existing_storage:
        existing_storage.product = data['product']
        existing_storage.tow = data['tow']
        existing_storage.datetime = datetime.strptime(data['datetime'], "%Y-%m-%dT%H:%M:%S.%f")
        db.session.commit()
        return {'message': 'Storage updated successfully'}, 200
    else:
        try:
            new_storage = Storage(freezer=data['freezer'],
                                  space=data['space'],
                                  tow=data['tow'],
                                  product=data['product'],
                                  datetime=datetime.strptime(data['datetime'], "%Y-%m-%dT%H:%M:%S.%f"))
            db.session.add(new_storage)
            db.session.commit()
            return {'id': new_storage.id}, 201
        except IntegrityError as e:
            db.session.rollback()  # Rollback the session to a clean state
            return {'message': 'Already existing'}, 420
