from plugin_manager import register_plugin


@register_plugin("custom", "encrypt", author="Bob", version="2.0")
def encrypt(text, shift=3):
    return "".join(chr(ord(c) + shift) for c in text)