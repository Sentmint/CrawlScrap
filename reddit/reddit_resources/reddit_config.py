import json
import os

def getConfig():
    try:
        config_path = os.path.join(os.path.dirname(__file__), 'reddit_config.json')
        with open(config_path) as config:
            data = json.load(config)
            return data
    except:
        print("Error encountered when reading config file.")
        return None