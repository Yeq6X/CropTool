# views/main_view.py

import tkinter as tk
from tkinter import filedialog
from utils.hotkey_utils import get_hotkey_text

class MainView(tk.Frame):
    def __init__(self, master, viewmodel):
        super().__init__(master)
        self.viewmodel = viewmodel
        self.pack()
        self.setup_ui()

    def setup_ui(self):
        # ボタン説明用のラベル
        self.command_description = tk.Label(self, text="コマンドの説明がここに表示されます", fg="blue")
        self.command_description.pack(pady=5)

        # ホットキーコマンドの説明用のラベル
        self.hotkey_description = tk.Label(self, text=get_hotkey_text(self.viewmodel.settings_model), fg="green", justify=tk.LEFT)
        self.hotkey_description.pack(pady=5)

        self.select_input_button = tk.Button(self, text='入力フォルダを選択', command=self.viewmodel.select_input_folder)
        self.select_input_button.pack(pady=5)
        # ボタンにマウスオーバーイベントを追加
        self.select_input_button.bind("<Enter>", lambda e: self.show_description("入力フォルダを選択します。画像処理を行うためのソース画像が含まれるフォルダを指定してください。"))
        self.select_input_button.bind("<Leave>", lambda e: self.clear_description())

        self.start_loading_button = tk.Button(self, text='読み込み開始', command=self.viewmodel.start_loading)
        self.start_loading_button.pack(pady=5)
        # ボタンにマウスオーバーイベントを追加
        self.start_loading_button.bind("<Enter>", lambda e: self.show_description("選択したフォルダから画像の読み込みを開始します。処理には時間がかかる場合があります。"))
        self.start_loading_button.bind("<Leave>", lambda e: self.clear_description())

        self.log_text = tk.Text(self, height=10, width=50, state='disabled')
        self.log_text.pack(pady=5)

    def log(self, message):
        """ログメッセージを表示"""
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, message + '\n')
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')
        
    def show_description(self, description):
        """コマンドの説明を表示"""
        self.command_description.config(text=description)
        
    def clear_description(self):
        """コマンドの説明をクリア"""
        self.command_description.config(text="")
