"""The lib package"""

import sys
import logging


LOGGER = logging.getLogger('FileRESTAPI')


def _make_loghandlers():
    """Make handlers for logger"""
    formatter = logging.Formatter('%(process)d %(asctime)s: [%(levelname)s] %(message)s')

    stdout = logging.StreamHandler(sys.stdout)
    stdout.setFormatter(formatter)
    LOGGER.addHandler(stdout)


_make_loghandlers()
