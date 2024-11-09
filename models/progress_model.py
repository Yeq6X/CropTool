# models/progress_model.py

from utils.file_utils import read_json, write_json
import os

class ProgressModel:
    def __init__(self, progress_file, input_folder, output_folder):
        self.progress_file = progress_file
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.progress_list = self.load_progress()

    def load_progress(self):
        """進捗ファイルからデータを読み込みます。ファイルがなければ空の辞書を返します。"""
        if os.path.exists(self.progress_file):
            return read_json(self.progress_file)
        else:
            return {}

    def save_progress(self):
        """現在の進捗リストを進捗ファイルに書き込みます。"""
        write_json(self.progress_file, self.progress_list)

    def update_status(self, file_name, status, is_discarded=False):
        """
        指定したファイルのステータスと破棄状態を更新し、進捗ファイルを保存します。

        Parameters:
        - file_name (str): 更新するファイル名
        - status (str): ファイルの新しいステータス（例: 'completed', 'incomplete', 'ignored'）
        - is_discarded (bool): ファイルが破棄されたかどうか
        """
        self.progress_list[file_name] = {
            'status': status,
            'is_discarded': is_discarded
        }
        self.save_progress()

    def sync_with_files(self, file_list):
        """
        ファイルリストと進捗リストを同期し、削除されたファイルには破棄フラグを設定し、新しいファイルは未完了で追加します。

        Parameters:
        - file_list (list): 現在のファイルリスト
        """
        existing_files = set(self.progress_list.keys())
        current_files = set(file_list)

        # ファイルが削除された場合、is_discardedをTrueに設定
        for file_name in existing_files - current_files:
            self.progress_list[file_name]['is_discarded'] = True

        # 新しいファイルをprogress_listに追加
        for file_name in sorted(current_files - existing_files):
            self.progress_list[file_name] = {
                'status': 'incomplete',
                'is_discarded': False
            }

        self.save_progress()

    def get_file_count(self):
        """進捗リストに登録されたファイルの総数を返します。"""
        return len(self.progress_list)

    def get_discarded_file_count(self):
        """破棄フラグが設定されたファイルの数を返します。"""
        return sum(1 for file_info in self.progress_list.values() if file_info['is_discarded'])

    def get_completed_file_count(self):
        """
        ステータスが 'completed' または 'ignored' に設定されているファイルの数を返します。
        """
        return sum(1 for file_info in self.progress_list.values() 
                   if file_info['status'] in ('completed', 'ignored'))
