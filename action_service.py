from db import get_session, webusers
from helpers import check_password_hash, PathUtil, mailer


def __send_reset_password_mail(email):
    msg = f"Reset Email Request for Account {email}\nHello,\n"\
           "We've received you request to reset your account password!\n"\
           "If you've not permitted such action , please contact use via anoxsys.security@gmail.com\n"\
           "Click to reset : http://192.168.1.23:3000/flask/v1/email-reset"
    try:
        mailer.send_email(subject="Reset Passwrd", body=msg, to_email=email)
        return True
    except:
        return False


def check_user_for_login(data):
    record = webusers.query.filter_by(email=data["email"]).first()
    if not record:
        return 404, {"error": "not found"}
    same = check_password_hash(record.passwd_hash, data["password"])
    if not same:
        return 401, {"error": "username / password are wrong"}
    new_token = record.encode_auth_token(server_key=PathUtil.get_server_secret_bytes(), user_id=record.id)
    record.token = new_token
    with get_session() as Session:
        Session.add(record)
    return 200, {"token": new_token}


def check_user_for_register(data):
    record = webusers.query.filter_by(email=data["email"]).first()
    if record:
        return 401, {"error": "already exists"}
    record = webusers(email=data["email"], pwd=data["password"])
    same = check_password_hash(record.passwd_hash, data["password"])
    if not same:
        return 500, {"error": "registration failed, bad password hashing"}
    new_token = record.encode_auth_token(server_key=PathUtil.get_server_secret_bytes(), user_id=record.id)
    record.token = new_token
    with get_session() as Session:
        Session.add(record)
    return 201, {"token": new_token}

def check_user_for_reset_password(data):
    record = webusers.query.filter_by(email=data["email"]).first()
    if not record:
        return 401, {"error": "already exists"}
    if not __send_reset_password_mail(data["email"]):
        return 500, {"error": "could not send reset password to email"}
    return 200, {"message": f"reset password send to {data['email']=}"}
