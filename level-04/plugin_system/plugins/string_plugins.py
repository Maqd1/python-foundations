from plugin_manager import register_plugin


@register_plugin("string", "reverse", author="John", version="1.1")
def reverse(text):
    return text[::-1]


@register_plugin("string", "uppercase", author="Alice", version="1.0")
def uppercase(text):
    return text.upper()


@register_plugin("string", "count_words", author="Alice", version="1.0")
def count_words(text):
    return len(text.split())