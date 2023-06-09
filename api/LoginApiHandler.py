import json
import pickle
import base64
import action_service
from flask import make_response
from flask_restful import Api, Resource, reqparse
from helpers import decode_jwt


class LoginApiHandler(Resource):

    @staticmethod
    def validate(payload):
        payload_decoded = json.loads(base64.urlsafe_b64decode(payload).decode("utf-8"))
        return action_service.check_user_for_login(data=payload_decoded)

    def post(self):
        print(self)
        parser = reqparse.RequestParser()
        parser.add_argument('payload', type=str)
        args = parser.parse_args()
        print(args)
        request_json = args['payload']
        ret_state, ret_obj = self.validate(payload=request_json)
        token = None
        if ret_state == 200:
            message = "user authenticated"
            resp = make_response({"response": message})
            resp.status_code = 200
            resp.set_cookie("__anoxsys_cookie__", ret_obj.get("token"))
            resp.headers["Authorization"] = ret_obj.get("token")
            return resp
        elif ret_state == 404:
            message = ret_obj.get("error")
            resp = make_response({"response": message})
            resp.status_code = 404
            return resp
        else:
            message = ret_obj.get("error")
            resp = make_response({"response": message})
            resp.status_code = 401
            return resp
