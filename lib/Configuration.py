"""The file defines the Configuration classs"""

import configparser


class Configuration:
    """Config class to parse and work with configuration values"""
    __CONFIG_PATH = '/opt/filerestapi/etc/config.ini'

    def __init__(self):
        self.__config = configparser.RawConfigParser()
        self.__config.read(self.__CONFIG_PATH)

    def get_dbpath(self):
        """Getting path to the DB"""
        return self.__config.get('DB', 'path')

    def get_filestorage_path(self):
        """Getting path to the FileStorage"""
        return self.__config.get('FileStorage', 'path')

