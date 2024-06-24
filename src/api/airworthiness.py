from .common import CommonAPI
import json
import requests


class AirworthinessAPI(CommonAPI):
    """
    Container for methods pertaining to the custom parameters for Airworthiness
    in the Aras Innovator Space.
    """
    def get_aw_parameter_list(self):
        """
        Creates a list of Airworthiness Parameters
        """
        query_url = f"{self._base_url}/server/odata/Airworthiness Parameter"

        query_response = requests.get(
            url=query_url,
            headers=self._headers_auth
        )

        return query_response.json()

    def search_aw_parameter_id(self, parameter_id):
        """
        Searches for a specific airworthiness parameter based on unique id
        number.

        Parameters
        ----------
        parameter_id: str
            unique identification number assigned to a parameter upon creation
        """
        query_url = (
            f"{self._base_url}/server/odata/"
            f"Airworthiness Parameter('{parameter_id}')"
        )

        query_response = requests.get(
            url=query_url,
            headers=self._headers_auth
        )

        return query_response.json()

    def create_aw_parameter(self, metadata):
        """
        Creates a new entry within the Airworthiness Parameter database.

        Parameters
        ----------
        metadata: dict
            dictionary of data entries to be assigned to the new Airworthiness
            entry. Must include an entry for 'parameter_number'.
        """
        valid_keys = [
            'parameter_number',
            'certification_criteria',
            'method_of_compliance',
            'standard'
        ]

        for key in metadata:
            if key not in valid_keys:
                raise KeyError(
                    f"Invalid entry '{key}'. Valid entries are {valid_keys}"
                )

        self._validate_metadata(metadata)

        converted_metadata = json.dumps(metadata)

        query_url = f"{self._base_url}/server/odata/Airworthiness Parameter"

        query_response = requests.post(
            url=query_url,
            headers=self._headers_auth,
            data=converted_metadata
        )

        return query_response.json()

    def edit_aw_parameter(self, parameter_id, metadata):
        """
        Edits an existing Airworthiness Parameter.

        Parameters
        ----------
        parameter_id: str
            the id number of the parameter that is assigned upon creation

        metadata: dict
            dictionary of data entries to be edited to the Airworthiness
            entry.
        """
        valid_keys = [
            'parameter_number',
            'certification_criteria',
            'method_of_compliance',
            'standard'
        ]

        if not isinstance(parameter_id, str):
            raise TypeError(
                'part_id must be formatted as a string'
            )

        for key in metadata:
            if key not in valid_keys:
                raise KeyError(
                    f"Invalid key '{key}'. Valid entries are {valid_keys}"
                )

        self._validate_metadata(metadata)

        converted_metadata = json.dumps(metadata)

        query_url = (
            f"{self._base_url}/server/odata/Airworthiness "
            f"Parameter('{parameter_id}')"
        )

        query_response = requests.patch(
            url=query_url,
            headers=self._headers_auth,
            data=converted_metadata
        )

        return query_response.json()

    def delete_aw_parameter(self, parameter_id):
        """
        Deletes an Airworthiness Parameter entry.

        Parameters
        ----------
        parameter_id: str
            id value of the Parameter entry, which is assigned upon creation.
        """
        if not isinstance(parameter_id, str):
            raise TypeError(
                'parameter_id must be formatted as a string'
            )

        query_url = (
            f"{self._base_url}/server/odata/"
            f"Airworthiness Parameter('{parameter_id}')"
        )

        query_response = requests.delete(
            url=query_url,
            headers=self._headers_auth
        )

        return query_response

    def get_aw_para_assessment_list(self):
        """
        Returns a list of Airworthiness Parameter Assessment entries.
        """
        query_url = (
            f"{self._base_url}/server/odata/Airworthiness Para Assessment"
        )

        query_response = requests.get(
            url=query_url,
            headers=self._headers_auth
        )

        return query_response.json()

    def search_aw_para_assessment_id(self, parameter_id):
        """
        Searches for a specific Airworthiness Parameter Assessment entry by
        id number.

        Parameters
        ----------
        parameter_id: str
            the unique id number for an entry that is assigned upon creation
        """
        if not isinstance(parameter_id, str):
            raise TypeError("parameter_id must be formatted as a string")

        query_url = (
            f"{self._base_url}/server/odata/Airworthiness Para Assessment"
            f"('{parameter_id}')"
        )

        query_response = requests.get(
            url=query_url,
            headers=self._headers_auth
        )

        return query_response.json()

    def edit_aw_parameter_assessment(self, parameter_id, metadata):
        """
        Edit the metadata for an Airworthiness Parameter Assessment entry.

        Parameters
        ----------
        parameter_id: str
            id number of the Assessment Parameter being edited

        metadata: dict
            key, value pair dictionary which consists of the metadata that is
            being written to the Assessment Parameter
        """
        if not isinstance(parameter_id, str):
            raise TypeError('parameter_id must be formatted as a string')
        if not isinstance(metadata, dict):
            raise TypeError('metadata must be formatted as a key, value dict')

        VALID_KEYS = [
            'aw_para',
            'na_rationale',
            'non_compliance_rationale',
            'oem',
            'oem_expected_compliance',
            'oem_method_of_compliance',
            'oem_responsible_engineer',
            'oem_standard',
            'friendly_name',
            'compliance'
        ]

        for key in metadata:
            if key not in VALID_KEYS:
                raise ValueError(
                    f"Invalid key '{key}'. Valid keys are {VALID_KEYS}"
                )

        self._validate_metadata(metadata)

        query_url = (
            f"{self._base_url}/server/odata/Airworthiness Para"
            f" Assessment('{parameter_id}')"
        )

        converted_metadata = json.dumps(metadata)

        query_response = requests.patch(
            url=query_url,
            headers=self._headers_auth,
            data=converted_metadata
        )

        return query_response.json()

    def create_aw_parameter_assessment(self, metadata):
        """
        Creates a new Airworthiness Parameter Assessment entry.

        Parameters
        ----------

        metadata: dict
            key, value pair dictionary which consists of the metadata that is
            being written to the Assessment Parameter
        """
        if not isinstance(metadata, dict):
            raise TypeError('metadata must be formatted as a key, value dict')

        VALID_KEYS = [
            'aw_para',
            'na_rationale',
            'non_compliance_rationale',
            'oem',
            'oem_expected_compliance',
            'oem_method_of_compliance',
            'oem_responsible_engineer',
            'oem_standard',
            'friendly_name',
            'compliance'
        ]

        for key in metadata:
            if key not in VALID_KEYS:
                raise ValueError(
                    f"Invalid key '{key}'. Valid keys are {VALID_KEYS}"
                )

        self._validate_metadata(metadata)

        query_url = (
            f"{self._base_url}/server/odata/Airworthiness Para Assessment"
        )

        converted_metadata = json.dumps(metadata)

        query_response = requests.post(
            url=query_url,
            headers=self._headers_auth,
            data=converted_metadata
        )

        return query_response.json()

    def delete_aw_assessment_parameter(self, parameter_id):
        """
        Deletes an Airworthiness Assessment Parameter entry.

        Parameters
        ----------
        parameter_id: str
            unique ID number for a the entry being deleted.
        """
        if not isinstance(parameter_id, str):
            raise TypeError('parameter_id must be formatted as a string')

        query_url = (
            f"{self._base_url}/server/odata/Airworthiness Para"
            f" Assessment('{parameter_id}')"
        )

        query_response = requests.delete(
            url=query_url,
            headers=self._headers_auth
        )

        return query_response

    def _validate_metadata(self, metadata):
        """
        Validates standard metadata entries for proper formatting.

        Parameters
        ----------
        metadata: dict
            dictionary of items being validated
        """

        if not isinstance(metadata, dict):
            raise TypeError('metadata must be a key, value formatted dict')

        keys = {
            'aw_para': str,
            'na_rationale': str,
            'non_compliance_rationale': str,
            'oem': str,
            'oem_expected_compliance': str,
            'oem_method_of_compliance': str,
            'oem_responsible_engineer': str,
            'oem_standard': str,
            'friendly_name': str,
            'compliance': bool,
            'parameter_number': str,
            'standard': str,
            'certification_criteria': str,
            'method_of_compliance': str
        }

        for title, entry in metadata.items():
            for key, value in keys.items():
                if title == key and type(entry) != value:
                    raise TypeError(
                        f"{title} contains invalid data type. Must be "
                        f"formatted as a {value}."
                    )
