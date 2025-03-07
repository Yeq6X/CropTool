# views/image_view.py

import tkinter as tk
from PIL import ImageTk
from tkinter import Canvas
from utils.hotkey_utils import get_hotkey_text

class ImageView(tk.Frame):
    def __init__(self, master, viewmodel):
        super().__init__(master)
        self.viewmodel = viewmodel
        self.pack(fill=tk.BOTH, expand=True)
        self.setup_ui()

    def setup_ui(self):
        # ホットキーコマンドの説明用のラベル
        self.hotkey_description = tk.Label(self, text=get_hotkey_text(self.viewmodel.settings_model), fg="green", justify=tk.LEFT)
        self.hotkey_description.pack(pady=5)

        self.info_label = tk.Label(self, text='')
        self.info_label.pack(pady=5)
        
        self.log_label = tk.Label(self, text='here is log')
        self.log_label.pack(pady=5)

        self.canvas = Canvas(self)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind('<Button-1>', self.viewmodel.on_left_click)
        self.canvas.bind('<ButtonRelease-1>', self.viewmodel.on_left_release)
        self.canvas.bind('<Button-3>', self.viewmodel.pick_color_event)
        self.canvas.bind('<Motion>', self.viewmodel.on_mouse_move)

    def display_image(self, image):
        self.image_tk = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, anchor='nw', image=self.image_tk)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

    def update_info(self, info_text):
        self.info_label.config(text=info_text)
        
    def update_log(self, log_label):
        self.log_label.config(text=log_label)
