import os
import pandas as pd


class TransferPipeline:
    """
    Class to encapsulate methods to transfer data from the hyperthought
    environment to the Aras Innovator environment.
    """
    def __init__(self, aras_parts_api, aras_files_api, ht_api, bom_file,
                 space_id, path=None):
        self.ht_api = ht_api
        self.space_id = space_id
        self.path = path
        self.bom_file = bom_file
        self.aras_parts_api = aras_parts_api
        self.aras_files_api = aras_files_api
        parts_list = ht_api.get_all_from_location(space_id, path)
        self.refined_parts_list = []
        for part in parts_list:
            if part['ftype'] == 'SLDASM' or part['ftype'] == 'SLDPRT':
                self.refined_parts_list.append(part)

    def _capture_component_metadata(self, part_pk):
        """
        Captures metadata of a file to use for the creation of a part in
        the Aras space.

        Parameters
        ----------
        part_pk: str
            the pk of the file in hyperthought
        """
        part = self.ht_api.get_document(part_pk)

        for entry in part['metadata']:
            if entry['keyName'] == 'PART NUMBER':
                part_name = entry['value']['link']
            if entry['keyName'] == 'ITEM NO.':
                part_number = entry['value']['link']

        metadata = {
            'item_number': part_number,
            'name': part_name
        }

        self.aras_parts_api.create_part(metadata)

    def _capture_subassembly_metadata(self, part_pk):
        """
        Uses hyperthought data to encapsulate all pertinent data and create
        an assembly in the Aras environment.

        Parameters
        ----------
        part_pk: str
            the pk of the file in hyperthought
        """
        part = self.ht_api.get_document(part_pk)
        for item in part['metadata']:
            if item['keyName'] == 'ITEM NO.':
                assembly_number = item['value']['link']
            if item['keyName'] == 'PART NUMBER':
                part_name = item['value']['link']

        number_list = {}
        for part in self.refined_parts_list:
            for item in part['metadata']:
                if item['keyName'] == 'ITEM NO.':
                    number_list[part['name']] = item['value']['link']

        formatted_list = []
        children_parts = []
        for item in self.refined_parts_list:
            for entry in item['metadata']:
                if entry['keyName'] == 'ITEM NO.':
                    if (
                        int(entry['value']['link']) == assembly_number and
                        entry['value']['link'] != assembly_number
                    ):
                        children_parts.append(item)
        for item in children_parts:
            for entry in item['metadata']:
                if entry['keyName'] == 'ITEM NO.':
                    item_no = entry['value']['link']
                if entry['keyName'] == 'QTY.':
                    quant = entry['value']['link']
                if entry['keyName'] == 'PART NUMBER':
                    part_number = entry['value']['link']
            formatted_list.append(
                {
                    'quantity': quant,
                    'related_id':
                        {
                            'item_number': item_no,
                            'name': part_number
                        }
                }
            )

        self.aras_parts_api.create_assembly(
            item_number=assembly_number,
            assembly_name=part_name,
            metadata=formatted_list
        )

    def _upload_hyperthought_files(self):
        """
        Downloads files located in the hyperthought space to the local machine
        and then uploads them to the Aras space.
        """
        user = os.getlogin()

        new_folder = f"C:/Users/{user}/Downloads/temporary_aras_files"

        if not os.path.exists(new_folder):
            os.makedirs(new_folder)

        file_pks = [file['pk'] for file in self.refined_parts_list]

        for file in file_pks:
            self.ht_api.download(
                file_id=file,
                directory=new_folder
            )

        local_files = os.listdir(new_folder)

        # creates an item number/filename relationship list
        file_dirs = []
        df = pd.read_excel(self.bom_file)
        for file in local_files:
            for i in range(len(df['PART NUMBER'])):
                if file.split('.')[0] == df['PART NUMBER'][i]:
                    file_dirs.append(
                        {
                            'item number': df['ITEM NO.'][i],
                            'file_number': file
                        }
                    )

        updated_local_files = []
        for pair in file_dirs:
            updated_local_files.append(
                {
                    'item number': pair['item number'],
                    'file_number': f"{new_folder}/{pair['file_number']}"
                }
            )

        # uploads the files in the list
        for pair in updated_local_files:
            self.aras_files_api.upload_file(
                file_path=pair['file_number'],
                file_number=str(pair['item number'])
            )

    def _link_files_to_parts(self):
        """
        Links the newly created parts to the newly uploaded CAD files.
        """
        print('Creating lists for pairing')
        file_list = self.aras_files_api.get_file_list()
        parts_list = self.aras_parts_api.get_parts_list()

        part_file_pairs = []

        print('Pairing files')
        for file in file_list['value']:
            for part in parts_list['value']:
                if file['filename'].split('.')[0] == part['name']:
                    part_file_pairs.append(
                        {
                            'file_id': file['id'],
                            'part_id': part['id']
                        }
                    )

        print('Pairing files to parts.')
        for pair in part_file_pairs:
            self.aras_parts_api.link_CAD_document(
                part_id=pair['part_id'],
                CAD_number=pair['file_id']
            )
        print('Pairing Process Completed.')

    def create_parts_from_metadata(self):
        """
        Uses metadata from a list of hyperthought files to create parts
        in the Aras space.
        """
        for part in self.refined_parts_list:
            for entry in part['metadata']:
                if entry['keyName'] == 'ITEM TYPE':
                    if entry['value']['link'] == 'Component':
                        self._capture_component_metadata(part['pk'])
                    if entry['value']['link'] == 'SubAssembly':
                        self._capture_subassembly_metadata(part['pk'])
                    if entry['value']['link'] == 'SubComponent':
                        pass

        self._upload_hyperthought_files()
        self._link_files_to_parts()
