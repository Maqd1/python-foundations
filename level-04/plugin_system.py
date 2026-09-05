'''
🔴 Very Hard Level (3 Questions)
Q5: The Plugin System (Hard)

Create a plugin architecture where functions can be dynamically registered and loaded.

Requirements:

    Create a plugin_manager.py module that:

        Maintains a registry of plugins

        Allows registering plugins with metadata

        Loads plugins from a directory

        Executes plugins based on triggers

    Plugin Registry:
    python

    plugin_registry = {
        "math": {
            "add": {"function": add, "author": "Damilola", "version": "1.0"},
            "multiply": {"function": multiply, "author": "Damilola", "version": "1.0"}
        },
        "string": {
            "reverse": {"function": reverse, "author": "John", "version": "1.1"}
        }
    }

    Decorator for Registration:
    python

    @register_plugin("math", "subtract")
    def subtract(a, b):
        return a - b

    Dynamic Loading:

        Scan a plugins/ directory

        Import any .py files

        Automatically register functions with @register_plugin

    Plugin Execution:
    python

    result = execute_plugin("math", "add", 5, 3)
    # Result: 8

    Plugin Management:

        List all plugins

        Get plugin info

        Enable/disable plugins

        Unload plugin

    Create plugins/ directory with example plugins:

        math_plugins.py

        string_plugins.py

        custom_plugins.py

Sample Output:
text

🔌 PLUGIN SYSTEM 🔌

Loaded plugins:
📦 math (2 plugins)
   ├── add v1.0 (Damilola)
   └── multiply v1.0 (Damilola)

📦 string (3 plugins)
   ├── reverse v1.1 (John)
   ├── uppercase v1.0 (Alice)
   └── count_words v1.0 (Alice)

📦 custom (1 plugin)
   └── encrypt v2.0 (Bob)

Execute plugin: math.add(5, 3)
Result: 8

Plugin metadata:
{
    "name": "add",
    "category": "math",
    "author": "Damilola",
    "version": "1.0",
    "enabled": True
}

Loading new plugin from 'plugins/my_plugin.py'...
✅ Plugin registered successfully!

Concepts: Decorators with parameters, dynamic imports, function registry, dictionary metadata, modular architecture
'''