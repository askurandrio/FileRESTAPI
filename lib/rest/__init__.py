"""The rest package"""

import logging

import flask
import flask_restful
from werkzeug.serving import WSGIRequestHandler


from .FileCollection import FileResource


LOGGER = logging.getLogger('FileRESTAPI')


WSGIRequestHandler.protocol_version = "HTTP/1.1"
APP = flask.Flask('WikiRESTAPI')
APP.config['PROPAGATE_EXCEPTIONS'] = True
API = flask_restful.Api(APP)
API.add_resource(FileResource, '/file', '/file/<int:file_id>')


@APP.errorhandler(Exception)
def _(_):
    """Standard error handler for APP"""
    LOGGER.exception('Error when processing request')
    return {}, 500
