# file_utils.py: ファイル操作のユーティリティ関数
import json
import os

def create_folder_if_not_exists(path):
    os.makedirs(path, exist_ok=True)

def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def write_json(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
