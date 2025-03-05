import json
import yaml
import toml


def create_toml():
    with open('config.toml', 'r') as f:
        config = toml.load(f)

    config['minio']["MINIO_ENDPOINT"] = "http://192.168.10.56:9000"
    config['minio']["MINIO_ACCESS_KEY"] = "sCipkQ9wAmfrIqYa4z7m"
    config['minio']["MINIO_SECRET_KEY"] = "OBW74C6M9zXC5oYwv9kR3hGi8ojYbrl01zlscAsH"
    config['minio']["MINIO_BUCKET"] = "testing"
    with open('config.toml', 'w') as f:
        toml.dump(config, f)


def create_json():
    parameter_json = {
    "MINIO_ENDPOINT" : "http://192.168.10.56:9000",
    "MINIO_ACCESS_KEY" : "sCipkQ9wAmfrIqYa4z7m",
    "MINIO_SECRET_KEY" : "OBW74C6M9zXC5oYwv9kR3hGi8ojYbrl01zlscAsH",
    "MINIO_BUCKET": "testing"
    }
    json_obj =json.dumps(parameter_json, indent=4)
    with open ('config.json', 'w') as outfile:
        outfile.write(json_obj)

def create_yaml():
    parameter = {
    "MINIO_ENDPOINT" : "http://192.168.10.56:9000",
    "MINIO_ACCESS_KEY" : "sCipkQ9wAmfrIqYa4z7m",
    "MINIO_SECRET_KEY" : "OBW74C6M9zXC5oYwv9kR3hGi8ojYbrl01zlscAsH",
    "MINIO_BUCKET": "testing"
    }
    with open('config.yaml', 'w') as f:
        yaml.dump(parameter, f)



# create_toml()
create_yaml()
create_json()