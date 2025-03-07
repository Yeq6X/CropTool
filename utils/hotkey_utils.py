# utils/hotkey_utils.py

def register_hotkeys(root, hotkeys, callbacks):
    for action, key in hotkeys.items():
        root.bind(key, callbacks[action])

def unregister_hotkeys(root, hotkeys):
    for key in hotkeys.values():
        root.unbind(key)

def get_hotkey_text(settings_model):
    """settings.jsonの設定に基づいてホットキーの説明テキストを生成"""
    settings = settings_model.settings
    hotkeys = settings.get('hotkeys', {})
    
    # デフォルトのホットキー設定（settings.jsonに設定がない場合のフォールバック）
    default_hotkeys = {
        "next_image": "<space>",
        "previous_image": "<Shift-space>",
        "save_image": "<Control-s>",
        "ignore_image": "<Control-b>",
        "corner_mode": "<KeyPress-r>",
        "center_mode": "<KeyPress-e>",
        "color_pick_keys": "<KeyPress-s>"
    }
    
    # 実際のホットキー（設定があればそれを使用、なければデフォルト値を使用）
    hotkeys_list_dict = {k: hotkeys.get(k, v).replace("<", "").replace(">", "").split("-") for k, v in default_hotkeys.items()}
    actual_hotkeys = {k: ' + '.join(map(lambda s: s[0].upper() + s[1:], v)) for k, v in hotkeys_list_dict.items()}

    return f"""
利用可能なホットキー:
{actual_hotkeys['next_image']}: 次の画像へ | {actual_hotkeys['previous_image']}: 前の画像へ | {actual_hotkeys['save_image']}: 画像を保存 | {actual_hotkeys['ignore_image']}: 画像をスキップ
{actual_hotkeys['corner_mode']}: 四隅選択モード | {actual_hotkeys['center_mode']}: 中心点選択モード | {actual_hotkeys['color_pick_keys']}: 色選択モード
"""
