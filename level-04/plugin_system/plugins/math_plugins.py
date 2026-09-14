from plugin_manager import register_plugin


@register_plugin("math", "add", author="Damilola", version="1.0")
def add(a, b):
    return a + b


@register_plugin("math", "multiply", author="Damilola", version="1.0")
def multiply(a, b):
    return a * b