__author__ = 'Borja'
import abc
import re
import regex


class Record(object):
    __metaclass__ = abc.ABCMeta

    # Field regex are the regular expressions used to identify every field within the record
    FIELD_REGEX = []

    def __init__(self, record):
        if record is None or record == '':
            raise ValueError("Record can't be None")

        # Raw record identifies the record String
        self._raw_record = record

        # The final regex and the size it has
        self._regex, self._regex_size = self._generate_regex()

        # Whether a record is rejected or not
        self._rejected = False

    @staticmethod
    def factory(record):
        record_type = record[0:3]

        if record_type == 'AGR':
            record_object = AgreementRecord(record)
        elif record_type == 'ALT':
            record_object = WorkAlternativeTitleRecord(record)
        elif record_type == 'ARI':
            record_object = WorkAdditionalInfoRecord(record)
        elif record_type == 'COM':
            record_object = WorkCompositeRecord(record)
        elif record_type == 'EWT':
            record_object = WorkExcerptTitle(record)
        elif record_type == 'GRH':
            record_object = GroupHeaderRecord(record)
        elif record_type == 'GRT':
            record_object = GroupTrailerRecord(record)
        elif record_type == 'HDR':
            record_object = TransmissionHeaderRecord(record)
        elif record_type == 'IND':
            record_object = InstrumentationDetailRecord(record)
        elif record_type == 'INS':
            record_object = InstrumentationSummaryRecord(record)
        elif record_type == 'IPA':
            record_object = InterestedPartyRecord(record)
        elif record_type == 'NAT':
            record_object = NRWorkTitleRecord(record)
        elif record_type in ['NCT', 'NET', 'NVT']:
            record_object = NRSpecialTitleRecord(record)
        elif record_type == 'NOW':
            record_object = NROtherWriterRecord(record)
        elif record_type == 'NPA':
            record_object = NRAgreementPartyNameRecord(record)
        elif record_type == 'NPN':
            record_object = NRPublisherNameRecord(record)
        elif record_type == 'NPR':
            record_object = NRPerformanceDataRecord(record)
        elif record_type == 'NWN':
            record_object = NRWriterNameRecord(record)
        elif record_type in ['NWR', 'REV']:
            record_object = RegistrationRecord(record)
        elif record_type == 'ORN':
            record_object = WorkOriginRecord(record)
        elif record_type == 'PER':
            record_object = PerformingArtistRecord(record)
        elif record_type == 'PWR':
            record_object = WriterAgentRecord(record)
        elif record_type == 'REC':
            record_object = RecordingDetailRecord(record)
        elif record_type == 'SPT':
            record_object = PublisherTerritoryRecord(record)
        elif record_type in ['SPU', 'OPU']:
            record_object = PublisherControlRecord(record)
        elif record_type in ['SWR', 'OWR']:
            record_object = WriterControlRecord(record)
        elif record_type == 'SWT':
            record_object = WriterTerritoryRecord(record)
        elif record_type == 'TER':
            record_object = TerritoryRecord(record)
        elif record_type == 'TRL':
            record_object = TransmissionTrailerRecord(record)
        elif record_type == 'VER':
            record_object = WorkVersionTitle(record)
        else:
            raise ValueError('Wrong record creation, obtained type: {}'.format(record_type))

        return record_object

    @property
    def rejected(self):
        return self._rejected

    def check_format_with_regex(self):
        """
        Checks if a given record fulfill the regular expression requirements for it's kind
        :return: True if the regular expression matches, false otherwise
        """
        matcher = re.compile(self._regex)

        if not matcher.match(self._raw_record[0:self._regex_size]):
            self._rejected = True

        return not self._rejected

    def _generate_regex(self):
        """
        Compose the regular expression, as well as it's size
        :return: The composed regular expression, The size of it
        """
        regex_string = '^' + "".join(str(regular_expression) for regular_expression in self.FIELD_REGEX) + '$'
        regex_size = sum(regular_expression.size for regular_expression in self.FIELD_REGEX)

        return regex_string, regex_size

    def __str__(self):
        return self._raw_record

    def __repr__(self):
        return self.__str__()


