import codecs
import unittest
from validator import Validator

__author__ = 'Borja'


class DocumentRegexTest(unittest.TestCase):
    def setUp(self):
        self.file_path = 'files/CW1328EMI_059.V21'
        self.validator = Validator()

    def test_wrong_records(self):
        records = [
            'HDRPB226144593EMI MUSICAL SA DE CV                         01.10201308090259112013080A               ',
            'GRHAGD0000102.100130400001  ',
            'TER0000000000000000J2136'
        ]

        valid_record, invalid_records = self.validator.validate_document_format(records)

        self.assertEqual(0, len(valid_record))
        self.assertEqual(len(records), len(invalid_records))

    def test_file(self):
        with codecs.open(self.file_path, encoding='utf-8') as file_utf8:
            document_content = file_utf8.readlines()

            valid_records, invalid_records = self.validator.validate_document_format(document_content)

        self.assertNotEqual(len(valid_records), 0)
        self.assertEqual(len(document_content), len(valid_records))
        self.assertEqual(len(invalid_records), 0)