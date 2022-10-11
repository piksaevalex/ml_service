from flask import jsonify, json
from flask_restx import Resource
from app import api
from .models import fit_model, predict_model, delete_model, Model_classes, models_store
from .const import HttpStatus
from flask_restx import reqparse


@api.route('/api/v1/model_classes')
class model_classes(Resource):
    @staticmethod
    def get():
        try:
            return get_common_response(Model_classes)
        except Exception as e:
            return get_error_response(e)


fit_parser = reqparse.RequestParser()
fit_parser.add_argument('model_type', help='Name of model type')
fit_parser.add_argument('params', help='Model params')
fit_parser.add_argument('x', help='X data with out target', action='append')
fit_parser.add_argument('y', help='Y data, only target', action='append')

delete_parser = reqparse.RequestParser()
delete_parser.add_argument('model_name', help='Name of model')


@api.route('/api/v1/models')
class models(Resource):
    @staticmethod
    def get():
        try:
            return get_common_response(list(models_store.keys()))
        except Exception as e:
            return get_error_response(e)

    @api.expect(fit_parser)
    def post(self):
        try:
            args = fit_parser.parse_args()
            params = json.loads(args.params.replace("'", "\""))
            model_name = fit_model(args.model_type, params, fix_list(args.x), fix_list(args.y))
            return get_common_response(model_name)
        except Exception as e:
            return get_error_response(e)

    @api.expect(delete_parser)
    def delete(self):
        try:
            args = delete_parser.parse_args()
            delete_model(args.model_name)
            return get_common_response([])
        except Exception as e:
            return get_error_response(e)


predict_parser = reqparse.RequestParser()
predict_parser.add_argument('model_name', help='Name of model')
predict_parser.add_argument('x', help='X data with out target', action='append')


@api.route('/api/v1/models/predict')
class predict(Resource):
    @api.expect(predict_parser)
    def post(self):
        try:
            args = predict_parser.parse_args()
            y_pred = predict_model(args.model_name, fix_list(args.x))
            return get_common_response(y_pred)
        except Exception as e:
            return get_error_response(e)


def get_error_response(exception):
    construct = {
        'error': exception.__str__(),
        'success': False,
        'result': []
    }
    response = jsonify(construct)
    response.status_code = HttpStatus.OK
    return response


def get_common_response(result):
    construct = {
        'error': [],
        'success': True,
        'result': result
    }
    response = jsonify(construct)
    response.status_code = HttpStatus.OK
    return response


def fix_list(arr):
    return [eval(item) for item in arr]
