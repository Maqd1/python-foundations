import importlib
import inspect
import os
from pathlib import Path

# Global registry: {category: {name: {"function": fn, "author": ..., "version": ..., "enabled": bool}}}
plugin_registry = {}


def register_plugin(category, name, author="Unknown", version="1.0"):
    """Decorator to register a function into the plugin registry with metadata."""

    def decorator(func):
        if category not in plugin_registry:
            plugin_registry[category] = {}

        plugin_registry[category][name] = {
            "function": func,
            "author": author,
            "version": version,
            "enabled": True,
            "category": category,
            "name": name,
        }

        return func

    return decorator


def load_plugins_from_directory(directory_path):
    """Dynamically imports all .py modules from a target directory."""
    path = Path(directory_path)
    if not path.exists() or not path.is_dir():
        return

    # Look for python files (ignoring __init__.py)
    for file_path in path.glob("*.py"):
        if file_path.name == "__init__.py":
            continue

        module_name = file_path.stem
        # Format import path relative to execution root
        rel_path = file_path.with_suffix("").parts
        import_path = ".".join(rel_path)

        try:
            importlib.import_module(import_path)
        except Exception as e:
            print(f"Failed to load plugin {module_name}: {e}")


def execute_plugin(category, name, *args, **kwargs):
    """Executes a registered plugin if enabled."""
    if category not in plugin_registry or name not in plugin_registry[category]:
        raise KeyError(f"Plugin '{category}.{name}' not found.")

    plugin_info = plugin_registry[category][name]
    if not plugin_info["enabled"]:
        raise RuntimeError(f"Plugin '{category}.{name}' is currently disabled.")

    return plugin_info["function"](*args, **kwargs)


def list_plugins():
    """Prints all registered plugins grouped by category."""
    print("Loaded plugins:")
    for category, plugins in plugin_registry.items():
        print(f"📦 {category} ({len(plugins)} plugins)")
        for name, info in plugins.items():
            status = "" if info["enabled"] else " [DISABLED]"
            print(
                f"   ├── {name} v{info['version']} ({info['author']}){status}"
            )
        print()


def get_plugin_info(category, name):
    """Gets raw metadata for a specific plugin."""
    if category in plugin_registry and name in plugin_registry[category]:
        info = dict(plugin_registry[category][name])
        info.pop("function", None)
        return info
    return None


def enable_plugin(category, name):
    if category in plugin_registry and name in plugin_registry[category]:
        plugin_registry[category][name]["enabled"] = True


def disable_plugin(category, name):
    if category in plugin_registry and name in plugin_registry[category]:
        plugin_registry[category][name]["enabled"] = False


def unload_plugin(category, name):
    if category in plugin_registry and name in plugin_registry[category]:
        del plugin_registry[category][name]
        if not plugin_registry[category]:
            del plugin_registry[category]