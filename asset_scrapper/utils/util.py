import json
from bson import json_util
def parse_json(data) -> dict:
    """
    Meant to handle BSON and(hopefully) other JSON type data that is coming from MongoDb

    Args:
        data (_type_): _description_

    Returns:
        _type_: _description_
    """
    return json.loads(json_util.dumps(data))