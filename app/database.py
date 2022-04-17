from typing import Dict
import uuid
from sqlalchemy import insert
from sqlalchemy.orm import sessionmaker
from models import *
from helpers import sqlalchemy_obj_to_dict


def validate_user(Session: sessionmaker, user_data: dict) -> bool:

    # Create Session
    session = Session()

    email = user_data['email']
    password = user_data['password']

    # One or none returns a 
    user = session.query(User).filter(User.email == email).one_or_none()

    if user is not None:
        user = sqlalchemy_obj_to_dict(user)

    breakpoint()



def create_user(Session: sessionmaker, user_data: Dict) -> None:

    # Create Session

    user_exists = validate_user(
        Session=Session,
        user_data=user_data
    )

    session = Session()

    # Column values for a user row
    user_id = uuid.uuid4().hex
    email = user_data['email']
    password = user_data['password']

    # Construct an insert (executable statement) object
    # Insert object is created using insert()
    statement = (
        insert(User).values(
            user_id=user_id,
            email=email,
            password=password
        )
    )

    # A session takes an executable statement param
    # Examples of executable statements include
    # Insert, Update, Delete, Select etc
    session.execute(statement=statement)

    # Session.commit() is required to persist new data to our DB
    session.commit()

    session.close()
