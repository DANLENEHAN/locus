from sqlalchemy import inspect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import hashlib


def sqlalchemy_obj_to_dict(obj: any) -> dict:
    return {x.key: getattr(obj, x.key) for x in inspect(obj).mapper.column_attrs}


def get_session():
    mysql_password = os.environ["MYSQL_PWD"]
    engine = create_engine(
        f"mysql+pymysql://root:{mysql_password}@localhost:3306/Train"
    )
    Session = sessionmaker(engine)
    return Session()


def hash_password(password: str):
    return hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=password.encode("utf-8"),
        salt=os.environ["SALT"].encode("utf-8"),
        iterations=100000,
        dklen=20,
    ).hex()
