import datetime
import sqlalchemy

from .db_session import SqlAlchemyBase


class Class_news(SqlAlchemyBase):
    __tablename__ = 'class_news'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    id_class = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    photo = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.Date,
                                     default=datetime.date.today)
    primary_news = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)