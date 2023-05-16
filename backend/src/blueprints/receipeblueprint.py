from flask import Blueprint, jsonify, abort, request
from flask_cors import cross_origin

from src.controllers.receipecontroller import ReceipeController
from src.util.dao import getDao
controller = ReceipeController(items_dao=getDao(collection_name='item'))

from src.static.diets import Diet

# instantiate the flask blueprint
receipe_blueprint = Blueprint('receipe_blueprint', __name__)

@receipe_blueprint.route('/', methods=['GET'])
@cross_origin()
def create():
    try:
        data = request.form.to_dict(flat=False)

        # convert all non-array fields back to simple values
        for key in data:
            if isinstance(data[key], list):
                data[key] = data[key][0]

        #item = controller.create(data)
        
        receipe = controller.get_receipe(diet=Diet.NORMAL, take_best=True)

        return jsonify(receipe), 200
    
    except Exception as e:
        print(f'{e.__class__.__name__}: {e}')
        abort(500, 'Unknown server error')