# models/settings_model.py

from utils.file_utils import read_json, write_json
import os

class SettingsModel:
    def __init__(self, settings_file):
        self.settings_file = settings_file
        self.settings = self.load_settings()

    def load_settings(self):
        if os.path.exists(self.settings_file):
            print(f"Loading settings from {self.settings_file}")
            return read_json(self.settings_file)
        else:
            print(f"Settings file not found: {self.settings_file}")
            default_settings = {
                'hotkeys': {
                    'next_image': '<space>',
                    'previous_image': '<Shift-space>',
                    'save_image': '<Control-s>',
                    'ignore_image': '<Control-b>',
                    "corner_mode": "<KeyPress-r>",
                    "center_mode": "<KeyPress-e>",
                    'color_pick_keys': '<KeyPress-s>'
                },
                'background_color': '#FFFFFF',
                "min_image_size": 400,
                'window_size': {
                    'width': 800,
                    'height': 600
                }
            }
            self.save_settings(default_settings)
            return default_settings

    def save_settings(self, settings=None):
        if settings:
            self.settings = settings
        print(f"Saving settings to {self.settings_file}")
        write_json(self.settings_file, self.settings)
