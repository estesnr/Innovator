from src.api.files import FilesAPI
import hashlib
import unittest
import yaml


class TestFiles(unittest.TestCase):

    def setUp(self):
        with open('config.yml', 'r') as f:
            self.setup = yaml.safe_load(f)

        self.file_parameters = self.setup['api']['files']

        self.files_api = FilesAPI(
            base_url=self.setup['api']['base_url'],
            client_id=self.setup['api']['client_id'],
            database=self.setup['api']['database'],
            username=self.setup['api']['username'],
            password_hash=hashlib.md5(
                (self.setup['api']['password']).encode()
            )
        )

    def test_get_file_list(self):

        file_list = self.files_api.get_file_list()

        file_id_compare = self.file_parameters['get_file_list']['id']

        self.assertIsInstance(file_list, dict)

        example_find = False
        for entry in file_list['value']:
            for key, value in entry.items():
                if key == 'id' and value == file_id_compare:
                    example_find = True

        self.assertTrue(example_find)

    def test_search_file_name(self):

        search_name = self.file_parameters['search_file_name']['name']

        file_search = self.files_api.search_file_name(search_name)

        self.assertIsInstance(file_search, dict)

        example_find = False
        for entry in file_search['value']:
            if entry['filename'] == search_name:
                example_find = True

        self.assertTrue(example_find)

    def test_search_file_id(self):
        search_id = self.file_parameters['search_file_id']['id']

        file_search = self.files_api.search_file_id(search_id)

        self.assertIsInstance(file_search, dict)

        example_find = False
        if file_search['id'] == search_id:
            example_find = True
        
        self.assertTrue(example_find)

    def test_upload_document(self):
        local_path = self.file_parameters['upload_file']['file']

        file_name = local_path.split('/')[1]

        self.files_api.upload_file(local_path, file_name)

        file_list = self.files_api.get_file_list()

        example_found = False
        for entry in file_list['value']:
            if entry['filename'] == file_name:
                example_id = entry['id']
                example_found = True

        self.files_api.delete_file(example_id)
        self.assertTrue(example_found)

    def test_delete_file(self):
        local_path = self.file_parameters['delete_file']['file']

        file_name = local_path.split('/')[1]

        self.files_api.upload_file(local_path, file_name)

        file_list = self.files_api.get_file_list()

        example_found = False
        for file in file_list['value']:
            if file['filename'] == file_name:
                delete_id = file['id']
                example_found = True

        self.assertTrue(example_found)

        self.files_api.delete_file(delete_id)

        id_list = []

        file_list = self.files_api.get_file_list()

        for file in file_list['value']:
            id_list.append(file['id'])

        self.assertNotIn(delete_id, id_list)
