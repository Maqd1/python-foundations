import json
import os


REQUIRED_FIELDS = [
    "database.host",
    "database.port",
    "database.credentials.username",
    "logging.level",
]


def display_config(data, prefix=""):
    for key, value in data.items():
        full_key = f"{prefix}.{key}" if prefix else key

        if isinstance(value, dict):
            display_config(value, full_key)
        else:
            print(f"{full_key} = {value}")


def get_nested_value(data, key_path):
    keys = key_path.split(".")

    current = data

    for key in keys:
        if not isinstance(current, dict) or key not in current:
            return None

        current = current[key]

    return current


def set_nested_value(data, key_path, value):
    keys = key_path.split(".")

    current = data

    for key in keys[:-1]:
        if key not in current:
            current[key] = {}

        if not isinstance(current[key], dict):
            return False

        current = current[key]

    current[keys[-1]] = value
    return True


def parse_value(value):
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return value


def validate_required_fields(data):
    missing = []

    for field in REQUIRED_FIELDS:
        if get_nested_value(data, field) is None:
            missing.append(field)

    return missing


def save_config(filename, data):
    backup_filename = f"{filename}.bak"

    if os.path.exists(filename):
        with open(filename, "r") as original:
            old_config = original.read()

        with open(backup_filename, "w") as backup:
            backup.write(old_config)

        print(f"Backup created: {backup_filename}")

    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

    print("✅ Config saved successfully!")


filename = input("Enter config filename: ").strip()

try:
    with open(filename, "r") as file:
        config = json.load(file)

except FileNotFoundError:
    print(f"❌ File not found: {filename}")
    raise SystemExit

except json.JSONDecodeError:
    print(f"❌ Invalid JSON file: {filename}")
    raise SystemExit


print("\n⚙️ CONFIGURATION MANAGER ⚙️")
print(f"Loaded config from: {filename}")

print("\nCurrent settings:")
display_config(config)


while True:
    key = input(
        "\nEnter key to modify (or 'save' to save): "
    ).strip()

    if key.lower() == "save":
        print("\n📁 Saving config...")

        missing = validate_required_fields(config)

        if missing:
            print("❌ Missing required fields:")

            for field in missing:
                print(f"   - {field}")

            continue

        save_config(filename, config)

        print("\nNew config:")
        print(json.dumps(config, indent=4))

        break

    value = input("Enter new value: ")
    value = parse_value(value)

    if set_nested_value(config, key, value):
        print(f"✅ Updated {key} to {value}")
    else:
        print(f"❌ Could not update {key}")