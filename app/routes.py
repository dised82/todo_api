from flask import Blueprint, jsonify, request
from http import HTTPStatus
from app import db

log = Blueprint('routes', __name__)

bp = Blueprint('routes', __name__)

commands = {
    "signup":{
        "type" : 'GET',
        "verb" : 'link/signup/<type:data>'
        }
}
# here lies all the connection commands/routes 
@log.route("/", methods=['POST'])
@log.route("/login", methods=['POST'])
def login():
    data = request.get_json() 
    return jsonify(data), HTTPStatus.ACCEPTED
# here lies all the main routes
@bp.route("/")
@bp.route("/index")
def index():
    return jsonify(commands), HTTPStatus.OK



