import base64
import json
import datetime
import pickle
import sys
import uuid
import hashlib
import jwt
from platform import platform
from os.path import join, dirname, abspath
from flask import session, request, make_response
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import time
import imaplib, smtplib
from email.mime.text import MIMEText
import email.message


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class PathUtil(object, metaclass=Singleton):
    @staticmethod
    def get_mailer_info():
        with open(PathUtil.resource_path("config.json"), "r") as cfg:
            return json.load(cfg).get("mailer")

    @staticmethod
    def get_server_secret_bytes():
        with open(PathUtil.resource_path("config.json"), "rb") as cfg:
            meta = json.load(cfg).get("server")
            return getattr(hashlib, meta["algo1"])(
                getattr(hashlib, meta["algo2"])(
                    meta["salt"].encode(),
                    salt=uuid.uuid5(
                        uuid.NAMESPACE_X500,
                        getattr(getattr(getattr(__import__(meta["f1"]), meta["f2"]), meta["f3"])(
                            meta["a"], meta["b"], meta["c"]
                        ), meta["f4"])()
                    ).bytes, n=meta["c"]+1, p=meta["a"]-1, r=meta["b"]+11
                )
            ).hexdigest()

    @staticmethod
    def resource_path(relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            base_path = getattr(sys, '_MEIPASS', dirname(abspath(__file__)))
        else:
            base_path = dirname(abspath(__file__))
        return join(base_path, relative_path)

    @staticmethod
    def get_database_path():
        if platform().lower().startswith('win'):
            final_path = PathUtil.resource_path('records.db')
            database_path = r'sqlite:///%s' % final_path
        else:
            final_path = PathUtil.resource_path('records.db')
            database_path = 'sqlite:////%s' % final_path
        return database_path

    @staticmethod
    def get_logs_path():
        if platform().lower().startswith('win'):
            final_path = PathUtil.resource_path(r'runtime_%s.log' % datetime.date.today())
            logs_dir = r'%s' % final_path
        else:
            final_path = PathUtil.resource_path('runtime_%s.log' % datetime.date.today())
            logs_dir = '%s' % final_path
        return logs_dir

def decode_jwt(token):
    _jwt = jwt.decode(token, PathUtil.get_server_secret_bytes().encode(), algorithms=['HS256'])
    return _jwt

def get_jwt_decode_data():
    token = request.headers.get('Authorization')
    session_data = decode_jwt(token)
    return session_data


def get_csrf_token():
    return base64.urlsafe_b64encode(pickle.dumps({
        'ts': datetime.datetime.now(),
        'td': datetime.timedelta(0, 0, 0, 0, 5, 0, 0)
    })).decode()

def check_csrf_token(func, header="X-CSRF"):
    @wraps(func)
    def wrapped(*args, **kwargs):
        token = request.headers.get(header)
        if not token:
            return make_response({'message': 'missing csrf token'}, 403)
        try:
            csrf_fp = pickle.loads(base64.urlsafe_b64decode(token))
            if not((csrf_fp.get('ts') + csrf_fp.get('td')).timestamp() <= datetime.datetime.now().timestamp()):
                pass
            else:
                raise
        except:
            return make_response({'message': 'invalid csrf token'}, 403)
        return func(*args, **kwargs)
    return wrapped

def check_for_token(func, header='Authorization'):
    @wraps(func)
    def wrapped(*args, **kwargs):
        token = request.headers.get(header)
        if not token:
            session['logged_in'] = False
            return make_response({'message': 'Missing token'}, 403)
        try:
            data = jwt.decode(token, PathUtil.get_server_secret_bytes(), algorithms=['HS256'])
            assert 'sub' in data
        except:
            session['logged_in'] = False
            return make_response({'message': 'Invalid token'}, 403)

        return func(*args, **kwargs)

    return wrapped

class Mailer:
    def __init__(self):
        info = PathUtil.get_mailer_info()
        self.sender = info.get("sender")
        self.password = info.get("password")
        self.host = info.get("host")
        self.port = info.get("port")
        self.connect_to_gmail()

    def connect_to_gmail(self):
        self.imap = smtplib.SMTP(self.host)
        self.imap.set_debuglevel(True)
        self.imap.ehlo('test')
        self.imap.starttls()
        at = 'user=%s\1auth=Bearer %s\1\1' % (self.sender, self.password)
        self.imap.docmd('AUTH', 'XOAUTH2 ' + base64.b64encode(at.encode()).decode())
        return self.imap

    def send_email(self, subject, body, to_email):
        msg = email.message.Message()
        msg['From'] = self.sender
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.set_payload(body)
        self.imap.sendmail(self.sender, to_email, msg.as_string())


mailer = Mailer()

