from src.api.parts import PartsAPI
import hashlib
import unittest
import yaml


class TestParts(unittest.TestCase):

    def setUp(self):
        with open('config.yml', 'r') as f:
            self.setup = yaml.safe_load(f)

        self.parts_api = PartsAPI(
            base_url=self.setup['api']['base_url'],
            client_id=self.setup['api']['client_id'],
            database=self.setup['api']['database'],
            username=self.setup['api']['username'],
            password_hash=hashlib.md5(
                (self.setup['api']['password']).encode()
            )
        )

    def test_get_parts_list(self):

        parts_list = self.parts_api.get_parts_list()

        self.assertIsInstance(parts_list, dict)

        example_present = True

        for entry in parts_list['value']:
            for key, value in entry.items():
                if key == 'id':
                    if value == self.setup['api']['parts']['id']:
                        example_present = True

        self.assertTrue(example_present)

    def test_search_part_number(self):

        part_number = self.setup['api']['parts']['part_number']

        part_search = self.parts_api.search_part_number(part_number)

        self.assertIsInstance(part_search, dict)

        for entry in part_search['value']:
            for key, value in entry.items():
                if key == 'description':
                    part_type = value
                if key == 'id':
                    part_id = value

        self.assertEqual(
            part_type, self.setup['api']['parts']['description']
        )
        self.assertEqual(part_id, self.setup['api']['parts']['id'])

    def test_search_part_type(self):

        part_type = self.setup['api']['parts']['description']

        search_part_type = self.parts_api.search_part_type(part_type)

        self.assertIsInstance(search_part_type, dict)

        id_list = []
        part_number_list = []

        for entry in search_part_type['value']:
            for key, value in entry.items():
                if key == 'id':
                    id_list.append(value)
                if key == 'item_number':
                    part_number_list.append(value)

        self.assertIn(
            self.setup['api']['parts']['id'],
            id_list
        )
        self.assertIn(
            self.setup['api']['parts']['part_number'],
            part_number_list
        )

    def test_search_part_id(self):

        part_id = self.setup['api']['parts']['id']

        search_part_id = self.parts_api.search_part_id(part_id)

        self.assertIsInstance(search_part_id, dict)

        for key, value in search_part_id.items():
            if key == 'item_number':
                item_number = value
            if key == 'description':
                part_description = value

        self.assertEqual(
            item_number,
            self.setup['api']['parts']['part_number']
        )
        self.assertEqual(
            part_description,
            self.setup['api']['parts']['description']
        )

    def test_create_part(self):

        metadata = self.setup['api']['parts']['create_part']['metadata']

        self.parts_api.create_part(metadata)

        part_search = self.parts_api.search_part_number(
            metadata['item_number']
        )

        self.assertIsInstance(part_search, dict)

        for entry in part_search['value']:
            for key, value in entry.items():
                if key == 'item_number':
                    part_type = value

        self.assertEqual(
            part_type,
            self.setup['api']['parts']['create_part']
            ['metadata']['item_number']
        )

    def test_update_part(self):

        update_metadata = {
            'description': self.setup['api']['parts']['update_part']['update']
        }

        create_metadata = {
            'item_number': self.setup['api']['parts']['update_part']['create']
        }

        self.parts_api.create_part(create_metadata)

        search_part_number = create_metadata['item_number']

        part_search = self.parts_api.search_part_number(search_part_number)

        for entry in part_search['value']:
            for key, value in entry.items():
                if key == 'id':
                    part_id = value

        self.parts_api.update_part(part_id, update_metadata)

        part_search = self.parts_api.search_part_number(search_part_number)

        for entry in part_search['value']:
            for key, value in entry.items():
                if key == 'description':
                    part_description = value

        self.assertEqual(part_description, update_metadata['description'])

    def test_delete_part(self):
        part = self.setup['api']['parts']['delete_part']

        create_metadata = {
            'item_number': part['item_number']
        }

        self.parts_api.create_part(create_metadata)

        part_search = self.parts_api.search_part_number(part['item_number'])

        for entry in part_search['value']:
            for key, value in entry.items():
                if key == 'id':
                    part_id = value

        self.parts_api.delete_part(part_id)

        parts_search = self.parts_api.get_parts_list()

        part_find = False

        for part in parts_search['value']:
            for key, value in part.items():
                if key == 'id' and value == part_id:
                    part_find = True

        self.assertFalse(part_find)

    def test_get_assembly(self):

        search_metadata = self.setup['api']['parts']['get_assembly']['id']

        find_assembly = self.parts_api.get_assembly(search_metadata)

        self.assertIsInstance(find_assembly, dict)
        self.assertNotEqual(len(find_assembly), 0)

    def test_create_assembly(self):

        bom_dict = self.setup['api']['parts']['create_assembly']

        parent_part = bom_dict['parent_name']

        child_parts = [
            bom_dict['child_1_name'],
            bom_dict['child_2_name']
        ]

        metadata = []

        for item in child_parts:
            metadata.append({
                'related_id': {
                    'item_number': item
                }
            })

        self.parts_api.create_assembly(
            item_number='test',
            assembly_name=parent_part,
            metadata=metadata
        )

        id_list = []

        part_name_search = self.parts_api.search_part_name(parent_part)

        for entry in part_name_search['value']:
            part_id = entry['id']
            id_list.append(part_id)

        assembly_search = self.parts_api.get_assembly(part_id)

        assembly_children = []

        for entry in assembly_search['value']:
            for key, value in entry.items():
                if key == 'related_id':
                    assembly_children.append(value['item_number'])
                    id_list.append(value['id'])

        for id in id_list:
            self.parts_api.delete_part(id)

        self.assertEqual(assembly_children, child_parts)

    def test_link_child_part(self):

        part_info = self.setup['api']['parts']['link_child_part']

        parent_name = part_info['parent_name']
        child_name = part_info['child_name']

        metadata = {
            "name": parent_name,
            "classification": "Assembly",
            "item_number": parent_name
        }

        child_metadata = {
            "name": child_name,
            "classification": "Component",
            "item_number": child_name
        }

        self.parts_api.create_part(metadata)
        self.parts_api.create_part(child_metadata)

        id_list = []

        assembly_search = self.parts_api.search_part_name(parent_name)

        self.assertIsInstance(assembly_search, dict)

        for entry in assembly_search['value']:
            for key, value in entry.items():
                if key == 'id':
                    assembly_id = value
                    id_list.append(assembly_id)

        child_search = self.parts_api.get_parts_list()

        for entry in child_search['value']:
            for key, value in entry.items():
                if key == 'name' and value == child_name:
                    child_id = entry['id']

        self.parts_api.link_child_part(assembly_id, child_id)

        assembly_check = self.parts_api.get_assembly(assembly_id)

        child_check = []

        self.assertIsInstance(assembly_search, dict)

        for entry in assembly_check['value']:
            for key, value in entry['related_id'].items():
                if key == 'name':
                    child_check.append(value)
                if key == 'id':
                    id_list.append(value)

        for id in id_list:
            self.parts_api.delete_part(id)

        self.assertIn(child_name, child_check)

    def test_search_linked_CAD_files(self):

        search_info = self.setup['api']['parts']['search_linked_CAD_files']
        assembly_id = search_info['assembly_id']
        document_name = search_info['CAD_name']

        cad_search = self.parts_api.search_linked_CAD_files(assembly_id)

        for entry in cad_search['value']:
            for key, value in entry['related_id'].items():
                if key == 'item_number':
                    cad_number = value

        self.assertEqual(document_name, cad_number)

    def test_link_cad_document(self):

        cad_info = self.setup['api']['parts']['link_cad_document']
        parent_name = cad_info['parent_name']
        cad_id = cad_info['cad_id']

        parent_metadata = {
            "item_number": parent_name
        }

        self.parts_api.create_part(parent_metadata)

        part_search = self.parts_api.search_part_number(parent_name)

        for part in part_search['value']:
            parent_id = part['id']

        self.parts_api.link_CAD_document(parent_id, cad_id)

        part_search = self.parts_api.search_part_number(parent_name)

        for part in part_search['value']:
            parent_id = part['id']

        cad_search = self.parts_api.search_linked_CAD_files(parent_id)


        self.parts_api.delete_part(parent_id)

        self.assertNotEqual(cad_search['value'], [])
