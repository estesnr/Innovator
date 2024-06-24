from src.api.documents import DocumentAPI
import hashlib
import unittest
import yaml


class TestDocuments(unittest.TestCase):

    def setUp(self):
        with open('config.yml', 'r') as f:
            self.setup = yaml.safe_load(f)

        self.documents_api = DocumentAPI(
            base_url=self.setup['api']['base_url'],
            client_id=self.setup['api']['client_id'],
            database=self.setup['api']['database'],
            username=self.setup['api']['username'],
            password_hash=hashlib.md5(
                (self.setup['api']['password']).encode()
            )
        )

    def test_get_documents_list(self):

        documents_list = self.documents_api.get_document_list()

        document_id_compare = self.setup['api']['documents']['id']

        self.assertIsInstance(documents_list, dict)

        example_find = False
        for entry in documents_list['value']:
            for key, value in entry.items():
                if key == 'id' and value == document_id_compare:
                    example_find = True

        self.assertTrue(example_find)

    def test_search_document_name(self):

        search_name = self.setup['api']['documents']['name']
        search_id = self.setup['api']['documents']['id']

        document_search = self.documents_api.search_document_name(search_name)

        self.assertIsInstance(document_search, dict)

        for entry in document_search['value']:
            for key, value in entry.items():
                if key == 'id':
                    document_id = value

        self.assertEqual(search_id, document_id)

    def test_search_document_id(self):

        search_name = self.setup['api']['documents']['name']
        search_id = self.setup['api']['documents']['id']

        document_search = self.documents_api.search_document_id(search_id)

        self.assertIsInstance(document_search, dict)

        for key, value in document_search.items():
            if key == 'name':
                document_name = value

        self.assertEqual(search_name, document_name)

    def test_delete_document(self):

        create_name = self.setup['api']['documents']
        create_name = create_name['delete_document']['create_name']

        create_number = self.setup['api']['documents']
        create_number = create_number['delete_document']['create_number']

        self.documents_api.create_document(create_name, create_number)

        document = self.documents_api.search_document_name(create_name)

        for entry in document['value']:
            for key, value in entry.items():
                if key == 'id':
                    document_id = value

        self.documents_api.delete_document(document_id)

        list_of_ids = []

        for entry in self.documents_api.get_document_list()['value']:
            for key, value in entry.items():
                if key == 'id':
                    list_of_ids.append(value)

        self.assertNotIn(document_id, list_of_ids)

    def test_create_document(self):

        create_name = self.setup['api']['documents']
        create_name = create_name['delete_document']['create_name']

        create_number = self.setup['api']['documents']
        create_number = create_number['delete_document']['create_number']

        self.documents_api.create_document(create_name, create_number)

        document = self.documents_api.search_document_name(create_name)

        for entry in document['value']:
            for key, value in entry.items():
                if key == "name":
                    document_name = value

        self.assertEqual(document_name, create_name)
