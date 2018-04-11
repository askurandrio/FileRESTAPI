"""This module defines the class File"""

import os
import shutil
import sqlalchemy

from ..Configuration import Configuration
from .db_session import BASE


class File(BASE):
    """This is the class for represent Files in the DB"""
    __tablename__ = 'files'
    oid = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    filename = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    size = sqlalchemy.Column(sqlalchemy.BigInteger, nullable=False)

    def __init__(self, oid, filename, size):
        self.oid = oid
        self.filename = filename
        self.size = size

    def __get_realy_filename(self):
        """Get the real file name"""
        return os.path.join(Configuration().get_filestorage_path(), str(self.oid))

    def openf(self, flags):
        """Open the file"""
        return open(self.__get_realy_filename(), flags)

    def rewrite(self, start_byte, stream):
        """Rewrite part of file"""
        with self.openf('ab') as file:
            file.seek(start_byte, 0)
            shutil.copyfileobj(stream, file)
        file.close()
        self.recalc_size()

    def recalc_size(self):
        """Recalculate size of file"""
        self.size = os.path.getsize(self.__get_realy_filename())

    def delete(self, session):
        """Delete the file"""
        os.remove(self.__get_realy_filename())
        session.delete(self)

    @classmethod
    def create(cls, session, filename, stream):
        """Create a new File"""
        file = cls(None, filename, 0)
        session.add(file)
        session.flush()

        shutil.copyfileobj(stream, file.openf('wb'))
        file.recalc_size()
        return file
