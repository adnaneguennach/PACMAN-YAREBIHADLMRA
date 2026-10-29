import json
from .models import Config, LevelConfig


class ConfigParser:
    def __init__(self):
        self.config = None

    def read_config(self, filename):
        with open(filename, "r", encoding="utf-8") as f:
            content = ""
            for line in f:
                if line.strip().startswith("#"):
                    continue
                if "#" in line:
                    line = line.split("#")[0]
                content += line

            self.config = json.loads(content)
        
        

    def parsing_data(self):
        try:
            self.read_config("config.json")
            config = self.config.copy()
            if not "levels" in config.keys():
                raise ValueError("[CONFIG ERROR]: Levels KEY Error")
            levels = config.pop("levels", None)
            Config(**self.config)
            for level in levels:
                LevelConfig(**level)
            return self.config
        except BaseException as error:
            print(f"{error}")
            exit()
