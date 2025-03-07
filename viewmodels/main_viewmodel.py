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
            self.main_view.log(f'Input folder selected: {self.input_folder}')
            self.main_view.log(f'Output folder: {self.output_folder}')
        else:
            self.main_view.log('No folder selected.')

    def start_loading(self):
        if not self.input_folder:
            self.main_view.log('Please select an input folder first.')
            return
        # 名前順に読み込む
        image_files = sorted([f for f in os.listdir(self.input_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))])
        self.progress_model.sync_with_files(image_files) # 進捗をファイルリストと同期または新規作成
        self.main_view.log('Progress synced with input folder.')
        self.open_image_view()

    def open_image_view(self):
        self.main_view.pack_forget()
        ImageViewModel(self.master, self.progress_model, self.settings_model)
