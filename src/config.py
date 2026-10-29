import json
from models import Config, LevelConfig


class ConfigParser:
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

    def keys(self):
        try:
            config = self.config.copy()
            if "levels" in config.keys():
                raise ValueError("[CONFIG ERROR]: Levels KEY Error")
            levels = config.pop("levels", None)
            Config(**self.config)
            for level in levels:
                LevelConfig(**level)
        except BaseException as error:
            print(f"{error}")
            exit()
