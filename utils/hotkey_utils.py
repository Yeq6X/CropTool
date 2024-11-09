# utils/hotkey_utils.py

def register_hotkeys(root, hotkeys, callbacks):
    for action, key in hotkeys.items():
        root.bind(key, callbacks[action])

def unregister_hotkeys(root, hotkeys):
    for key in hotkeys.values():
        root.unbind(key)
