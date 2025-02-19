import json
from types import SimpleNamespace

class ConfigMaster:

    def __init__(self, config_file : str):
        self.config_file = config_file
        with open(self.config_file,"r",encoding="utf-8") as config:
            try:
                self.config_data = json.load(config)
            except json.JSONDecodeError as err:
                raise

    def get_fuzzers(self):

        

   # def validate_config(self):
    #    self._

    #def _validate_fuzzer

