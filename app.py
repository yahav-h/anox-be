from flask import Flask, send_from_directory
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
from api.HelloApiHandler import HelloApiHandler
from api.LoginApiHandler import LoginApiHandler
from api.AccountApiHandler import AccountApiHandler
from api.DashboardApiHandler import DashboardApiHandler


app = Flask(__name__, static_url_path='', static_folder='frontend/build')
CORS(app)
api = Api(app)


@app.route("/", defaults={'path': ''})
def serve(path):
    return send_from_directory(app.static_folder, 'index.html')


api.add_resource(HelloApiHandler, '/flask/v1/hello')
api.add_resource(LoginApiHandler, '/flask/v1/login')
api.add_resource(AccountApiHandler, '/flask/v1/account')
api.add_resource(DashboardApiHandler, '/flask/v1/dashboard')

