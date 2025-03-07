# image_utils.py: 画像操作のユーティリティ関数
from PIL import Image, ImageDraw

def open_image(file_path):
    # RGBモードで画像を開く
    image = Image.open(file_path).convert('RGB')
    return image

def save_image(image, file_path):
    image.save(file_path)

def crop_image(image, rect, color):
    image_with_background = apply_background_color(image, color)
    # クロップ領域を取得
    cropped_image = image_with_background.crop(rect)

    return cropped_image

def apply_background_color(image, color):
    # 画像のサイズを取得
    width, height = image.size
    
    # 縦横3倍のサイズで背景色を設定した新しい画像を作成
    background_image = Image.new("RGB", (width * 3, height * 3), color)

    # 画像を中央に配置
    paste_x = width
    paste_y = height
    background_image.paste(image, (paste_x, paste_y))

    return background_image
