import json


class Config:
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
            self.config["highscore_filename"]
            self.config["lives"]
            self.config["pacgum"]
            self.config["points_per_pacgum"]
            self.config["points_per_super_pacgum"]
            self.config["points_per_ghost"]
            self.config["level_max_time"]
            self.config["seed"]
            self.config["levels"]
        except BaseException as error:
            print(error)
            exit()

