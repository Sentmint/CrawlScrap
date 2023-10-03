import json
import os

def getConfig():
    try:
        config_val = os.environ.get("REDDIT_CONFIG")
        config = json.loads(config_val)
        return config

    except Exception as e:
        print("Error encountered when reading config file: ", e)
        return None