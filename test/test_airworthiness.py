from src.api.airworthiness import AirworthinessAPI
import hashlib
import unittest
import yaml


class TestAirworthiness(unittest.TestCase):
    def setUp(self):
        with open('config.yml', 'r') as f:
            self.setup = yaml.safe_load(f)

        self.airworthiness_api = AirworthinessAPI(
            base_url=self.setup['api']['base_url'],
            client_id=self.setup['api']['client_id'],
            database=self.setup['api']['database'],
            username=self.setup['api']['username'],
            password_hash=hashlib.md5(
                (self.setup['api']['password']).encode()
            )
        )

        self.parameter_settings = self.setup['api']['airworthiness']

    def test_get_parameter_list(self):

        parameter_list = self.airworthiness_api.get_aw_parameter_list()

        target_id = (
            self.parameter_settings['get_parameter_list']['parameter_id']
        )

        parameter_present = False

        for parameter in parameter_list['value']:
            if parameter['id'] == target_id:
                parameter_present = True

        self.assertTrue(parameter_present)

    def test_search_aw_parameter_id(self):

        search_id = self.parameter_settings['search_aw_parameter_id']['id']

        search_parameter = self.airworthiness_api.search_aw_parameter_id(
            parameter_id=search_id
        )

        self.assertEqual(search_id, search_parameter['id'])

    def test_edit_aw_parameter(self):

        parameter_number = (
            self.parameter_settings['edit_aw_parameter']['parameter_number']
        )
        new_standard = (
            self.parameter_settings['edit_aw_parameter']['standard']
        )

        metadata = {
            'parameter_number': parameter_number
        }
        new_metadata = {
            'standard': new_standard
        }

        self.airworthiness_api.create_aw_parameter(metadata)
        parameter_list = (
            self.airworthiness_api.get_aw_parameter_list()['value']
        )

        for parameter in parameter_list:
            if parameter['parameter_number'] == parameter_number:
                edit_id = parameter['id']

        self.airworthiness_api.edit_aw_parameter(
            parameter_id=edit_id,
            metadata=new_metadata
        )

        edit_success = False
        parameter_list = (
            self.airworthiness_api.get_aw_parameter_list()['value']
        )

        for parameter in parameter_list:
            keys = [key for key in parameter]
            if 'standard' not in keys:
                pass
            else:
                if parameter['standard'] == new_standard:
                    delete_id = parameter['id']
                    edit_success = True

        self.airworthiness_api.delete_aw_parameter(delete_id)
        self.assertTrue(edit_success)

    def test_delete_aw_parameter(self):

        parameter_number = (
            self.parameter_settings['delete_aw_parameter']['parameter_name']
        )

        metadata = {
            'parameter_number': parameter_number
        }

        self.airworthiness_api.create_aw_parameter(metadata)

        parameter_list = (
            self.airworthiness_api.get_aw_parameter_list()['value']
        )

        parameter_present = False

        for entry in parameter_list:
            if entry['parameter_number'] == parameter_number:
                parameter_present = True
                parameter_id = entry['id']

        self.assertTrue(parameter_present)

        self.airworthiness_api.delete_aw_parameter(parameter_id)

        parameter_list = (
            self.airworthiness_api.get_aw_parameter_list()['value']
        )

        for parameter in parameter_list:
            if parameter['id'] == parameter_id:
                parameter_present = True
            else:
                parameter_present = False

        self.assertFalse(parameter_present)

    def test_create_aw_parameter(self):

        parameter_name = (
            self.parameter_settings['create_aw_parameter']['parameter_name']
        )

        metadata = {
            'parameter_number': parameter_name
        }

        self.airworthiness_api.create_aw_parameter(metadata)

        parameter_found = False
        parameter_search = (
            self.airworthiness_api.get_aw_parameter_list()['value']
        )

        for parameter in parameter_search:
            if parameter['parameter_number'] == parameter_name:
                parameter_found = True
                aw_id = parameter['id']

        self.airworthiness_api.delete_aw_parameter(aw_id)
        self.assertTrue(parameter_found)

    def test_get_aw_para_list(self):
        parameter_id = (
            self.parameter_settings['get_aw_para_assessment_list']['id']
        )

        parameter_list = self.airworthiness_api.get_aw_para_assessment_list()

        example_found = False
        for parameter in parameter_list['value']:
            if parameter['id'] == parameter_id:
                example_found = True

        self.assertTrue(example_found)

    def test_search_aw_para_assessment_id(self):
        parameter_id = (
            self.parameter_settings['search_aw_para_assessment_id']['id']
        )
        parameter_name = (
            self.parameter_settings['search_aw_para_assessment_id']['name']
        )

        search_parameter = self.airworthiness_api.search_aw_para_assessment_id(
            parameter_id
        )

        self.assertEqual(parameter_name, search_parameter['aw_para'])

    def test_create_aw_para_assessment(self):
        aw_para = (
            self.parameter_settings['create_aw_para_assessment']['aw_para']
        )

        metadata = {
            'aw_para': aw_para
        }

        self.airworthiness_api.create_aw_parameter_assessment(metadata)

        para_list = (
            self.airworthiness_api.get_aw_para_assessment_list()['value']
        )

        found_entry = False

        for para in para_list:
            if para['aw_para'] == aw_para:
                found_entry = True
                found_id = para['id']

        self.airworthiness_api.delete_aw_assessment_parameter(found_id)
        self.assertTrue(found_entry)

    def test_edit_aw_para_assessment(self):
        aw_para = (
            self.parameter_settings['edit_aw_para_assessment']['aw_para']
        )
        oem = (
            self.parameter_settings['edit_aw_para_assessment']['oem']
        )

        metadata = {
            'aw_para': aw_para
        }
        update_metadata = {
            'oem': oem
        }

        self.airworthiness_api.create_aw_parameter_assessment(metadata)

        parameter_list = self.airworthiness_api.get_aw_para_assessment_list()

        for para in parameter_list['value']:
            if para['aw_para'] == aw_para:
                edit_id = para['id']

        self.airworthiness_api.edit_aw_parameter_assessment(
            parameter_id=edit_id,
            metadata=update_metadata
        )

        parameter_list = self.airworthiness_api.get_aw_para_assessment_list()

        edit_success = False

        for para in parameter_list['value']:
            key_list = [key for key in para]
            if 'oem' not in key_list:
                pass
            else:
                if para['oem'] == oem:
                    delete_id = para['id']
                    edit_success = True

        self.airworthiness_api.delete_aw_assessment_parameter(delete_id)
        self.assertTrue(edit_success)

    def test_delete_aw_para_assessment(self):
        aw_para = (
            self.parameter_settings['delete_aw_para_assessment']['aw_para']
        )

        metadata = {
            'aw_para': aw_para
        }

        self.airworthiness_api.create_aw_parameter_assessment(metadata)

        parameter_present = False

        parameter_list = self.airworthiness_api.get_aw_para_assessment_list()

        for para in parameter_list['value']:
            if para['aw_para'] == aw_para:
                delete_id = para['id']
                parameter_present = True

        self.assertTrue(parameter_present)

        self.airworthiness_api.delete_aw_assessment_parameter(delete_id)

        parameter_list = self.airworthiness_api.get_aw_para_assessment_list()

        for para in parameter_list['value']:
            if para['id'] == delete_id:
                parameter_present = True
            else:
                parameter_present = False

        self.assertFalse(parameter_present)
