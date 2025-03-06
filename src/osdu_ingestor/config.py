import json
import toml
import yaml
from os.path import exists
import os

class Config:
    _instance = None
    def __init__(self):
        raise RuntimeError("Call instance() instead")
    
    @classmethod
    def instance(cls, config_file=None):
        path = config_file
        if path is None:
            path = os.environ.get("CONFIG_PATH", None)            
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            cls._instance._initialize(path)
        return cls._instance
    
    def _initialize(self, config_file=None):
        try:
            self.config_file = os.environ.get("CONFIG_PATH")
            if self.config_file is None:
                for ext in [".yaml", ".toml", ".json"]:
                    if exists(f"config{ext}"):
                        self.config_file = f"config{ext}"
                        print(f"Use config {ext}" )
                        break
        
            if self.config_file and exists(self.config_file):
                self.load_config()
            else:
                raise FileNotFoundError("No valid config found!")
        except FileNotFoundError as e:
            print(f"Error: {e}")
            self.config_data = {}

    def load_config(self):
        if self.config_file.lower().endswith(".json"):
            try:
                with open(self.config_file, "r") as file:
                    self.config_data = json.load(file)
            except json.JSONDecodeError:
                print("Error: Invalid JSON format in config file. Using default values.")

        elif self.config_file.lower().endswith(".toml"):
            try:
                with open(self.config_file, "r") as file:
                    config_raw_data = toml.load(file)
                    self.config_data = config_raw_data.get("minio",{})
            except toml.TomlDecodeError:
                print("Errot: Invalid TOML format in config file. Using default values")

        elif self.config_file.lower().endswith(".yaml"):
            try:
                with open(self.config_file, "r") as file:
                    self.config_data = yaml.safe_load(file)
            except yaml.parser.ParserError:
                print("Error: Invalid YAML format in config file. Using default values")

        else:
            print("Config file not found.")
    
    def get(self, key, default=None):
        return self.config_data.get(key,default)









