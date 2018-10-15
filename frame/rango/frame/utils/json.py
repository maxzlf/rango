import enum
import json
import datetime
from uuid import UUID



class JsonEncoder(json.JSONEncoder):


    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        elif isinstance(obj, enum.Enum):
            return obj.value
        elif isinstance(obj, UUID):
            return obj.hex
        else:
            return json.JSONEncoder.default(self, obj)
