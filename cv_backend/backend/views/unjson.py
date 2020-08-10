import json
from collections import namedtuple


#  将Json格式的数据转化成Object
def UnJson(jsonData):
    json_str = json.dumps(jsonData)
    data = json.loads(json_str, object_hook=lambda d: namedtuple('data', d.keys())(*d.values()))
    return data