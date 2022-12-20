from flask import jsonify, json
from flask_restx import Resource, fields, reqparse
from app.module.logic import Logic
from app.flask_api.http import HttpStatus
from app import api
from app.db.database import SessionLocal

logic = Logic(SessionLocal)


@api.route('/api/v1/model_classes')
class model_classes(Resource):
    @staticmethod
    def get():
        try:
            return get_common_response(logic.get_model_classes())
        except FileNotFoundError as e:
            print(e)
            return get_error_response(e, HttpStatus.NOT_FOUND)
        except Exception as e:
            return get_error_response(e)


delete_parser = reqparse.RequestParser()
delete_parser.add_argument('model_id', help='Id of model')

delete_fields = api.model('Delete body', {
    'model_id': fields.Integer(description='Id of model', default=1),
})


@api.route('/api/v1/models')
class models(Resource):
    @staticmethod
    def get():
        try:
            return get_common_response(logic.get_models())
        except FileNotFoundError as e:
            print(e)
            return get_error_response(e, HttpStatus.NOT_FOUND)
        except Exception as e:
            return get_error_response(e)

    @api.doc(body=delete_fields)
    def delete(self):
        try:
            args = delete_parser.parse_args(strict=True)
            logic.delete_model(args.model_id)
            return get_common_response([])
        except FileNotFoundError as e:
            print(e)
            return get_error_response(e, HttpStatus.NOT_FOUND)
        except Exception as e:
            return get_error_response(e)


fit_parser = reqparse.RequestParser()
fit_parser.add_argument('model_type', help='Name of model type')
fit_parser.add_argument('params', help='Model params')
fit_parser.add_argument('x', help='X data with out target', action='append')
fit_parser.add_argument('y', help='Y data, only target', action='append')

fit_fields = api.model('Fit body', {
    'model_type': fields.String(enum=['Ridge', 'RandomForestRegressor'], description='Name of model type'),
    'params': fields.Raw(default={}, description='Model params'),
    'x': fields.List(fields.List(fields.Float), default=[[1, 2, 3], [2, 2, 3], [3, 2, 1]]),
    'y': fields.List(fields.Float, default=[1, 2, 3]),
})


@api.route('/api/v1/models/fit')
class fit(Resource):
    @api.doc(body=fit_fields)
    def post(self):
        try:
            args = fit_parser.parse_args(strict=True)
            params = json.loads(args.params.replace("'", "\""))
            model_name = logic.fit_model(args.model_type, params, fix_list(args.x), fix_list(args.y))
            return get_common_response(model_name, HttpStatus.CREATED)
        except FileNotFoundError as e:
            print(e)
            return get_error_response(e, HttpStatus.NOT_FOUND)
        except Exception as e:
            print(e)
            return get_error_response(e)


predict_parser = reqparse.RequestParser()
predict_parser.add_argument('model_id', help='Id of model')
predict_parser.add_argument('x', help='X data with out target', action='append')

predict_fields = api.model('Predict body', {
    'model_id': fields.Integer(description='Id of model', default=1),
    'x': fields.List(fields.List(fields.Float), default=[[1, 2, 3], [2, 2, 3], [3, 2, 1]],
                     description='X data with out target'),
})


@api.route('/api/v1/models/predict')
class predict(Resource):
    @api.doc(body=predict_fields)
    def post(self):
        try:
            args = predict_parser.parse_args(strict=True)
            y_pred = logic.predict_model(args.model_id, fix_list(args.x))
            return get_common_response(y_pred)
        except FileNotFoundError as e:
            print(e)
            return get_error_response(e, HttpStatus.NOT_FOUND)
        except Exception as e:
            return get_error_response(e)


def get_error_response(exception, status_code=HttpStatus.BAD_REQUEST):
    construct = {
        'error': exception.__str__().replace("'", "\""),
        'success': False,
        'result': []
    }
    response = jsonify(construct)
    response.status_code = status_code
    return response


def get_common_response(result, status_code=HttpStatus.OK):
    construct = {
        'error': [],
        'success': True,
        'result': result
    }
    response = jsonify(construct)
    response.status_code = status_code
    return response


def fix_list(arr):
    return [eval(item) for item in arr]
