from flask import jsonify, request
from . import api
from ..models import TimeLine
from .utils import get_attribute_values as get_values
from .utils import get_timeline_data


@api.route('/info', methods=['GET'])
def info():

    attr_list = ['stars', 'source', 'brand', 'asin']

    result_response = {attr: get_values(getattr(TimeLine, attr))
                       for attr in attr_list}

    return jsonify(result_response)


@api.route('/timeline', methods=['GET'])
def timeline():

    params = request.args
    if not any(params):
        return jsonify({'massage': 'Missing params'})

    data = get_timeline_data(params)
    response = {'timeline': data}

    return jsonify(response)