class AviKey(object):
    SOCIETY_CODE = regex.get_numeric_regex(3, True)
    NUMBER = regex.get_ascii_regex(15, True)

    REGEX = regex.Regex('{}{}'.format(SOCIETY_CODE, NUMBER), 18)

    def __init__(self, avikey=None):
        self.society_code = int(avikey[0:3])
        self.number = avikey[3:18]


class RecordPrefix(object):
    RECORD_TYPE = regex.get_alpha_regex(3)
    TRANSACTION_NUMBER = regex.get_numeric_regex(8)
    RECORD_NUMBER = regex.get_numeric_regex(8)

    REGEX = regex.Regex('{}{}{}'.format(RECORD_TYPE, TRANSACTION_NUMBER, RECORD_NUMBER), 19)

    def __init__(self, prefix=None):
        self.record_type = prefix[0:3]
        self.transaction_number = int(prefix[3:11])
        self.record_number = int(prefix[11:19])

    def __str__(self):
        return "'Record type': {}, 'Transaction number': {}, 'Record number': {}".format(
            self.record_type, self.transaction_number, self.record_number)

    def __repr__(self):
        return self.__str__()


class SocietyAffiliation(object):
    REGEX = regex.get_numeric_regex(1, True) + regex.get_numeric_regex(1, True) + regex.get_numeric_regex(1, True)


class VIsan(object):
    VERSION = regex.get_numeric_regex(8, True)
    ISAN = regex.get_numeric_regex(12, True)
    EPISODE = regex.get_numeric_regex(4, True)
    CHECK_DIGIT = regex.get_numeric_regex(1, True)

    REGEX = regex.Regex('{}{}{}{}'.format(
        VERSION, ISAN, EPISODE, CHECK_DIGIT), 25)

    def __init__(self, visan=None):
        self.version = int(visan[0:7])
        self.isan = int(visan[7:19])
        self.episode = int(visan[19:23])
        self.check_digit = int(visan[23:24])


class AgreementRecord(Record):
    FIELD_REGEX = [RecordPrefix.REGEX,
                   regex.get_alphanumeric_regex(14),
                   regex.get_alphanumeric_regex(14, True),
                   regex.get_alpha_regex(2),
                   regex.get_date_regex(),
                   regex.get_date_regex(True),
                   regex.get_date_regex(True),
                   regex.get_defined_values_regex(1, False, 'A', 'D', 'N'),
                   regex.get_date_regex(True),
                   regex.get_defined_values_regex(1, False, 'D', 'N', 'O'),
                   regex.get_date_regex(True),
                   regex.get_date_regex(True),
                   regex.get_numeric_regex(5),
                   regex.get_defined_values_regex(1, True, 'N', 'S'),
                   regex.get_boolean_regex(True),
                   regex.get_boolean_regex(True),
                   regex.get_alphanumeric_regex(14, True)]

    def __init__(self, record):
        super(AgreementRecord, self).__init__(record)


class GroupHeaderRecord(Record):
    FIELD_REGEX = [regex.get_defined_values_regex(3, False, 'GRH'),
                   regex.get_defined_values_regex(3, False, 'AGR', 'NWR', 'REV'),
                   regex.get_numeric_regex(5),
                   regex.get_defined_values_regex(5, False, '02\.10'),
                   regex.get_numeric_regex(10, True),
                   regex.get_optional_regex(2)]

    def __init__(self, record):
        super(GroupHeaderRecord, self).__init__(record)


class GroupTrailerRecord(Record):
    FIELD_REGEX = [regex.get_defined_values_regex(3, False, 'GRT'),
                   regex.get_numeric_regex(5),
                   regex.get_numeric_regex(8),
                   regex.get_numeric_regex(8),
                   regex.get_alpha_regex(3, True),
                   regex.get_numeric_regex(10, True)]

    def __init__(self, record):
        super(GroupTrailerRecord, self).__init__(record)


