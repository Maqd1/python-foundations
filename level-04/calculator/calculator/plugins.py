"""Simple plugin system: register custom functions the evaluator can call by name."""

_plugins = {}


def register_plugin(name, func):
    _plugins[name] = func


def get_plugin(name):
    return _plugins.get(name)


def list_plugins():
    return list(_plugins.keys())
