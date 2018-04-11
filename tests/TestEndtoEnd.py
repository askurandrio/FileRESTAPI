"""Test for all application"""
#TODO: Rework this

import io
import os
import sys
import unittest
import subprocess

import requests


URI = 'http://127.0.0.1:80'


class TestEndtoEnd(unittest.TestCase):
    """Test all application"""

    def test_add_file(self):
        """The file creation test"""
        filename = 'test_add_file.data'
        file_content = b'012345678910'
        post_req = requests.post('{}/file'.format(URI),
                                 data=io.BytesIO(file_content),
                                 params={'filename':filename},
                                 stream=True)
        self.assertEqual(post_req.status_code, 201)
        file_id = post_req.json()['file_id']

        req_get_all = requests.get('{}/file'.format(URI))
        self.assertEqual(req_get_all.status_code, 200)
        req_get_all_json = req_get_all.json()
        self.assertEqual(req_get_all_json['content'][0]['id'], file_id)
        self.assertEqual(req_get_all_json['content'][0]['filename'], filename)
        self.assertEqual(req_get_all_json['content'][0]['size'], len(file_content))

        req_get = requests.get('{}/file/{}'.format(URI, file_id), stream=True)
        self.assertEqual(req_get.status_code, 200)
        self.assertEqual(req_get.raw.read(), file_content)

        req_inc_get = requests.get('{}/page/{}'.format(URI, 10))
        self.assertEqual(req_inc_get.status_code, 404)

    def test_add_large_file(self):
        """The large file creation test"""
        gb = 1024 * 1024 * 1024
        post_req = requests.post('{}/file'.format(URI),
                                 data=(os.urandom(gb) for _ in range(10)),
                                 params={'filename':'test_large_file.data'},
                                 stream=True)
        self.assertEqual(post_req.status_code, 201)
        file_id = post_req.json()['file_id']

        req_get = requests.get('{}/file/{}'.format(URI, file_id), stream=True)
        self.assertEqual(req_get.status_code, 200)


    def test_del_file(self):
        """The file delete test"""
        post_req = requests.post('{}/file'.format(URI),
                                 data=io.BytesIO(b'012345678910'),
                                 params={'filename':'test_del_file.data'},
                                 stream=True)
        self.assertEqual(post_req.status_code, 201)
        file_id = post_req.json()['file_id']

        req_get = requests.get('{}/file/{}'.format(URI, file_id), stream=True)
        self.assertEqual(req_get.status_code, 200)

        req_del = requests.delete('{}/file/{}'.format(URI, file_id))
        self.assertEqual(req_del.status_code, 200)

        req_get = requests.get('{}/file/{}'.format(URI, file_id), stream=True)
        self.assertEqual(req_get.status_code, 404)

    @classmethod
    def tearDownClass(cls):
        process = subprocess.Popen(['python3', '/opt/filerestapi/bin/manager.py', '--clean'],
                                   stdout=sys.stdout,
                                   stdin=sys.stdin)
        process.communicate()
        assert process.returncode == 0
