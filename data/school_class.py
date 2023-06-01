import sqlalchemy

from .db_session import SqlAlchemyBase


class School_class(SqlAlchemyBase):
    __tablename__ = 'school_class'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title_class = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    teacher = sqlalchemy.Column(sqlalchemy.String, nullable=True)
