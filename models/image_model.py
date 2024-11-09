# image_model.py: 画像データとクロップ範囲情報の管理
from PIL import Image
from utils.image_utils import open_image, crop_image
from collections import deque
import os

class ImageModel:
    def __init__(self, file_path):
        self.file_path = file_path
        self.image_data = None
        self.crop_rectangle = None
        self.background_color = '#FFFFFF'
        self.crop_count = 0  # 同じ画像内での保存用カウンター
        self.load_image()

    def load_image(self):
        self.image_data = open_image(self.file_path)

    def increment_crop_count(self):
        self.crop_count += 1