"""This module defines engine and session"""

import sqlalchemy
import sqlalchemy.ext.declarative

from ..Configuration import Configuration


BASE = sqlalchemy.ext.declarative.declarative_base()


def make_session():
    """Make a session"""
    sessionmaker = make_sessionmaker('sqlite:///' + Configuration().get_dbpath())
    return sessionmaker()


def make_sessionmaker(dbpath):
    """Make a sessionmaker"""
    engine = sqlalchemy.create_engine(dbpath)
    BASE.metadata.create_all(engine)
    return sqlalchemy.orm.sessionmaker(bind=engine)
