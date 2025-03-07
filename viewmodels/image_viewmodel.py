# viewmodels/image_viewmodel.py

import tkinter as tk
from PIL import Image, ImageTk
from models.image_model import ImageModel
from views.image_view import ImageView
from utils.image_utils import crop_image, save_image
import os
import winsound

class ImageViewModel:
    def __init__(self, master, progress_model, settings_model):
        self.master = master
        self.progress_model = progress_model
        self.settings_model = settings_model
        self.image_view = ImageView(master, self)
        self.image_list = self.get_incomplete_images()
        self.current_index = -1
        self.image_model = None
        self.start_point = None
        self.tmp_rectangle = None
        self.current_mode = 'corner'
        self.zoom_level = 1.0
        self.crop_rectangle = None

        if self.image_list:
            self.load_next_image()
        else:
            self.image_view.update_info('No images to load.')

        # ホットキーの登録
        self.master.bind(self.settings_model.settings['hotkeys']['next_image'], lambda e: self.load_next_image())
        self.master.bind(self.settings_model.settings['hotkeys']['previous_image'], lambda e: self.load_previous_image())
        self.master.bind(self.settings_model.settings['hotkeys']['save_image'], lambda e: self.save_image())
        self.master.bind(self.settings_model.settings['hotkeys']['ignore_image'], lambda e: self.ignore_image())
        self.master.bind(self.settings_model.settings['hotkeys']['corner_mode'], lambda e: self.set_mode('corner'))
        self.master.bind(self.settings_model.settings['hotkeys']['center_mode'], lambda e: self.set_mode('center'))
        self.master.bind(self.settings_model.settings['hotkeys']['color_pick_keys'], self.pick_color_event)

        # マウスホイールの登録
        self.image_view.canvas.bind("<MouseWheel>", self.on_mouse_wheel)
        self.image_view.canvas.bind("<Shift-MouseWheel>", self.on_shift_mouse_wheel)
        self.image_view.canvas.bind("<Control-MouseWheel>", self.on_ctrl_mouse_wheel)

    def set_mode(self, mode):
        """クロップモードの設定"""
        self.current_mode = mode

    def get_incomplete_images(self):
        """未完了の画像リストを取得"""
        return [fname for fname, pdata in self.progress_model.progress_list.items()
                if pdata['status'] == 'incomplete' and not pdata['is_discarded']]

    def load_next_image(self):
        """次の画像をロード"""
        if self.current_index + 1 < len(self.image_list):
            self.current_index += 1
            self.load_image()
        else:
            self.image_view.update_info('No more images.')

    def load_previous_image(self):
        """前の画像をロード"""
        if self.current_index - 1 >= 0:
            self.current_index -= 1
            self.load_image()
        else:
            self.image_view.update_info('No previous images.')
            
    def load_image(self):
        file_name = self.image_list[self.current_index]
        file_path = os.path.join(self.progress_model.input_folder, file_name)
        self.image_model = ImageModel(file_path)
        
        # 初期のrectを中心にmin_image_sizeの正方形を描画
        image_width, image_height = self.image_model.image_data.size
        canvas_width = image_width * 3
        canvas_height = image_height * 3
        x0 = canvas_width / 2 - self.settings_model.settings['min_image_size'] / 2
        y0 = canvas_height / 2 - self.settings_model.settings['min_image_size'] / 2
        x1 = canvas_width / 2 + self.settings_model.settings['min_image_size'] / 2
        y1 = canvas_height / 2 + self.settings_model.settings['min_image_size'] / 2
        self.crop_rectangle = (x0, y0, x1, y1)
        
        self.calculate_zoom_level()
        self.zoom_level *= 0.6
        self.display_image()
        self.center_image()
        self.update_info_label()
        

    def calculate_zoom_level(self):
        """ImageViewの短辺に画像の長辺が合うようにzoom_levelを計算する"""
        canvas_width = self.image_view.canvas.winfo_width()
        canvas_height = self.image_view.canvas.winfo_height()
        image_width, image_height = self.image_model.image_data.size

        # 画像とキャンバスのサイズを取得後に計算
        if canvas_width == 1 and canvas_height == 1:
            # 最初にキャンバスのウィンドウサイズが取得できない可能性があるため一度更新する
            self.master.update()
            canvas_width = self.image_view.canvas.winfo_width()
            canvas_height = self.image_view.canvas.winfo_height()

        # 短辺に合わせるために、画像の横と縦の比率を計算し、最小の比率を使用する
        scale_x = canvas_width / image_width
        scale_y = canvas_height / image_height
        self.zoom_level = min(scale_x, scale_y)

    def display_image(self):
    # ズームレベルを反映して画像を表示
        image_to_display = self.image_model.image_data.copy().resize(
            (int(self.image_model.image_data.width * self.zoom_level),
            int(self.image_model.image_data.height * self.zoom_level)),
            Image.ANTIALIAS
        )
        self.image_view.image_tk = ImageTk.PhotoImage(image_to_display)

        # 画像の大きさを取得
        image_width = int(self.image_model.image_data.width * self.zoom_level)
        image_height = int(self.image_model.image_data.height * self.zoom_level)

        # キャンバスのスクロール領域を画像の大きさよりも少し大きく設定し、全方向にスクロール可能にする
        scroll_region = (
            0,  # 左
            0,  # 上
            image_width * 3,  # 右
            image_height * 3  # 下
        )
        self.image_view.canvas.config(scrollregion=scroll_region)

        # デバッグのため、スクロール領域の背景として矩形を描画
        self.image_view.canvas.delete('scrollregion_bg')  # 既存のデバッグ矩形を削除
        self.image_view.canvas.create_rectangle(
            scroll_region[0], scroll_region[1], scroll_region[2], scroll_region[3],
            fill=self.settings_model.settings['background_color'],
            outline='', tags='scrollregion_bg'
        )

        # キャンバスの中央に画像を描画
        canvas_center_x = (scroll_region[2] - scroll_region[0]) / 2
        canvas_center_y = (scroll_region[3] - scroll_region[1]) / 2
        self.image_view.canvas.create_image(canvas_center_x, canvas_center_y, anchor='center', image=self.image_view.image_tk, tags='image')

        # 矩形を描画
        self.draw_shapes()

    def center_image(self):
        """画像をキャンバスの中心に表示する"""
        # スクロール領域の中心を計算
        image_width = self.image_model.image_data.width * self.zoom_level
        image_height = self.image_model.image_data.height * self.zoom_level
        scroll_width = image_width * 3
        scroll_height = image_height * 3
        
        canvas_width = self.image_view.canvas.winfo_width()
        canvas_height = self.image_view.canvas.winfo_height()

        # 中央にスクロールするためにスクロール位置を設定
        self.image_view.canvas.xview_moveto((scroll_width - canvas_width) / 2 / scroll_width)
        self.image_view.canvas.yview_moveto((scroll_height - canvas_height) / 2 / scroll_height)

    def update_info_label(self):
        all_files = self.progress_model.get_file_count() - self.progress_model.get_discarded_file_count()
        completed_files = self.progress_model.get_completed_file_count()
        # ファイル名のみ表示
        info = [f"ファイル名: {os.path.basename(self.image_model.file_path)}",
                f"ステータス: {self.progress_model.progress_list[self.image_list[self.current_index]]['status']}",
                f"進捗: {completed_files}/{all_files}"]
        info_text = ' | '.join(info)
        self.image_view.update_info(info_text)

    def save_image(self):
        """クロップして画像を保存し、進捗を更新"""
        if self.crop_rectangle and self.crop_rectangle[2] - self.crop_rectangle[0] >= self.settings_model.settings['min_image_size']:
            cropped_image = crop_image(self.image_model.image_data, self.crop_rectangle, self.settings_model.settings['background_color'])
            output_path = os.path.join(self.progress_model.output_folder,
                                       f"{os.path.splitext(os.path.basename(self.image_model.file_path))[0]}_{self.image_model.crop_count}.{os.path.splitext(os.path.basename(self.image_model.file_path))[1]}")
            save_image(cropped_image, output_path)
            self.image_model.increment_crop_count()
            self.progress_model.update_status(os.path.basename(self.image_model.file_path), 'completed')
            self.image_view.update_log(f"画像を保存しました: {output_path}")
            self.crop_rectangle = None  # 保存後に矩形をリセット
        else:
            winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
            self.image_view.update_log("画像のサイズが小さすぎます。最小サイズは" + str(self.settings_model.settings['min_image_size']) + "pxです。settings.jsonのmin_image_sizeを変更してください。")

    def ignore_image(self):
        """画像を無視として進捗を更新"""
        self.progress_model.update_status(os.path.basename(self.image_model.file_path), 'ignored')
        self.load_next_image()

    def pick_color_event(self, event):
        """色取得の共通イベントハンドラ"""
        # 画面上のマウス座標を取得
        screen_x, screen_y = self.image_view.canvas.winfo_pointerxy()

        # キャンバス上の相対座標に変換
        canvas_x = screen_x - self.image_view.canvas.winfo_rootx()
        canvas_y = screen_y - self.image_view.canvas.winfo_rooty()

        # scrollregion上でのスクロール位置を取得
        x = self.image_view.canvas.canvasx(canvas_x) / self.zoom_level
        y = self.image_view.canvas.canvasy(canvas_y) / self.zoom_level
        
        # 画像上の座標に変換
        x, y = self.scrollregion_to_image_coords(x, y)
        
        self.pick_color(x, y)

    def pick_color(self, x, y):
        """指定された座標から色を取得し、設定に保存"""
        # 画像のサイズを取得
        image_width, image_height = self.image_model.image_data.size
        
        # 座標が画像の範囲内にあるかチェック
        if 0 <= x < image_width and 0 <= y < image_height:
            # 画像上の位置で色を取得
            pixel_color = self.image_model.image_data.getpixel((int(x), int(y)))
            color_hex = '#%02x%02x%02x' % pixel_color[:3]
            
            # 取得した色を設定に保存
            self.settings_model.settings['background_color'] = color_hex
            self.settings_model.save_settings()
            
            self.display_image()

    # scrollregion上の座標をimage上の座標に変換
    def scrollregion_to_image_coords(self, x, y):
        # 現在3倍になっている
        image_width = self.image_model.image_data.width
        image_height = self.image_model.image_data.height
        
        x = x - image_width
        y = y - image_height
        
        return x, y

    def on_left_click(self, event):
        """矩形の開始位置を設定"""
        x = self.image_view.canvas.canvasx(event.x) / self.zoom_level
        y = self.image_view.canvas.canvasy(event.y) / self.zoom_level
        self.start_point = (x, y)
        self.image_view.canvas.delete('crop_rectangle')
        if self.current_mode == 'corner':
            self.tmp_rectangle = self.image_view.canvas.create_rectangle(x, y, x, y, outline='red', tags='tmp_rectangle')
        elif self.current_mode == 'center':
            self.tmp_rectangle = self.image_view.canvas.create_rectangle(x, y, x, y, outline='red', tags='tmp_rectangle')

    def on_mouse_move(self, event):
        """マウスドラッグ中の矩形または投げ縄の描画を更新"""
        x = self.image_view.canvas.canvasx(event.x) / self.zoom_level
        y = self.image_view.canvas.canvasy(event.y) / self.zoom_level
        if self.start_point and self.start_point[0] != x and self.start_point[1] != y:
            if self.current_mode == 'corner':
                # 符号を取得して正方形のサイズを計算
                x0, y0 = self.start_point
                sign_x = (x - x0) / abs(x - x0)
                sign_y = (y - y0) / abs(y - y0)
                square_size = max(abs(x - x0), abs(y - y0))
                x1 = x0 + square_size * sign_x
                y1 = y0 + square_size * sign_y
            elif self.current_mode == 'center':
                self.start_point
                square_size = max(abs(x - self.start_point[0]), abs(y - self.start_point[1]))*2
                x0 = self.start_point[0] - square_size/2
                y0 = self.start_point[1] - square_size/2
                x1 = self.start_point[0] + square_size/2
                y1 = self.start_point[1] + square_size/2

            # ズームレベルを反映して矩形を描画            
            x0, y0, x1, y1 = [val * self.zoom_level for val in (x0, y0, x1, y1)]
            self.image_view.canvas.coords(self.tmp_rectangle, x0, y0, x1, y1)

            # サイズが小さい場合は矩形を赤色にする
            if square_size < self.settings_model.settings['min_image_size']:
                self.image_view.canvas.itemconfig(self.tmp_rectangle, outline='red')
            else:
                self.image_view.canvas.itemconfig(self.tmp_rectangle, outline='blue')

    def on_left_release(self, event):
        """矩形の終了位置を設定し、クロップ領域を確定"""
        x = self.image_view.canvas.canvasx(event.x) / self.zoom_level
        y = self.image_view.canvas.canvasy(event.y) / self.zoom_level
        self.image_view.canvas.delete('tmp_rectangle')
        if self.start_point and self.start_point[0] != x and self.start_point[1] != y:
            if self.current_mode == 'corner':
                x0, y0 = self.start_point
                sign_x = (x - x0) / abs(x - x0)
                sign_y = (y - y0) / abs(y - y0)
                square_size = max(abs(x - x0), abs(y - y0))
                x1 = x0 + square_size * sign_x
                y1 = y0 + square_size * sign_y
                self.crop_rectangle = (min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1))
            elif self.current_mode == 'center':
                square_size = max(abs(x - self.start_point[0]), abs(y - self.start_point[1]))*2
                x0 = self.start_point[0] - square_size/2
                y0 = self.start_point[1] - square_size/2
                x1 = self.start_point[0] + square_size/2
                y1 = self.start_point[1] + square_size/2
                self.crop_rectangle = (x0, y0, x1, y1)

            self.start_point = None
            self.draw_shapes()
            
    # 矩形を描画
    def draw_shapes(self):
        self.image_view.canvas.delete('crop_rectangle')
        if self.crop_rectangle:
            x0, y0, x1, y1 = self.crop_rectangle
            self.image_view.canvas.create_rectangle(
                x0 * self.zoom_level, y0 * self.zoom_level,
                x1 * self.zoom_level, y1 * self.zoom_level, outline='green',
                tags='crop_rectangle'
            )

    def on_mouse_wheel(self, event):
        """縦スクロール"""
        self.image_view.canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def on_shift_mouse_wheel(self, event):
        """横スクロール"""
        self.image_view.canvas.xview_scroll(-1 * (event.delta // 120), "units")

    def on_ctrl_mouse_wheel(self, event):
        """拡大縮小"""
        self.zoom_level *= 1.1 if event.delta > 0 else 0.9
        self.display_image()
