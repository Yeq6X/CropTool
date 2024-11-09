# main.py: アプリケーションのエントリポイント

import tkinter as tk
from viewmodels.main_viewmodel import MainViewModel

def main():
    root = tk.Tk()
    root.title("LoRA Image Processing Tool")
    app = MainViewModel(root)
    root.mainloop()

if __name__ == "__main__":
    main()
