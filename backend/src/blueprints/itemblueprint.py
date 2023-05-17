from flask import Blueprint, jsonify, abort, request
from flask_cors import cross_origin

from pymongo.errors import WriteError
import json

from src.controllers.controller import Controller
from src.util.dao import getDao
controller = Controller(dao=getDao(collection_name='item'))

# instantiate the flask blueprint
item_blueprint = Blueprint('item_blueprint', __name__)

@item_blueprint.route('/create', methods=['POST'])
@cross_origin()
def create():
    try:
        data = request.form.to_dict(flat=False)

        # convert all non-array fields back to simple values
        for key in data:
            if isinstance(data[key], list):
                data[key] = data[key][0]
        data['quantity'] = float(data['quantity'])

        item = controller.create(data)
        
        return jsonify(item), 200
    except WriteError as e:
        abort(400, 'Invalid input data')
    except Exception as e:
        print(f'{e.__class__.__name__}: {e}')
        abort(500, 'Unknown server error')

@item_blueprint.route('/all', methods=['GET'])
@cross_origin()
def get_all():
    try:
        items = controller.get_all()
        return jsonify(items), 200
    except WriteError as e:
        abort(400, 'Invalid input data')
    except Exception as e:
        print(f'{e.__class__.__name__}: {e}')
        abort(500, 'Unknown server error')

@item_blueprint.route('/byid/<id>', methods=['GET', 'PUT', 'DELETE'])
@cross_origin()
def get(id):
    try:
        if request.method == 'GET':
            # obtain an item that fits a specific id
            task = controller.get(id)
            return jsonify(task), 200
        elif request.method == 'PUT':
            # update an item with a specific id 
            data = request.form.to_dict(flat=True)['data']
            data = json.loads(data.replace("'", "\""))

            task = controller.update(id, data)
            return jsonify(task), 200
        elif request.method == 'DELETE':
            # delete an item with a specific id
            result = controller.delete(id=id)
            return jsonify({"success": result}), 200
    except Exception as e:
        print(f'{e.__class__.__name__}: {e}')
        abort(500, 'Unknown server error')