class InstrumentationDetailRecord(Record):
    FIELD_REGEX = [RecordPrefix.REGEX, regex.get_alpha_regex(3), regex.get_numeric_regex(3, True)]

    def __init__(self, record):
        super(InstrumentationDetailRecord, self).__init__(record)


class InstrumentationSummaryRecord(Record):
    FIELD_REGEX = [RecordPrefix.REGEX,
                   regex.get_numeric_regex(3, True),
                   regex.get_ascii_regex(3, True),
                   regex.get_ascii_regex(50, True)]

    def __init__(self, record):
        super(InstrumentationSummaryRecord, self).__init__(record)


class InterestedPartyRecord(Record):
    FIELD_REGEX = [RecordPrefix.REGEX,
                   regex.get_alpha_regex(2),
                   regex.get_ascii_regex(11, True),
                   regex.get_numeric_regex(13, True),
                   regex.get_ascii_regex(9),
                   regex.get_ascii_regex(45),
                   regex.get_ascii_regex(30, True),
                   SocietyAffiliation.REGEX,
                   regex.get_numeric_regex(5),
                   SocietyAffiliation.REGEX,
                   regex.get_numeric_regex(5),
                   SocietyAffiliation.REGEX,
                   regex.get_numeric_regex(5)]

    def __init__(self, record):
        super(InterestedPartyRecord, self).__init__(record)


class NRAgreementPartyNameRecord(Record):
    FIELD_REGEX = [RecordPrefix.REGEX,
                   regex.get_ascii_regex(9),
                   regex.get_non_roman_regex(160),
                   regex.get_non_roman_regex(160),
                   regex.get_alpha_regex(2, True)]

    def __init__(self, record):
        super(NRAgreementPartyNameRecord, self).__init__(record)


class NROtherWriterRecord(Record):
    FIELD_REGEX = [RecordPrefix.REGEX,
                   regex.get_ascii_regex(160),
                   regex.get_ascii_regex(160),
                   regex.get_alpha_regex(2, True),
                   regex.get_alpha_regex(1, True)]

    def __init__(self, record):
        super(NROtherWriterRecord, self).__init__(record)


class NRPerformanceDataRecord(Record):
    FIELD_REGEX = [RecordPrefix.REGEX,
                   regex.get_ascii_regex(160, True),
                   regex.get_ascii_regex(160, True),
                   regex.get_ascii_regex(11, True),
                   regex.get_ascii_regex(13, True),
                   regex.get_alpha_regex(2, True),
                   regex.get_alpha_regex(2, True),
                   regex.get_alpha_regex(3, True)]

    def __init__(self, record):
        super(NRPerformanceDataRecord, self).__init__(record)


class NRPublisherNameRecord(Record):
    FIELD_REGEX = [RecordPrefix.REGEX,
                   regex.get_numeric_regex(2),
                   regex.get_ascii_regex(9),
                   regex.get_ascii_regex(480),
                   regex.get_alpha_regex(2, True)]

    def __init__(self, record):
        super(NRPublisherNameRecord, self).__init__(record)


class NRSpecialTitleRecord(Record):
    FIELD_REGEX = [RecordPrefix.REGEX,
                   regex.get_ascii_regex(640),
                   regex.get_alpha_regex(2, True)]

    def __init__(self, record):
        super(NRSpecialTitleRecord, self).__init__(record)


class NRWorkTitleRecord(Record):
    FIELD_REGEX = [RecordPrefix.REGEX,
                   regex.get_ascii_regex(640),
                   regex.get_ascii_regex(2),
                   regex.get_alpha_regex(2, True)]

    def __init__(self, record):
        super(NRWorkTitleRecord, self).__init__(record)


