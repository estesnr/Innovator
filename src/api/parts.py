from .common import CommonAPI
import json
import requests


class PartsAPI(CommonAPI):
    """
    Class to handle functions pertaining to parts located in Aras.
    """

    def get_parts_list(self):
        """
        Return a list of dicts for all Part items in Aras.
        """
        query_url = f"{self._base_url}/server/odata/Part"

        query_response = requests.get(
            url=query_url,
            headers=self._headers_auth
        )

        return query_response.json()

    def search_part_number(self, part_number):
        """
        Return pertinent data for a part number.

        Parameters
        ----------
        part_number: str
            manufacturer's part number
        """
        # checks if part number is valid
        if not isinstance(part_number, str):
            raise ValueError("Part Number must be formatted as a string.")

        query_url = (
            f"{self._base_url}/server/odata/Part?$"
            f"filter=item_number eq {part_number}"
        )

        query_response = requests.get(
            url=query_url,
            headers=self._headers_auth
        )

        return query_response.json()

    def search_part_name(self, part_name):
        """
        Return pertinent data for a part based on name.

        Parameters
        ----------
        part_number: str
            manufacturer's part number
        """
        # checks if part number is valid
        if not isinstance(part_name, str):
            raise ValueError("Part Name must be formatted as a string.")

        query_url = (
            f"{self._base_url}/server/odata/Part?$"
            f"filter=name eq {part_name}"
        )

        query_response = requests.get(
            url=query_url,
            headers=self._headers_auth
        )

        return query_response.json()

    def search_part_type(self, part_type):
        """
        Searches for a list of parts based on category.
        Example: "Gasket, Screw, etc..."

        Parameters
        ----------
        part_type: str
            The type of part being searched
        """
        # checks part type is valid
        if not isinstance(part_type, str):
            raise ValueError(
                "Part must be structured as a string."
            )

        query_url = (
            f"{self._base_url}/server/odata/Part?"
            f"$filter=description eq {part_type}"
        )

        query_response = requests.get(
            url=query_url,
            headers=self._headers_auth
        )

        return query_response.json()

    def search_part_id(self, part_id):
        """
        Searches for information on a part based on part id number.

        Parameters
        ----------
        part_id: str
            the id number of the part to be searched
        """
        # checks part id is valid
        if not isinstance(part_id, str):
            raise ValueError(
                "Part Id number must be formatted as a string."
            )

        query_url = f"{self._base_url}/server/odata/Part('{part_id}')"

        query_response = requests.get(
            url=query_url,
            headers=self._headers_auth
        )

        return query_response.json()

    def create_part(self, metadata):
        """
        Enters a new part into the database along with pertinent metadata.

        Parameters
        ----------
        metadata: dict
            Dictionary of metadata entires that get assigned to the newly
            created part.
        """
        # check if metadata is valid
        if not isinstance(metadata, dict):
            raise ValueError(
                "Metadata must be structured as a key:value pair dictionary."
            )

        valid_keys = [
            'classification',
            'created_on',
            'description',
            'external_owner',
            'generation',
            'keyed_name',
            'name',
            'state',
            'unit',
            'item_number',
            'itemtype',
            'quantity',
            'related_id'
        ]

        for key in metadata:
            if key not in valid_keys:
                raise RuntimeError(
                    "Invalid Metadata entry. Valid keys are 'description,"
                    "'name, 'keyed_name', 'state', 'unit', 'item_number'"
                )

        query_url = f"{self._base_url}/server/odata/Part"

        converted_metadata = json.dumps(metadata)

        query_response = requests.post(
            url=query_url,
            headers=self._headers_auth,
            data=converted_metadata
        )

        return query_response.json()

    def update_part(self, part_id, metadata):
        """
        Updates metadata for an existing part in the database.

        Parameters
        ----------
        part_id: str
            unique id number that is assigned to the part when it's initially
            created. Not to be confused with item_number, which is the
            manufacturer's part number.

        metadata: dict
            dictionary of metadata entries to be updated for the assigned part.
        """
        # checks variables are valid
        if not isinstance(part_id, str):
            raise ValueError(
                'Part ID number must be structured as as string.'
            )

        if not isinstance(metadata, dict):
            raise ValueError(
                'metadata must be structured as a key:value pair dictionary'
            )

        valid_keys = [
            'classification',
            'created_on',
            'description',
            'external_owner',
            'generation',
            'keyed_name',
            'name',
            'state',
            'unit',
            'item_number',
            'itemtype',
            'quantity'
        ]

        for key in metadata:
            if key not in valid_keys:
                raise RuntimeError(
                    "Invalid Metadata entry. Valid keys are 'description,"
                    "'name, 'keyed_name', 'state', 'unit', 'item_number'"
                )

        query_url = f"{self._base_url}/server/odata/Part('{part_id}')"

        converted_metadata = json.dumps(metadata)

        query_response = requests.patch(
            url=query_url,
            headers=self._headers_auth,
            data=converted_metadata
        )

        return query_response.json()

    def delete_part(self, part_id):
        """
        Deletes a part from the database.

        Parameters
        ----------
        part_id: str
            unique id number that is assigned to the part when it's initially
            created. Not to be confused with item_number, which is the
            manufacturer's part number.
        """
        # checks if part id is valid
        if not isinstance(part_id, str):
            raise ValueError(
                "part_id must be structured a string."
            )

        # create the query structure
        query_url = f"{self._base_url}/server/odata/Part('{part_id}')"

        query_response = requests.delete(
            url=query_url,
            headers=self._headers_auth
        )

        return query_response

    def get_assembly(self, part_id):
        """
        Return a list of dicts for children of a part.

        Parameters
        ----------
        part_id: str
            unique id number that is assigned to the part when it's initially
            created. Not to be confused with item_number, which is the
            manufacturer's part number.
        """
        # checks part id is valid
        if not isinstance(part_id, str):
            raise ValueError(
                "part_id must be a string"
            )

        # constructs the query
        query_url = (
            f"{self._base_url}/server/odata/Part('{part_id}')"
            "/Part BOM?$expand=related_id"
        )

        query_response = requests.get(
            url=query_url,
            headers=self._headers_auth
        )

        return query_response.json()

    def _recurse_product_structure(self, parent_id, assembly_dict):
        """Recursively use get_assembly to get a product structure."""
        children = assembly_dict['value']

        for child in children:
            child_id = child['related_id']['id']
            self.product_structure[parent_id]['children'].append(child_id)

            self.product_structure[child_id] = {
                'parent': parent_id,
                'children': []
            }
            child_assembly_level = self.get_assembly(
                part_id=child_id,
                authorization=self._authorization
            )
            self._recurse_product_structure(
                parent_id=child_id,
                assembly_dict=child_assembly_level
            )

    def create_assembly(self, item_number, assembly_name, metadata):
        """
        Creates an assembly, including the parent assembly and child parts.

        Parameters
        ----------
        parent_part: str
            the name of the parent part.

        metadata: list
            list of structured dictionaries to assign to the assembly.
            list should be structured as follows:
                [{
                    'related_id': {
                        'item_number': {universal document number of child}
                },
                {
                    'related_id': {
                         'item_number': {universal document number of child}
                    }
                }]

            Additional information can be added, item_number is a mandatory
            parameter. Each child part requires it's own 'related_id' entry
        """
        # checks variable is valid
        if not isinstance(metadata, list):
            raise ValueError(
                "metadata must be a formatted list of dictionaries."
            )

        # construct the query
        query_url = f"{self._base_url}/server/odata/Part"

        query_body = {
            'item_number': item_number,
            'name': assembly_name,
            'PART BOM': metadata
        }

        converted_metadata = json.dumps(query_body)

        query_response = requests.post(
            url=query_url,
            headers=self._headers_auth,
            data=converted_metadata
        )

        return query_response.json()

    def link_child_part(self, assembly_id, child_part):
        """
        Adds children parts onto an existing assembly.

        Parameters
        ----------
        assembly_id: str
            The ID number of the assembly being updated.

        child_parts: list
            ID Number of the existing part being attached to the parent.
        """
        if not isinstance(assembly_id, str):
            raise ValueError("assembly_id must be a string.")

        if not isinstance(child_part, str):
            raise ValueError("child_parts must be a string.")

        child_request = {
            "source_id@odata.bind": f"Part('{assembly_id}')",
            "related_id@odata.bind": f"BOM('{child_part}')"
        }

        query_url = (f"{self._base_url}/server/odata/Part BOM")

        converted_metadata = json.dumps(child_request)

        query_response = requests.post(
            url=query_url,
            headers=self._headers_auth,
            data=converted_metadata
        )

        return query_response.json()

    def search_linked_CAD_files(self, part_id):
        """
        Searches a part for CAD documents attached to the part.

        Parameters
        ----------
        part_id: str
            unique ID number for the part
        """
        if not isinstance(part_id, str):
            raise ValueError(
                "part_id must be formatted as a string"
            )

        query_url = (
            f"{self._base_url}/server/odata/Part('{part_id}')"
            "/Part CAD?$expand=related_id"
        )

        query_response = requests.get(
            url=query_url,
            headers=self._headers_auth
        )

        return query_response.json()

    def link_CAD_document(self, part_id, CAD_id):
        """
        Links a CAD Document to a part.

        Parameters
        ----------
        part_id: str
            the ID number of the parent part CAD is being attached to.

        CAD_number: str
            the filename of the CAD file being linked.
        """
        if not isinstance(part_id, str):
            raise ValueError(
                "part_id must be formatted as a string"
            )

        if not isinstance(CAD_id, str):
            raise ValueError(
                "CAD_id must be formatted as a string"
            )

        query_url = (
            f"{self._base_url}/server/odata/Part('{part_id}')/Part CAD"
        )

        metadata = {
            'related_id@odata.bind': f"CAD('{CAD_id})"
        }

        converted_metadata = json.dumps(metadata)

        query_response = requests.post(
            url=query_url,
            headers=self._headers_auth,
            data=converted_metadata
        )

        return query_response.json()
