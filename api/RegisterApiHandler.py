import json
import base64
import action_service
from flask import make_response
from flask_restful import Resource, reqparse
from helpers import get_csrf_token, check_csrf_token


class RegisterApiHandler(Resource):

    @staticmethod
    def validate(payload):
        payload_decoded = json.loads(base64.urlsafe_b64decode(payload).decode("utf-8"))
        return action_service.check_user_for_register(data=payload_decoded)

    def get(self):
        response = make_response({
            'resultStatus': 'SUCCESS',
            'csrfToken': get_csrf_token()
        }, 200)
        return response

    @check_csrf_token
    def post(self):
        print(self)
        parser = reqparse.RequestParser()
        parser.add_argument('payload', type=str)
        args = parser.parse_args()
        print(args)
        request_json = args['payload']
        ret_state, ret_obj = self.validate(payload=request_json)

        if ret_state == 200:
            message = "user registered successfully"
            resp = make_response({"response": message}, 201)
            resp.headers["Authorization"] = ret_obj.get("token")
            return resp
        elif ret_state == 401:
            message = ret_obj.get("error")
            return make_response({"response": message}, 401)
        else:
            message = ret_obj.get("error")
            return make_response({"response": message}, 500)
