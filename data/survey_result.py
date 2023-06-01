import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class SurveyResult(SqlAlchemyBase):
    __tablename__ = 'result_survey'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True,
                           autoincrement=True)
    id_survey = sqlalchemy.Column(sqlalchemy.Integer,
                                  sqlalchemy.ForeignKey("survey.id"))
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                  sqlalchemy.ForeignKey("survey.user_id"))
    id_question = sqlalchemy.Column(sqlalchemy.Integer)
    question = sqlalchemy.Column(sqlalchemy.String)
    answer1 = sqlalchemy.Column(sqlalchemy.String)
    num_answers1 = sqlalchemy.Column(sqlalchemy.Integer,
                                     default=0)
    answer2 = sqlalchemy.Column(sqlalchemy.String)
    num_answers2 = sqlalchemy.Column(sqlalchemy.Integer,
                                     default=0)
    answer3 = sqlalchemy.Column(sqlalchemy.String)
    num_answers3 = sqlalchemy.Column(sqlalchemy.Integer,
                                     default=0)
    answer4 = sqlalchemy.Column(sqlalchemy.String)
    num_answers4 = sqlalchemy.Column(sqlalchemy.Integer,
                                     default=0)
    surveys = orm.relationship('Survey', foreign_keys=[id_survey])
    surveys = orm.relationship('Survey', foreign_keys=[user_id])