class NRWriterNameRecord(Record):
    FIELD_REGEX = [RecordPrefix.REGEX,
                   regex.get_ascii_regex(9),
                   regex.get_ascii_regex(160),
                   regex.get_ascii_regex(160),
                   regex.get_alpha_regex(2, True)]

    def __init__(self, record):
        super(NRWriterNameRecord, self).__init__(record)


class PerformingArtistRecord(Record):
    FIELD_REGEX = [RecordPrefix.REGEX,
                   regex.get_ascii_regex(45),
                   regex.get_ascii_regex(30, True),
                   regex.get_ascii_regex(11, True),
                   regex.get_ascii_regex(13, True)]

    def __init__(self, record):
        super(PerformingArtistRecord, self).__init__(record)


class PublisherControlRecord(Record):
    FIELD_REGEX = [RecordPrefix.REGEX,
                   regex.get_numeric_regex(2),
                   regex.get_ascii_regex(9, True),
                   regex.get_ascii_regex(45, True),
                   regex.get_flag_regex(True),
                   regex.get_alpha_regex(1, True) + regex.get_alpha_regex(1, True),
                   regex.get_ascii_regex(9, True),
                   regex.get_numeric_regex(11, True),
                   regex.get_ascii_regex(14, True),
                   SocietyAffiliation.REGEX,
                   regex.get_numeric_regex(5, True),
                   SocietyAffiliation.REGEX,
                   regex.get_numeric_regex(5, True),
                   SocietyAffiliation.REGEX,
                   regex.get_numeric_regex(5, True),
                   regex.get_flag_regex(True),
                   regex.get_flag_regex(True),
                   regex.get_optional_regex(1),
                   regex.get_ascii_regex(13, True),
                   regex.get_ascii_regex(14, True),
                   regex.get_ascii_regex(14, True),
                   regex.get_alpha_regex(2, True),
                   regex.get_alpha_regex(1, True)]

    def __init__(self, record):
        super(PublisherControlRecord, self).__init__(record)


class PublisherTerritoryRecord(Record):
    FIELD_REGEX = [RecordPrefix.REGEX,
                   regex.get_ascii_regex(9),
                   regex.get_optional_regex(6),
                   regex.get_numeric_regex(5, True),
                   regex.get_numeric_regex(5, True),
                   regex.get_numeric_regex(5, True),
                   regex.get_defined_values_regex(1, False, 'E', 'I'),
                   regex.get_numeric_regex(4),
                   regex.get_boolean_regex(),
                   regex.get_numeric_regex(3)]

    def __init__(self, record):
        super(PublisherTerritoryRecord, self).__init__(record)


class RecordingDetailRecord(Record):
    FIELD_REGEX = [RecordPrefix.REGEX,
                   regex.get_date_regex(True),
                   regex.get_optional_regex(60),
                   regex.get_time_regex(True),
                   regex.get_optional_regex(5),
                   regex.get_ascii_regex(60, True),
                   regex.get_ascii_regex(60, True),
                   regex.get_ascii_regex(18, True),
                   regex.get_ascii_regex(13, True),
                   regex.get_ascii_regex(12, True),
                   regex.get_alpha_regex(1, True),
                   regex.get_alpha_regex(1, True),
                   regex.get_ascii_regex(3, True)]

    def __init__(self, record):
        super(RecordingDetailRecord, self).__init__(record)


class RegistrationRecord(Record):
    FIELD_REGEX = [RecordPrefix.REGEX,
                   regex.get_ascii_regex(60),
                   regex.get_alpha_regex(2, True),
                   regex.get_ascii_regex(14),
                   regex.get_ascii_regex(11, True),
                   regex.get_date_regex(True),
                   regex.get_ascii_regex(12, True),
                   regex.get_alpha_regex(3),
                   regex.get_time_regex(True),
                   regex.get_flag_regex(),
                   regex.get_alpha_regex(3, True),
                   regex.get_alpha_regex(3, True),
                   regex.get_alpha_regex(3),
                   regex.get_alpha_regex(3, True),
                   regex.get_alpha_regex(3, True),
                   regex.get_alpha_regex(3, True),
                   regex.get_ascii_regex(30, True),
                   regex.get_ascii_regex(10, True),
                   regex.get_alpha_regex(2, True),
                   regex.get_boolean_regex(True),
                   regex.get_numeric_regex(3, True),
                   regex.get_date_regex(True),
                   regex.get_flag_regex(True),
                   regex.get_ascii_regex(25, True),
                   regex.get_ascii_regex(25, True),
                   regex.get_flag_regex(True)]

    def __init__(self, record):
        super(RegistrationRecord, self).__init__(record)


