from typing import Dict
from sqlalchemy import insert
from models import *
from helpers import sqlalchemy_obj_to_dict, hash_password
from flask import session as flask_session


def user_exists(session, email: str) -> Dict:

    user = session.query(User).filter(User.email == email).one_or_none()

    if user is not None:
        return True
    else:
        return False


def validate_user(session, email: str, password: str) -> bool:

    user = session.query(User).filter(User.email == email).one_or_none()

    if user is not None:
        user = sqlalchemy_obj_to_dict(user)
        user_password = user["password"]
        if user_password == hash_password(password=password):
            return {"success": "User valid"}
        else:
            return {"error": "Invalid Credentials"}

    else:
        return {"error": "User doesn't exist"}


def get_user(session, email: str):
    user = session.query(User).filter(User.email == email).one_or_none()

    if user is not None:
        return sqlalchemy_obj_to_dict(user)
    else:
        return {"error": "User doesn't exist"}


def create_user(session, username: str, email: str, password: str) -> Dict:
    """
    Create user if it it doesn't
    exist
    """

    user_exist = user_exists(session=session, email=email)

    if not user_exist:
        statement = insert(User).values(
            username=username, email=email, password=hash_password(password=password)
        )

        session.execute(statement=statement)
        session.commit()
        session.close()
    else:
        return {"error": "User already exists"}

    return {"success": "User created"}


def log_user_in(session, email, password):
    response = validate_user(session=session, email=email, password=password)
    if response.get("success"):
        user = get_user(session=session, email=email)
        flask_session["username"] = user["username"]
        flask_session["id"] = user["id"]
        flask_session["user_id"] = f"{user['username']}_{user['id']}"
        return response, 200
    else:
        return response, 401


def user_logged_in():
    username = flask_session.get("username")
    id = flask_session.get("id")
    user_id = flask_session.get("user_id")

    if not all([username, id, user_id]):
        return False
    else:
        if f"{username}_{id}" == user_id:
            return True
    return False


def clear_cache():
    try:
        for key in ["username", "id", "user_id"]:
            flask_session.pop(key)
        return True
    except:
        return False
