from flask_restful import Api, Resource, reqparse
from helpers import check_for_token, get_jwt_decode_data, generate_password_hash, check_password_hash

class AccountApiHandler(Resource):
    @check_for_token
    def get(self):
        return {
            'resultStatus': 'SUCCESS',
            'message': "Account Api Handler"
        }

    @check_for_token
    def post(self):
        print(self)
        parser = reqparse.RequestParser()
        parser.add_argument('type', type=str)
        parser.add_argument('message', type=str)

        args = parser.parse_args()

        print(args)
        # note, the post req from anox-fe needs to match the strings here (e.g. 'type and 'message')

        request_type = args['type']
        request_json = args['message']
        # ret_status, ret_msg = ReturnData(request_type, request_json)
        # currently just returning the req straight
        ret_status = request_type
        ret_msg = request_json

        if ret_msg:
            message = "Your Message Requested: {}".format(ret_msg)
        else:
            message = "No Msg"

        final_ret = {"status": "Success", "message": message}

        return final_ret
