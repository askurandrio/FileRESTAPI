"""This module defines engine and session"""

import sqlalchemy
import sqlalchemy.ext.declarative

from ..Configuration import Configuration


BASE = sqlalchemy.ext.declarative.declarative_base()
SESSIONMAKER = None


def make_session():
    """Make a session"""
    global SESSIONMAKER #pylint: disable=W0603
    if SESSIONMAKER is None:
        SESSIONMAKER = make_sessionmaker(Configuration().get_dbpath())
    return SESSIONMAKER()


def make_sessionmaker(dbpath):
    """Make a sessionmaker"""
    engine = sqlalchemy.create_engine(dbpath)
    BASE.metadata.create_all(engine)
    return sqlalchemy.orm.sessionmaker(bind=engine)
