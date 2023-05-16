# coding=utf-8
import os, json
from dotenv import dotenv_values

from flask import Flask, jsonify
from flask_cors import CORS, cross_origin

# import the blueprints which handle the incoming data
from src.blueprints.itemblueprint import item_blueprint
from src.blueprints.receipeblueprint import receipe_blueprint
#from src.util.dao import getDao

# create the Flask application
app = Flask('chef-backend')

# configure CORS for cross-origin resource sharing (between the frontend and backend)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# register blueprints
app.register_blueprint(blueprint=item_blueprint, url_prefix='/items')
app.register_blueprint(blueprint=receipe_blueprint, url_prefix='/receipes')

@app.route('/')
@cross_origin()
def ping():
    """Heartbeat method to check if the server is running and which version is currently active.
    
    returns: 
      version -- version string of the current backend version"""
    VERSION = dotenv_values('.env').get('VERSION')
    return jsonify({'version': VERSION}), 200

# simple population method that adds initial data to the database
@app.route('/populate', methods=['POST'])
@cross_origin()
def populate():

    return jsonify({"success": True}), 200

if __name__ == '__main__':
    # print all available REST endpoints
    print(app.url_map)

    # if a specific FLASK_BIND_IP is given, run the app on that URL
    if (os.environ.get('FLASK_BIND_IP')):
        app.run(host=os.environ.get('FLASK_BIND_IP'))
    else:
        app.run()
    