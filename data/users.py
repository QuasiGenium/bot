import datetime
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    room = sqlalchemy.Column(sqlalchemy.String)
    moves = sqlalchemy.Column(sqlalchemy.String)
    another = sqlalchemy.Column(sqlalchemy.String)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)