class TerritoryRecord(Record):
    FIELD_REGEX = [RecordPrefix.REGEX,
                   regex.get_defined_values_regex(1, False, 'E', 'I'),
                   regex.get_numeric_regex(4)]

    def __init__(self, record):
        super(TerritoryRecord, self).__init__(record)


class TransmissionHeaderRecord(Record):

    FIELD_REGEX = [regex.get_defined_values_regex(3, False, 'HDR'),
                   regex.get_alpha_regex(2),
                   regex.get_numeric_regex(9),
                   regex.get_ascii_regex(45),
                   regex.get_defined_values_regex(5, False, '01\.10'),
                   regex.get_date_regex(),
                   regex.get_time_regex(),
                   regex.get_date_regex(),
                   regex.get_alphanumeric_regex(15, True)]

    def __init__(self, record):
        super(TransmissionHeaderRecord, self).__init__(record)


class TransmissionTrailerRecord(Record):
    FIELD_REGEX = [regex.get_defined_values_regex(3, False, 'TRL'),
                   regex.get_numeric_regex(5),
                   regex.get_numeric_regex(8),
                   regex.get_numeric_regex(8)]

    def __init__(self, record):
        super(TransmissionTrailerRecord, self).__init__(record)


class WorkAdditionalInfoRecord(Record):
    FIELD_REGEX = [RecordPrefix.REGEX,
                   regex.get_numeric_regex(3),
                   regex.get_ascii_regex(14, True),
                   regex.get_alpha_regex(3),
                   regex.get_alpha_regex(2, True),
                   regex.get_ascii_regex(160, True)]

    def __init__(self, record):
        super(WorkAdditionalInfoRecord, self).__init__(record)


class WorkAlternativeTitleRecord(Record):
    FIELD_REGEX = [RecordPrefix.REGEX,
                   regex.get_non_roman_regex(60),
                   regex.get_alpha_regex(2),
                   regex.get_alpha_regex(2, True)]

    def __init__(self, record):
        super(WorkAlternativeTitleRecord, self).__init__(record)


class WorkCompositeRecord(Record):
    FIELD_REGEX = [RecordPrefix.REGEX,
                   regex.get_ascii_regex(60),
                   regex.get_ascii_regex(11, True),
                   regex.get_ascii_regex(14, True),
                   regex.get_time_regex(True),
                   regex.get_ascii_regex(45),
                   regex.get_ascii_regex(30, True),
                   regex.get_numeric_regex(11, True),
                   regex.get_ascii_regex(45, True),
                   regex.get_ascii_regex(30, True),
                   regex.get_numeric_regex(11, True),
                   regex.get_numeric_regex(13, True),
                   regex.get_numeric_regex(13, True)]

    def __init__(self, record):
        super(WorkCompositeRecord, self).__init__(record)


class WorkExcerptTitle(Record):
    FIELD_REGEX = [RecordPrefix.REGEX,
                   regex.get_ascii_regex(60),
                   regex.get_ascii_regex(11, True),
                   regex.get_alpha_regex(2, True),
                   regex.get_ascii_regex(45, True),
                   regex.get_ascii_regex(30, True),
                   regex.get_ascii_regex(60, True),
                   regex.get_numeric_regex(11, True),
                   regex.get_numeric_regex(13, True),
                   regex.get_ascii_regex(45, True),
                   regex.get_ascii_regex(30, True),
                   regex.get_numeric_regex(11, True),
                   regex.get_numeric_regex(13, True),
                   regex.get_ascii_regex(14, True)]

    def __init__(self, record):
        super(WorkExcerptTitle, self).__init__(record)


