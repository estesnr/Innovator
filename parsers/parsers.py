from hyperthought.metadata import MetadataItem
import math
import os
import pandas as pd
import uuid


class Aras_Parsers():

    def parse_sldwrks(self, file_pk):
        """
        Uses name of the file to relate information as metadata based on an
        imported spreadsheet that outlines relationship data.
        """

        df = pd.read_excel(self.spreadsheet)
        file = self.files_api.get_document(file_pk)
        file_name = file['name']

        id_number = str(uuid.uuid4())
        id_number = ''.join(id_number.split('-'))

        # creates a dictionary of values to compare against filenames
        val_list = []
        for i in range(len(df)):
            exp_dict = {}
            for key in df:
                if type(df[key][i]) != str:
                    if math.isnan(df[key][i]):
                        exp_dict[str(key)] = 'NaN'
                    else:
                        exp_dict[str(key)] = float(df[key][i])
                else:
                    exp_dict[str(key)] = df[key][i].replace('\n', '').strip()
            if exp_dict not in val_list:
                val_list.append(exp_dict)

        reverse_val_list = (
            sorted(val_list, key=lambda v: v['ITEM NO.'], reverse=True)
        )

        prev = None

        # searches for parent/child assembly relationships
        for val in reverse_val_list:
            part_num = val['ITEM NO.']

            # if the part number is not the same
            # as its integer
            if (part_num != int(part_num)):
                val['ITEM TYPE'] = 'SubComponent'
            # else if the previous part as an int
            # equals the current value as an int
            elif (prev == int(part_num)):
                val['ITEM TYPE'] = 'SubAssembly'
            # the previous and current values
            # are different entirely
            else:
                val['ITEM TYPE'] = 'Component'

            prev = int(part_num)

        # print(val_list)
        metadata = []
        for val in val_list:
            if val['PART NUMBER'] == file_name.split('.')[0]:
                for key, value in val.items():
                    metadata.append(MetadataItem(key, value))
            elif len(val['PART NUMBER'].split('/')) == 2:
                if val['PART NUMBER'].split('/')[1] == file_name.split('.')[0]:
                    for key, value in val.items():
                        metadata.append(MetadataItem(key, value))
            else:
                pass

        metadata.append(MetadataItem('id_number', id_number))

        self.files_api.update_metadata(file_pk, metadata)

    def parse(self):
        VALID_EXTENSIONS = [
            'SLDPRT',
            'SLDASM'
        ]

        file = self.files_api.get_document(self.file_pk)
        file_name = file['name']

        file_extension = os.path.splitext(file_name)[1].lstrip('.')

        if file_extension in VALID_EXTENSIONS:
            self.parse_sldwrks(self.file_pk)

    def __init__(self, files_api, file_pk, spreadsheet):

        self.files_api = files_api
        self.file_pk = file_pk
        self.spreadsheet = spreadsheet
