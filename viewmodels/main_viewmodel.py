# viewmodels/main_viewmodel.py

import tkinter as tk
from models.progress_model import ProgressModel
from models.settings_model import SettingsModel
from views.main_view import MainView
from viewmodels.image_viewmodel import ImageViewModel
from utils.file_utils import create_folder_if_not_exists
import os

class MainViewModel:
    def __init__(self, master):
        self.master = master
        self.settings_model = SettingsModel('data/settings.json')
        print(self.settings_model.settings)
        self.progress_model = None
        
        # 設定からウィンドウサイズを読み込んで設定
        window_size = self.settings_model.settings.get('window_size', {'width': 800, 'height': 600})
        self.master.geometry(f"{window_size['width']}x{window_size['height']}")
        self.master.bind("<Configure>", self.on_window_resize)
        
        self.main_view = MainView(master, self)
        self.input_folder = ''
        self.output_folder = ''

    def on_window_resize(self, event):
        # リサイズイベントを処理し、ウィンドウのサイズを保存
        if event.widget == self.master:
            new_width = event.width
            new_height = event.height
            self.settings_model.settings['window_size'] = {
                'width': new_width,
                'height': new_height
            }
            self.settings_model.save_settings()

    def select_input_folder(self):
        folder = tk.filedialog.askdirectory()
        if folder:
            self.input_folder = folder
            self.output_folder = os.path.join(self.input_folder, 'output')
            create_folder_if_not_exists(self.output_folder)
            progress_file = os.path.join(self.output_folder, 'progress.json')
            self.progress_model = ProgressModel(progress_file, self.input_folder, self.output_folder)
            self.main_view.log(f'入力フォルダ: {self.input_folder}')
            self.main_view.log(f'出力フォルダ: {self.output_folder}')
        else:
            self.main_view.log('入力フォルダを選択してください。')

    def start_loading(self):
        if not self.input_folder:
            self.main_view.log('先に入力フォルダを選択してください。')
            return
        # 名前順に読み込む
        image_files = sorted([f for f in os.listdir(self.input_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp'))])
        print(image_files)
        self.progress_model.sync_with_files(image_files) # 進捗をファイルリストと同期または新規作成
        self.main_view.log('入力フォルダと進捗が同期しました。')
        self.open_image_view()

    def open_image_view(self):
        self.main_view.pack_forget()
        ImageViewModel(self.master, self.progress_model, self.settings_model)