class WorkOriginRecord(Record):
    FIELD_REGEX = [RecordPrefix.REGEX,
                   regex.get_ascii_regex(3),
                   regex.get_ascii_regex(60, True),
                   regex.get_ascii_regex(15, True),
                   regex.get_numeric_regex(4, True),
                   regex.get_ascii_regex(60, True),
                   regex.get_ascii_regex(1, True),
                   VIsan.REGEX,
                   regex.get_ascii_regex(12, True),
                   regex.get_ascii_regex(60, True),
                   regex.get_ascii_regex(20, True),
                   regex.get_numeric_regex(4, True),
                   AviKey.REGEX]

    def __init__(self, record):
        super(WorkOriginRecord, self).__init__(record)


class WorkVersionTitle(Record):
    FIELD_REGEX = [RecordPrefix.REGEX,
                   regex.get_ascii_regex(60),
                   regex.get_ascii_regex(11, True),
                   regex.get_alpha_regex(2, True),
                   regex.get_ascii_regex(45, True),
                   regex.get_ascii_regex(30, True),
                   regex.get_ascii_regex(60, True),
                   regex.get_numeric_regex(11, True),
                   regex.get_numeric_regex(13, True),
                   regex.get_ascii_regex(45, True),
                   regex.get_ascii_regex(30, True),
                   regex.get_numeric_regex(11, True),
                   regex.get_numeric_regex(13, True),
                   regex.get_ascii_regex(14, True)]

    def __init__(self, record):
        super(WorkVersionTitle, self).__init__(record)


class WriterAgentRecord(Record):
    FIELD_REGEX = [RecordPrefix.REGEX,
                   regex.get_ascii_regex(9),
                   regex.get_ascii_regex(45),
                   regex.get_ascii_regex(14, True),
                   regex.get_ascii_regex(14, True),
                   regex.get_ascii_regex(9)]

    def __init__(self, record):
        super(WriterAgentRecord, self).__init__(record)


class WriterControlRecord(Record):
    FIELD_REGEX = [RecordPrefix.REGEX,
                   regex.get_ascii_regex(9, True),
                   regex.get_ascii_regex(45, True),
                   regex.get_ascii_regex(30, True),
                   regex.get_flag_regex(True),
                   regex.get_alpha_regex(1, True) + regex.get_alpha_regex(1, True),
                   regex.get_ascii_regex(9, True),
                   regex.get_numeric_regex(11, True),
                   SocietyAffiliation.REGEX,
                   regex.get_numeric_regex(5, True),
                   SocietyAffiliation.REGEX,
                   regex.get_numeric_regex(5, True),
                   SocietyAffiliation.REGEX,
                   regex.get_numeric_regex(5, True),
                   regex.get_flag_regex(True),
                   regex.get_boolean_regex(True),
                   regex.get_boolean_regex(True),
                   regex.get_optional_regex(1),
                   regex.get_ascii_regex(13, True),
                   regex.get_numeric_regex(12, True),
                   regex.get_alpha_regex(1, True)]

    def __init__(self, record):
        super(WriterControlRecord, self).__init__(record)


class WriterTerritoryRecord(Record):
    FIELD_REGEX = [RecordPrefix.REGEX,
                   regex.get_ascii_regex(9),
                   regex.get_numeric_regex(5, True),
                   regex.get_numeric_regex(5, True),
                   regex.get_numeric_regex(5, True),
                   regex.get_defined_values_regex(1, False, 'E', 'I'),
                   regex.get_numeric_regex(4),
                   regex.get_boolean_regex(),
                   regex.get_numeric_regex(3)]

    def __init__(self, record):
        super(WriterTerritoryRecord, self).__init__(record)