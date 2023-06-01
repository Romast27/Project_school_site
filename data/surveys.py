import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Survey(SqlAlchemyBase):
    __tablename__ = 'survey'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    user = orm.relationship('User', foreign_keys=[user_id])
    user_name = sqlalchemy.Column(sqlalchemy.String,
                                sqlalchemy.ForeignKey("users.name"))
    user = orm.relationship('User', foreign_keys=[user_name])
