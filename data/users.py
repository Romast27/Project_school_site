from .db_session import SqlAlchemyBase
from flask_login import UserMixin
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash

import sqlalchemy


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    password = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    # about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    remember_me = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    # type_user = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=1)
    # news = orm.relationship("News", back_populates='user')
    # def set_password(self, password):
        # self.hashed_password = generate_password_hash(password)
    
    # def check_password(self, password):
        # return check_password_hash(self.hashed_password, password)
