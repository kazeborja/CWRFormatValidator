from models.records import *

__author__ = 'Borja'


class Validator(object):

    def __init__(self):
        self._records = []

    def validate_document_format(self, document_json):
        """
        Validate an entire document record by record, checking if they are well formed
        :param document_json: Expected an array representing the document records
        :return: Both arrays, first one containing the valid records and second one with the failures
        """
        valid_records = []
        invalid_records = []

        for record in document_json:
            record_object = Record.factory(record)

            if record_object.check_format_with_regex():
                valid_records.append(record)
            else:
                invalid_records.append(record)

            self._records.append(record)

        return valid_records, invalid_records
