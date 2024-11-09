# views/main_view.py

import tkinter as tk
from tkinter import filedialog

class MainView(tk.Frame):
    def __init__(self, master, viewmodel):
        super().__init__(master)
        self.viewmodel = viewmodel
        self.pack()
        self.setup_ui()

    def setup_ui(self):
        self.select_input_button = tk.Button(self, text='Select Input Folder', command=self.viewmodel.select_input_folder)
        self.select_input_button.pack(pady=5)

        self.start_loading_button = tk.Button(self, text='Start Loading', command=self.viewmodel.start_loading)
        self.start_loading_button.pack(pady=5)

        self.log_text = tk.Text(self, height=10, width=50, state='disabled')
        self.log_text.pack(pady=5)

    def log(self, message):
        """ログメッセージを表示"""
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, message + '\n')
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')
