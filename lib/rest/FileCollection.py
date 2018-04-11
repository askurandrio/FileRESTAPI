"""This module defines the FileResource class"""

import flask
from flask import request
import flask_restful

from lib.db import make_session, File


class FileResource(flask_restful.Resource):
    """The REST endpoint for File"""

    @staticmethod
    def post():
        """Create a new file"""
        session = make_session()
        file = File.create(session, request.args['filename'], stream=request.stream)
        session.commit()
        return {'file_id':file.oid}, 201

    @staticmethod
    def get(file_id=None):
        """Get the file or files info"""
        session = make_session()
        if file_id is None:
            #Directory support is not yet implemented...
            root = {'dirname':'/', 'type':'directory', 'content':[]}
            for file in session.query(File):
                file_data = {'type':'file',
                             'id':file.oid,
                             'filename':file.filename,
                             'size':file.size}
                root['content'].append(file_data)
            return root, 200

        file = session.query(File).get(file_id)

        if file is None:
            return 'File not found', 404
        def read_file():
            """Read th file"""
            fstream = file.openf('rb')
            while True:
                buf = fstream.read(1024)
                if not buf:
                    break
                yield buf
        return flask.Response(read_file())

    @staticmethod
    def delete(file_id):
        """Delete the file"""
        session = make_session()
        file = session.query(File).get(file_id)
        if file is None:
            return 'File not found', 404
        file.delete(session)
        session.commit()
        return '', 200
