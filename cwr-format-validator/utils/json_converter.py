import datetime
import json
__author__ = 'Borja'


class JsonConverter():
    def __init__(self):
        self._dt_handler = lambda obj: (obj.isoformat()
                                        if isinstance(obj, datetime.time)
                                        or isinstance(obj, datetime.date)
                                        else obj.__dict__)

    def parse_object(self, python_object):
        json_object = json.dumps(python_object, default=self._dt_handler)

        return json_object
