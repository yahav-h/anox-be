from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, String, Boolean, ForeignKey, Integer
from helpers import PathUtil, generate_password_hash
import datetime
import jwt

cache = {}
db_path_string = PathUtil.get_database_path()
engine = create_engine(db_path_string)
db_session = scoped_session(
    sessionmaker(
        autocommit=False, autoflush=False, bind=engine
    )
)
Base = declarative_base()
Base.query = db_session.query_property()


def db_init():
    Base.metadata.create_all(bind=engine)

@contextmanager
def get_session():
    global db_session
    try:
        yield db_session
    except:
        db_session.rollback()
    finally:
        db_session.commit()


class webusers(Base):
    __tablename__ = "webusers"
    id = Column(Integer(), primary_key=True, autoincrement=True, nullable=False)
    email = Column(String(32), unique=True, nullable=False)
    passwd_hash = Column(String(64), unique=False, nullable=False)
    created_time = Column(DateTime(), nullable=False)
    modified_time = Column(DateTime(), nullable=False)
    token = Column(String(256), unique=True, nullable=True)
    def __repr__(self): return f"<webuser {self.id=} {self.email=}>"

    def __init__(self, email=None, pwd=None):
        self.email = email
        self.passwd_hash = generate_password_hash(pwd, method="sha256")
        self.created_time = datetime.datetime.now()
        self.modified_time = datetime.datetime.now()

    @staticmethod
    def encode_auth_token(server_key, user_id, seconds=600):
        payload = {
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=seconds),
            "iat": datetime.datetime.utcnow(),
            "sub": user_id
        }
        return jwt.encode(
            payload=payload,
            key=server_key,
            algorithm="HS256"
        )
