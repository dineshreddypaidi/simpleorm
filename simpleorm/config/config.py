import json
from urllib.parse import urlparse

def load_json_config(file_path) -> dict:
    with open(file_path, "r") as f:
        return json.load(f)
    
def load_from_url(db_url) -> dict:
    config = {}
    
    parsed_url = urlparse(db_url)
    
    config['engine'] = parsed_url.scheme
    config['user'] = parsed_url.username
    config["password"] = parsed_url.password
    config["host"] = parsed_url.hostname
    config["database"] = parsed_url.path.lstrip('/')
    
    return config