from flask import Flask, send_from_directory, request
from flask_restful import Api
from flask_cors import CORS
from api.RegisterApiHandler import RegisterApiHandler
from api.LoginApiHandler import LoginApiHandler
from api.AccountApiHandler import AccountApiHandler
from api.DashboardApiHandler import DashboardApiHandler
from api.ResetPasswordApiHandler import ResetPasswordApiHandler
from helpers import PathUtil
from db import db_init, cache


app = Flask(__name__, static_url_path='', static_folder='anox-fe/public')
app.config["SERVER_SECRET"] = PathUtil.get_server_secret_bytes()
CORS(app)
api = Api(app)
db_init()

def get_jwt_decode_data():
    token = request.headers.get('Authorization')
    session_data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
    return session_data


@app.route("/", defaults={'path': ''})
def serve(path):
    return send_from_directory(app.static_folder, 'index.html')


api.add_resource(RegisterApiHandler, '/flask/v1/register')
api.add_resource(LoginApiHandler, '/flask/v1/login')
api.add_resource(AccountApiHandler, '/flask/v1/account')
api.add_resource(DashboardApiHandler, '/flask/v1/dashboard')
api.add_resource(ResetPasswordApiHandler, '/flask/v1/reset-password')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
