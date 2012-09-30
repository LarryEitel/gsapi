# -*- coding: utf-8 -*-
from flask import request
from flask_rest import RESTResource, need_auth
from gsapi.extensions import RegexConverter, Blueprint

import gsapi.models as models

api = Blueprint("api", __name__, url_prefix="/api")
api.add_app_url_map_converter(RegexConverter, 'regex')

from gsapi.views import generic


##################### GET
@api.route( '/<regex("[\w]*[Ss]"):class_name>/<regex("[a-f0-9]{24}"):id>', methods=['GET'])
@api.route( '/<regex("[\w]*[Ss]"):class_name>?', methods=['GET'])
@api.route( '/<regex("[\w]*[Ss]"):class_name>', methods=['GET'])
def get(class_name, id=None):
    # if not class_name in Config.DOMAIN.keys():
    #     abort(404)
    response = generic.get(class_name, id)
    return response

##################### PUT
@api.route( '/<regex("[\w]*[Ss]"):class_name>', methods=['PUT','PATCH'])
def put(class_name):
    if not class_name in Config.DOMAIN.keys():
        abort(404)
    response = generic.put(class_name)
    return response

##################### POST
@api.route( '/<regex("[\w]*[Ss]"):class_name>', methods=['POST'])
def post(class_name):
    if not class_name in Config.DOMAIN.keys():
        abort(404)
    response = generic.post(class_name)
    return response

