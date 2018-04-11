"""This module manages the application"""

import os
import argparse
import configparser


CONFIG_PATH = '/opt/filerestapi/etc/config.ini'


def main(args):
    """Main function"""
    config = configparser.RawConfigParser()
    config.read(CONFIG_PATH)

    if args.dbpath is not None:
        config.set('DB', 'path', args.dbpath)
    if args.filestorage_path is not None:
        config.set('FileStorage', 'path', args.filestorage_path)

    config.write(open(CONFIG_PATH, 'w'))

    if args.clean:
        dbpath = config.get('DB', 'path')
        if os.path.exists(dbpath):
            os.remove(dbpath)
        else:
            print('This path is not exists: {}'.format(dbpath))

        filestorage_path = config.get('FileStorage', 'path')
        for filename in os.listdir(filestorage_path):
            filename = os.path.join(filestorage_path, filename)
            os.remove(filename)


def build_argparser():
    """Build a ArgumentParser"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--dbpath', help='Path to the DB')
    parser.add_argument('--filestorage_path', help='Path to the FileStorage')
    parser.add_argument('--clean', action='store_true', help='Clean a data')
    return parser


if __name__ == '__main__':
    main(build_argparser().parse_args())
    