import json

def getConfig():
    try:
        with open('reddit/reddit_resource/reddit_config.json') as config:
            data = json.load(config)
            return data
    except:
        print("Error encountered when reading config file.")
        return None