import os
import sys
import json

class ConfigManager():
    def __init__(self, cfg_file, default_cfg_file):
        # default_config.json
        # config.json
        self.cfg_file = cfg_file
        self.default_cfg_file = default_cfg_file

        self.load_default_cfg(self.default_cfg_file)
        self.load_current_cfg(self.cfg_file)

        self.NEW_CONFIG = self.CURRENT_CONFIG


    def load_default_cfg(self, default_cfg_file):
        with open(default_cfg_file) as df_cfg_file:
            default_config = json.load(df_cfg_file)

        self.DEFAULT_CONFIG = default_config


    def load_current_cfg(self, current_cfg_file):
        with open(current_cfg_file) as current_cfg_file:
            current_config = json.load(current_cfg_file)
        
        self.CURRENT_CONFIG = current_config


    def show_current_cfg(self):
        self.load_current_cfg(self.cfg_file)
        print('Current settings in config file: {}'.format(self.cfg_file))
        for key, value in self.CURRENT_CONFIG.items():
             print('{}: {}'.format(key, value))


    def preview_changes(self):
        print('Changes:')
        for key, value in self.CURRENT_CONFIG.items():
            if self.CURRENT_CONFIG[key] != self.NEW_CONFIG[key]:
                print('{}: {} --> {}'.format(key, value, self.NEW_CONFIG[key]))


    def save_config(self):
        with open(self.cfg_file, 'w') as outfile:
            json.dump(self.NEW_CONFIG, outfile, indent=4)
        self.load_current_cfg(self.cfg_file)

