import json
import os
import re
import pprint
from jsonschema import validate
from jsonschema.exceptions import ValidationError



def load_json_file(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)

    except FileNotFoundError:
        print(f"❌ File not found: {filename}")
        return None

    except json.JSONDecodeError as error:
        print(f"❌ Invalid JSON: {error}")
        return None


def load_json_string(json_string):
    try:
        return json.loads(json_string)
    except json.JSONDecodeError as error:
        print(f"❌ Invalid JSON string: {error}")
        return None


def get_root_type(data):
    if isinstance(data, list):
        return "Array"
    if isinstance(data, dict):
        return "Object"
    if data is None:
        return "Null"
    return type(data).__name__.title()


def count_objects(data):
    if isinstance(data, dict):
        return 1 + sum(count_objects(value) for value in data.values())

    if isinstance(data, list):
        return sum(count_objects(item) for item in data)

    return 0


def collect_keys(data, keys=None):
    if keys is None:
        keys = set()

    if isinstance(data, dict):
        for key, value in data.items():
            keys.add(key)
            collect_keys(value, keys)

    elif isinstance(data, list):
        for item in data:
            collect_keys(item, keys)

    return keys


def show_summary(data):
    print("\n" + "=" * 70)
    print("📊 JSON SUMMARY")
    print("=" * 70)

    keys = collect_keys(data)

    print(f"Root type: {get_root_type(data)}")
    print(f"Objects: {count_objects(data)}")
    print(f"Unique keys: {len(keys)}")
    print(f"Keys: {', '.join(sorted(keys))}")


def pretty_print(data):
    print("\n" + "=" * 70)
    print("📋 JSON DATA")
    print("=" * 70)

    print(json.dumps(data, indent=4, ensure_ascii=False))


def get_dot_value(data, path):
    if not path:
        return data

    current = data

    for part in path.split("."):

        if isinstance(current, dict):

            if part not in current:
                raise KeyError(f"Key '{part}' not found.")

            current = current[part]

        elif isinstance(current, list):

            try:
                index = int(part)
            except ValueError:
                raise TypeError(
                    f"'{part}' is not a valid array index."
                )

            if index < 0 or index >= len(current):
                raise IndexError(
                    f"Array index {index} is out of range."
                )

            current = current[index]

        else:
            raise TypeError(
                f"Cannot access '{part}' inside "
                f"{type(current).__name__}."
            )

    return current


def dot_notation_query(data):
    print("\n" + "=" * 70)
    print("🔍 DOT NOTATION")
    print("=" * 70)

    print("Examples:")
    print("  address.city")
    print("  0.address.city")
    print("  1.name")

    path = input("\nEnter path: ").strip()

    try:
        result = get_dot_value(data, path)

        print("\nResult:")
        print(json.dumps(result, indent=4, ensure_ascii=False))

    except (KeyError, IndexError, TypeError) as error:
        print(f"❌ {error}")


def find_all_key_occurrences(data, target_key, path="$"):
    results = []

    if isinstance(data, dict):

        for key, value in data.items():

            current_path = f"{path}.{key}"

            if key == target_key:
                results.append({
                    "path": current_path,
                    "value": value
                })

            results.extend(
                find_all_key_occurrences(
                    value,
                    target_key,
                    current_path
                )
            )

    elif isinstance(data, list):

        for index, item in enumerate(data):

            current_path = f"{path}[{index}]"

            results.extend(
                find_all_key_occurrences(
                    item,
                    target_key,
                    current_path
                )
            )

    return results


def find_key_menu(data):
    print("\n" + "=" * 70)
    print("🔎 FIND ALL KEY OCCURRENCES")
    print("=" * 70)

    key = input("Enter key: ").strip()

    results = find_all_key_occurrences(data, key)

    if not results:
        print(f"❌ Key '{key}' was not found.")
        return

    print(f"\nFound {len(results)} occurrence(s):\n")

    for result in results:
        print(f"Path: {result['path']}")
        print(
            "Value:",
            json.dumps(
                result["value"],
                ensure_ascii=False
            )
        )
        print()


def parse_jsonpath(path):
    path = path.strip()

    if path.startswith("$"):
        path = path[1:]

    if path.startswith("."):
        path = path[1:]

    tokens = []
    current = ""
    index = 0

    while index < len(path):

        char = path[index]

        if char == ".":

            if current:
                tokens.append(current)
                current = ""

            index += 1
            continue

        if char == "[":

            if current:
                tokens.append(current)
                current = ""

            end = path.find("]", index)

            if end == -1:
                raise ValueError("Missing closing ']'.")

            tokens.append(path[index + 1:end])
            index = end + 1
            continue

        current += char
        index += 1

    if current:
        tokens.append(current)

    return tokens


def jsonpath_search(data, tokens):
    if not tokens:
        return [data]

    token = tokens[0]
    remaining = tokens[1:]

    results = []

    if token == "*":

        if isinstance(data, dict):

            for value in data.values():
                results.extend(
                    jsonpath_search(
                        value,
                        remaining
                    )
                )

        elif isinstance(data, list):

            for value in data:
                results.extend(
                    jsonpath_search(
                        value,
                        remaining
                    )
                )

        return results

    if isinstance(data, list):

        try:
            index = int(token)
        except ValueError:
            return []

        if 0 <= index < len(data):
            return jsonpath_search(
                data[index],
                remaining
            )

        return []

    if isinstance(data, dict):

        if token not in data:
            return []

        return jsonpath_search(
            data[token],
            remaining
        )

    return []


def jsonpath_query(data):
    print("\n" + "=" * 70)
    print("🌳 JSONPATH QUERY")
    print("=" * 70)

    print("Examples:")
    print("  $.0.name")
    print("  $[*].name")
    print("  $[*].address.city")
    print("  $[0].address.city")

    path = input("\nEnter JSONPath: ").strip()

    try:
        tokens = parse_jsonpath(path)
        results = jsonpath_search(data, tokens)

        if not results:
            print("❌ No results found.")
            return

        print(f"\nFound {len(results)} result(s):\n")

        for index, result in enumerate(results, start=1):
            print(f"[{index}]")
            print(
                json.dumps(
                    result,
                    indent=4,
                    ensure_ascii=False
                )
            )

    except ValueError as error:
        print(f"❌ {error}")


def get_nested_value(data, path):
    try:
        return get_dot_value(data, path)
    except (KeyError, IndexError, TypeError):
        return None


def parse_condition(condition):
    operators = [
        "contains",
        ">=",
        "<=",
        "!=",
        "=",
        ">",
        "<"
    ]

    for operator in operators:

        if operator in condition:

            left, right = condition.split(
                operator,
                1
            )

            left = left.strip()
            right = right.strip()

            if (
                len(right) >= 2
                and right[0] == "'"
                and right[-1] == "'"
            ):
                right = right[1:-1]

            elif (
                len(right) >= 2
                and right[0] == '"'
                and right[-1] == '"'
            ):
                right = right[1:-1]

            elif right.lower() == "true":
                right = True

            elif right.lower() == "false":
                right = False

            elif right.lower() == "null":
                right = None

            else:

                try:
                    if "." in right:
                        right = float(right)
                    else:
                        right = int(right)

                except ValueError:
                    pass

            return left, operator, right

    raise ValueError("Invalid condition.")


def compare_values(actual, operator, expected):

    if operator == "=":
        return actual == expected

    if operator == "!=":
        return actual != expected

    if operator == ">":
        try:
            return actual > expected
        except TypeError:
            return False

    if operator == "<":
        try:
            return actual < expected
        except TypeError:
            return False

    if operator == ">=":
        try:
            return actual >= expected
        except TypeError:
            return False

    if operator == "<=":
        try:
            return actual <= expected
        except TypeError:
            return False

    if operator == "contains":

        if isinstance(actual, str):
            return str(expected).lower() in actual.lower()

        if isinstance(actual, list):
            return expected in actual

        return False

    return False


def evaluate_single_condition(item, condition):
    field, operator, expected = parse_condition(
        condition
    )

    actual = get_nested_value(
        item,
        field
    )

    return compare_values(
        actual,
        operator,
        expected
    )


def split_logical_conditions(condition):
    pattern = r"\s+(AND|OR)\s+"

    parts = re.split(
        pattern,
        condition,
        flags=re.IGNORECASE
    )

    conditions = []
    operators = []

    for index, part in enumerate(parts):

        if index % 2 == 0:
            conditions.append(part.strip())

        else:
            operators.append(part.upper())

    return conditions, operators


def evaluate_condition(item, condition):
    conditions, operators = split_logical_conditions(
        condition
    )

    if not conditions:
        return False

    try:
        results = [
            evaluate_single_condition(
                item,
                single_condition
            )
            for single_condition in conditions
        ]

    except ValueError:
        return False

    result = results[0]

    for index, operator in enumerate(operators):

        if operator == "AND":
            result = result and results[index + 1]

        elif operator == "OR":
            result = result or results[index + 1]

    return result


def filter_array(data, condition):

    if not isinstance(data, list):
        print("❌ Filtering requires a JSON array.")
        return []

    results = []

    for item in data:

        if not isinstance(item, dict):
            continue

        if evaluate_condition(
            item,
            condition
        ):
            results.append(item)

    return results


def array_filter_menu(data):
    print("\n" + "=" * 70)
    print("🔍 ARRAY FILTER")
    print("=" * 70)

    print("Examples:")
    print("  age > 25")
    print("  active = true")
    print("  address.city = Lagos")
    print("  name contains Damilola")
    print("  age > 25 AND active = true")
    print("  age > 30 OR active = false")

    condition = input(
        "\nEnter condition: "
    ).strip()

    results = filter_array(
        data,
        condition
    )

    if not results:
        print("\n❌ No matching records found.")
        return

    print(
        f"\n✅ Found {len(results)} matching record(s):\n"
    )

    print(
        json.dumps(
            results,
            indent=4,
            ensure_ascii=False
        )
    )


def parse_select_fields(select_part):
    fields = []

    for field in select_part.split(","):

        field = field.strip()

        if not field:
            continue

        fields.append(field)

    return fields


def select_field_value(item, field):
    value = get_nested_value(
        item,
        field
    )

    return value


def project_fields(item, fields):
    result = {}

    for field in fields:

        value = select_field_value(
            item,
            field
        )

        result[field] = value

    return result


def parse_select_query(query):
    pattern = re.compile(
        r"^\s*SELECT\s+(.+?)"
        r"(?:\s+WHERE\s+(.+))?"
        r"\s*$",
        re.IGNORECASE
    )

    match = pattern.match(query)

    if not match:
        raise ValueError(
            "Invalid query. Use: "
            "SELECT field1, field2 WHERE condition"
        )

    select_part = match.group(1)
    condition = match.group(2)

    fields = parse_select_fields(
        select_part
    )

    if not fields:
        raise ValueError(
            "No fields were selected."
        )

    return fields, condition


def execute_select_query(data, query):

    if not isinstance(data, list):
        raise ValueError(
            "SELECT queries require a JSON array."
        )

    fields, condition = parse_select_query(
        query
    )

    results = []

    for item in data:

        if not isinstance(item, dict):
            continue

        if condition:

            if not evaluate_condition(
                item,
                condition
            ):
                continue

        results.append(
            project_fields(
                item,
                fields
            )
        )

    return results


def query_language_menu(data):
    print("\n" + "=" * 70)
    print("🧠 JSON QUERY LANGUAGE")
    print("=" * 70)

    print("Examples:")
    print(
        "  SELECT name, age "
        "WHERE age > 25"
    )
    print(
        "  SELECT name, address.city "
        "WHERE active = true"
    )
    print(
        "  SELECT name "
        "WHERE name contains 'Damilola'"
    )
    print(
        "  SELECT name, age "
        "WHERE age > 25 AND active = true"
    )
    print(
        "  SELECT name "
        "WHERE address.city = 'Lagos'"
    )

    query = input("\nEnter query: ").strip()

    try:
        results = execute_select_query(
            data,
            query
        )

        if not results:
            print("\n❌ No matching records found.")
            return

        print(
            f"\n✅ Found {len(results)} result(s):\n"
        )

        print(
            json.dumps(
                results,
                indent=4,
                ensure_ascii=False
            )
        )

    except ValueError as error:
        print(f"❌ {error}")

# ============================================================
# DATA TRANSFORMATION
# ============================================================

def rename_keys(data, rename_map):
    """Rename keys recursively throughout JSON data."""

    if isinstance(data, list):
        return [
            rename_keys(item, rename_map)
            for item in data
        ]

    if isinstance(data, dict):

        result = {}

        for key, value in data.items():

            new_key = rename_map.get(
                key,
                key
            )

            result[new_key] = rename_keys(
                value,
                rename_map
            )

        return result

    return data


def rename_keys_menu(data):
    print("""
============================================================
✏️ RENAME JSON KEYS
============================================================

Enter key mappings one at a time.

Example:
name=full_name
age=user_age
email=contact_email

Type DONE when finished.

============================================================
""")

    rename_map = {}

    while True:

        mapping = input(
            "Rename: "
        ).strip()

        if mapping.upper() == "DONE":
            break

        if "=" not in mapping:
            print(
                "❌ Use this format: old_key=new_key"
            )
            continue

        old_key, new_key = mapping.split(
            "=",
            1
        )

        old_key = old_key.strip()
        new_key = new_key.strip()

        if not old_key or not new_key:
            print(
                "❌ Both key names are required."
            )
            continue

        rename_map[old_key] = new_key

    if not rename_map:
        print("❌ No keys provided.")
        return data

    transformed = rename_keys(
        data,
        rename_map
    )

    print(
        json.dumps(
            transformed,
            indent=4,
            ensure_ascii=False
        )
    )

    return transformed


def extract_nested_value(data, source_path, target_key):
    """Extract a nested value and add it to the top level."""

    if isinstance(data, list):

        return [
            extract_nested_value(
                item,
                source_path,
                target_key
            )
            for item in data
        ]

    if not isinstance(data, dict):
        return data

    value = get_nested_value(
        data,
        source_path
    )

    result = dict(data)

    result[target_key] = value

    return result


def extract_nested_menu(data):
    print("""
============================================================
📤 EXTRACT NESTED VALUE
============================================================

Example:

Source path:
address.city

Target key:
city

This converts:

{
    "name": "Damilola",
    "address": {
        "city": "Lagos"
    }
}

into:

{
    "name": "Damilola",
    "address": {
        "city": "Lagos"
    },
    "city": "Lagos"
}

============================================================
""")

    source_path = input(
        "Source nested path: "
    ).strip()

    if not source_path:
        print("❌ Source path is required.")
        return data

    target_key = input(
        "Target key: "
    ).strip()

    if not target_key:
        print("❌ Target key is required.")
        return data

    transformed = extract_nested_value(
        data,
        source_path,
        target_key
    )

    print(
        json.dumps(
            transformed,
            indent=4,
            ensure_ascii=False
        )
    )

    return transformed

# ============================================================
# ARRAY TO OBJECT
# ============================================================

def array_to_object(data, key_field):
    """Convert an array of objects into an object keyed by a field."""

    if not isinstance(data, list):
        print("❌ Array-to-object conversion requires a JSON array.")
        return data

    result = {}

    for item in data:

        if not isinstance(item, dict):
            continue

        if key_field not in item:
            continue

        key = str(item[key_field])

        result[key] = item

    return result


def array_to_object_menu(data):
    print("""
============================================================
🔄 ARRAY TO OBJECT
============================================================

Example:

Key field:
id

This converts:

[
    {"id": "USER001", "name": "Damilola"},
    {"id": "USER002", "name": "Aisha"}
]

into:

{
    "USER001": {"id": "USER001", "name": "Damilola"},
    "USER002": {"id": "USER002", "name": "Aisha"}
}

============================================================
""")

    key_field = input(
        "Key field: "
    ).strip()

    if not key_field:
        print("❌ Key field is required.")
        return data

    transformed = array_to_object(
        data,
        key_field
    )

    print(
        json.dumps(
            transformed,
            indent=4,
            ensure_ascii=False
        )
    )

    return transformed


# ============================================================
# COMPUTED FIELDS
# ============================================================

def add_computed_field(data, field_name, expression):
    """Add a computed field to every object."""

    if isinstance(data, list):

        return [
            add_computed_field(
                item,
                field_name,
                expression
            )
            for item in data
        ]

    if not isinstance(data, dict):
        return data

    result = dict(data)

    try:

        # Replace field references with values.
        expression_to_eval = expression

        fields = re.findall(
            r"[A-Za-z_][A-Za-z0-9_.]*",
            expression
        )

        reserved = {
            "True",
            "False",
            "None"
        }

        for field in sorted(
            fields,
            key=len,
            reverse=True
        ):

            if field in reserved:
                continue

            value = get_nested_value(
                data,
                field
            )

            if value is None:
                continue

            expression_to_eval = re.sub(
                rf"\b{re.escape(field)}\b",
                repr(value),
                expression_to_eval
            )

        result[field_name] = eval(
            expression_to_eval,
            {
                "__builtins__": {}
            },
            {}
        )

    except Exception as error:

        print(
            f"❌ Could not calculate "
            f"{field_name}: {error}"
        )

        result[field_name] = None

    return result


def computed_field_menu(data):
    print("""
============================================================
🧮 ADD COMPUTED FIELD
============================================================

Examples:

Field name:
age_next_year

Expression:
age + 1

Another example:

Field name:
age_group

Expression:
age * 2

Nested fields are supported:

Field name:
city_length

Expression:
address.city

Type CANCEL to cancel.

============================================================
""")

    field_name = input(
        "Computed field name: "
    ).strip()

    if field_name.upper() == "CANCEL":
        return data

    if not field_name:
        print("❌ Field name is required.")
        return data

    expression = input(
        "Expression: "
    ).strip()

    if expression.upper() == "CANCEL":
        return data

    if not expression:
        print("❌ Expression is required.")
        return data

    transformed = add_computed_field(
        data,
        field_name,
        expression
    )

    print(
        json.dumps(
            transformed,
            indent=4,
            ensure_ascii=False
        )
    )

    return transformed
# ============================================================
# JSON SCHEMA VALIDATION
# ============================================================

def validate_json_schema(data, schema):
    """Validate JSON data against a JSON Schema."""

    try:
        validate(
            instance=data,
            schema=schema
        )

        print("✅ JSON Schema validation passed.")
        return True

    except ValidationError as error:
        print("❌ JSON Schema validation failed.")
        print(f"Reason: {error.message}")

        if error.path:
            print(
                "Location: "
                + ".".join(str(part) for part in error.path)
            )

        return False


def schema_validation_menu(data):
    print("""
============================================================
📋 JSON SCHEMA VALIDATION
============================================================

Validating the current JSON data against a sample
user schema.

============================================================
""")

    schema = {
        "type": "array",
        "items": {
            "type": "object",
            "required": [
                "id",
                "name",
                "email",
                "age",
                "address",
                "active"
            ],
            "properties": {
                "id": {
                    "type": "string"
                },
                "name": {
                    "type": "string"
                },
                "email": {
                    "type": "string"
                },
                "age": {
                    "type": "integer"
                },
                "address": {
                    "type": "object",
                    "required": [
                        "city",
                        "state",
                        "country"
                    ],
                    "properties": {
                        "city": {
                            "type": "string"
                        },
                        "state": {
                            "type": "string"
                        },
                        "country": {
                            "type": "string"
                        }
                    }
                },
                "active": {
                    "type": "boolean"
                }
            }
        }
    }

    validate_json_schema(
        data,
        schema
    )

    return data


# ============================================================
# REQUIRED FIELDS + TYPE VALIDATION
# ============================================================

def validate_required_fields(data, required_fields):
    """Check that required fields exist."""

    if isinstance(data, list):

        results = []

        for index, item in enumerate(data):

            if not isinstance(item, dict):
                results.append({
                    "index": index,
                    "missing": required_fields,
                    "valid": False
                })
                continue

            missing = [
                field
                for field in required_fields
                if field not in item
            ]

            results.append({
                "index": index,
                "missing": missing,
                "valid": len(missing) == 0
            })

        return results

    if isinstance(data, dict):

        missing = [
            field
            for field in required_fields
            if field not in data
        ]

        return [{
            "index": 0,
            "missing": missing,
            "valid": len(missing) == 0
        }]

    return []


def required_fields_menu(data):
    print("""
============================================================
🔎 REQUIRED FIELDS VALIDATION
============================================================

Enter required fields separated by commas.

Example:

id,name,email,age,address,active

============================================================
""")

    fields_input = input(
        "Required fields: "
    ).strip()

    if not fields_input:
        print("❌ No fields provided.")
        return data

    required_fields = [
        field.strip()
        for field in fields_input.split(",")
        if field.strip()
    ]

    results = validate_required_fields(
        data,
        required_fields
    )

    all_valid = True

    for result in results:

        if result["valid"]:

            print(
                f"✅ Record {result['index']}: "
                "all required fields present."
            )

        else:

            all_valid = False

            print(
                f"❌ Record {result['index']}: "
                f"missing {', '.join(result['missing'])}"
            )

    if all_valid:
        print("\n✅ Required field validation passed.")
    else:
        print("\n❌ Required field validation failed.")

    return data


def python_type_name(value):
    """Return the JSON-compatible type name."""

    if isinstance(value, bool):
        return "boolean"

    if isinstance(value, int):
        return "integer"

    if isinstance(value, float):
        return "number"

    if isinstance(value, str):
        return "string"

    if isinstance(value, list):
        return "array"

    if isinstance(value, dict):
        return "object"

    if value is None:
        return "null"

    return "unknown"


def validate_field_types(data, field_types):
    """Validate field types."""

    if isinstance(data, list):

        records = data

    elif isinstance(data, dict):

        records = [data]

    else:

        print("❌ Type validation requires objects.")
        return data

    for index, record in enumerate(records):

        if not isinstance(record, dict):
            print(
                f"❌ Record {index} is not an object."
            )
            continue

        for field, expected_type in field_types.items():

            value = get_nested_value(
                record,
                field
            )

            if value is None:

                print(
                    f"❌ Record {index}: "
                    f"{field} is missing."
                )

                continue

            actual_type = python_type_name(value)

            if actual_type == expected_type:

                print(
                    f"✅ Record {index}: "
                    f"{field} → {actual_type}"
                )

            else:

                print(
                    f"❌ Record {index}: "
                    f"{field} expected "
                    f"{expected_type}, "
                    f"got {actual_type}"
                )

    return data


def type_validation_menu(data):
    print("""
============================================================
🔤 TYPE VALIDATION
============================================================

Enter field:type pairs separated by commas.

Supported types:

string
integer
number
boolean
array
object
null

Example:

name:string,age:integer,active:boolean

Nested fields are supported:

address.city:string

============================================================
""")

    input_value = input(
        "Field types: "
    ).strip()

    if not input_value:
        print("❌ No field types provided.")
        return data

    field_types = {}

    for item in input_value.split(","):

        if ":" not in item:
            print(
                f"❌ Invalid format: {item}"
            )
            continue

        field, expected_type = item.split(
            ":",
            1
        )

        field = field.strip()
        expected_type = expected_type.strip().lower()

        allowed_types = {
            "string",
            "integer",
            "number",
            "boolean",
            "array",
            "object",
            "null"
        }

        if expected_type not in allowed_types:

            print(
                f"❌ Unsupported type: "
                f"{expected_type}"
            )

            continue

        field_types[field] = expected_type

    if not field_types:
        print("❌ No valid field types provided.")
        return data

    validate_field_types(
        data,
        field_types
    )

    return data

# ============================================================
# VALUE RANGE VALIDATION
# ============================================================

def validate_value_ranges(data, range_rules):
    """Validate numeric fields against minimum/maximum ranges."""

    if isinstance(data, list):
        records = data
    elif isinstance(data, dict):
        records = [data]
    else:
        print("❌ Range validation requires JSON objects.")
        return data

    all_valid = True

    for index, record in enumerate(records):

        if not isinstance(record, dict):
            continue

        for field, rules in range_rules.items():

            value = get_nested_value(
                record,
                field
            )

            if value is None:
                print(
                    f"⚠️ Record {index}: "
                    f"{field} is missing."
                )
                all_valid = False
                continue

            if not isinstance(value, (int, float)) \
                    or isinstance(value, bool):

                print(
                    f"❌ Record {index}: "
                    f"{field} is not numeric."
                )
                all_valid = False
                continue

            minimum = rules.get("min")
            maximum = rules.get("max")

            if minimum is not None and value < minimum:

                print(
                    f"❌ Record {index}: "
                    f"{field} = {value} "
                    f"is below minimum {minimum}."
                )

                all_valid = False

            elif maximum is not None and value > maximum:

                print(
                    f"❌ Record {index}: "
                    f"{field} = {value} "
                    f"is above maximum {maximum}."
                )

                all_valid = False

            else:

                print(
                    f"✅ Record {index}: "
                    f"{field} = {value} "
                    f"is within range."
                )

    if all_valid:
        print("\n✅ Value range validation passed.")
    else:
        print("\n❌ Value range validation failed.")

    return data


def value_range_menu(data):
    print("""
============================================================
📏 VALUE RANGE VALIDATION
============================================================

Enter rules in this format:

age:18:100

Multiple rules:

age:18:100,score:0:100

Nested fields are supported:

profile.age:18:100

============================================================
""")

    rules_input = input(
        "Range rules: "
    ).strip()

    if not rules_input:
        print("❌ No range rules provided.")
        return data

    range_rules = {}

    for rule in rules_input.split(","):

        parts = rule.split(":")

        if len(parts) != 3:

            print(
                f"❌ Invalid rule: {rule}"
            )
            continue

        field = parts[0].strip()

        try:
            minimum = float(parts[1].strip())
            maximum = float(parts[2].strip())
        except ValueError:

            print(
                f"❌ Invalid numeric range: {rule}"
            )
            continue

        if minimum > maximum:

            print(
                f"❌ Minimum cannot exceed maximum: "
                f"{rule}"
            )
            continue

        range_rules[field] = {
            "min": minimum,
            "max": maximum
        }

    if not range_rules:
        print("❌ No valid range rules provided.")
        return data

    validate_value_ranges(
        data,
        range_rules
    )

    return data


# ============================================================
# JSON EXPORT
# ============================================================

def export_json(data, filename):
    """Export current JSON data to a file."""

    try:

        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False
            )

        print(
            f"✅ JSON exported successfully: "
            f"{filename}"
        )

    except OSError as error:

        print(
            f"❌ Export failed: {error}"
        )


def export_json_menu(data):
    print("""
============================================================
💾 EXPORT JSON
============================================================

Enter a filename.

Example:

filtered_users.json

============================================================
""")

    filename = input(
        "Filename: "
    ).strip()

    if not filename:
        print("❌ Filename is required.")
        return data

    if not filename.lower().endswith(".json"):
        filename += ".json"

    export_json(
        data,
        filename
    )

    return data

# ============================================================
# COLORED PRETTY PRINT
# ============================================================

def colorize_json(value, indent=0):
    """Pretty print JSON with terminal colors."""

    RESET = "\033[0m"
    CYAN = "\033[36m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"

    spacing = " " * indent

    if isinstance(value, dict):

        lines = ["{"]

        items = list(value.items())

        for index, (key, item) in enumerate(items):

            comma = "," if index < len(items) - 1 else ""

            formatted = colorize_json(
                item,
                indent + 4
            )

            formatted_lines = formatted.split("\n")

            first_line = (
                " " * (indent + 4)
                + f"{CYAN}\"{key}\"{RESET}: "
                + formatted_lines[0].lstrip()
            )

            lines.append(
                first_line
                + (
                    "\n"
                    + "\n".join(
                        formatted_lines[1:]
                    )
                    if len(formatted_lines) > 1
                    else ""
                )
                + comma
            )

        lines.append(
            spacing + "}"
        )

        return "\n".join(lines)

    if isinstance(value, list):

        lines = ["["]

        for index, item in enumerate(value):

            comma = "," if index < len(value) - 1 else ""

            formatted = colorize_json(
                item,
                indent + 4
            )

            formatted_lines = formatted.split("\n")

            lines.append(
                " " * (indent + 4)
                + formatted_lines[0].lstrip()
                + (
                    "\n"
                    + "\n".join(
                        formatted_lines[1:]
                    )
                    if len(formatted_lines) > 1
                    else ""
                )
                + comma
            )

        lines.append(
            spacing + "]"
        )

        return "\n".join(lines)

    if isinstance(value, str):
        return f"{GREEN}\"{value}\"{RESET}"

    if isinstance(value, bool):
        return f"{YELLOW}{str(value).lower()}{RESET}"

    if value is None:
        return f"{BLUE}null{RESET}"

    return f"{YELLOW}{value}{RESET}"


def colored_pretty_print(data):
    print("""
============================================================
🎨 COLORED JSON
============================================================
""")

    print(
        colorize_json(data)
    )

    print(
        "\033[0m"
    )

    return data


# ============================================================
# TREE VISUALIZATION
# ============================================================

def print_json_tree(data, prefix="", name="ROOT"):
    """Display JSON data as a tree."""

    print(
        f"{prefix}📁 {name}"
    )

    if isinstance(data, dict):

        items = list(data.items())

        for index, (key, value) in enumerate(items):

            is_last = index == len(items) - 1

            branch = "└── " if is_last else "├── "
            next_prefix = prefix + (
                "    " if is_last else "│   "
            )

            if isinstance(value, (dict, list)):

                print_json_tree(
                    value,
                    prefix + branch,
                    key
                )

            else:

                print(
                    f"{prefix}{branch}"
                    f"🔹 {key}: {value}"
                )

    elif isinstance(data, list):

        for index, item in enumerate(data):

            is_last = index == len(data) - 1

            branch = "└── " if is_last else "├── "

            if isinstance(item, (dict, list)):

                print_json_tree(
                    item,
                    prefix + branch,
                    f"[{index}]"
                )

            else:

                print(
                    f"{prefix}{branch}"
                    f"🔹 [{index}]: {item}"
                )


def tree_visualization_menu(data):
    print("""
============================================================
🌳 JSON TREE
============================================================
""")

    print_json_tree(data)

    print(
        "\n============================================================"
    )

    return data

# ============================================================
# SUMMARY STATISTICS
# ============================================================

def collect_numeric_values(data, field):
    """Collect numeric values from JSON records."""

    if isinstance(data, list):
        records = data
    elif isinstance(data, dict):
        records = [data]
    else:
        return []

    values = []

    for record in records:

        if not isinstance(record, dict):
            continue

        value = get_nested_value(
            record,
            field
        )

        if isinstance(value, (int, float)) \
                and not isinstance(value, bool):

            values.append(value)

    return values


def summary_statistics(data):
    """Display summary statistics for numeric fields."""

    print("""
============================================================
📊 SUMMARY STATISTICS
============================================================
""")

    numeric_fields = set()

    def discover_fields(value, prefix=""):

        if isinstance(value, list):

            for item in value:
                discover_fields(
                    item,
                    prefix
                )

        elif isinstance(value, dict):

            for key, item in value.items():

                field_name = (
                    f"{prefix}.{key}"
                    if prefix
                    else key
                )

                if isinstance(item, (int, float)) \
                        and not isinstance(item, bool):

                    numeric_fields.add(
                        field_name
                    )

                elif isinstance(item, dict):

                    discover_fields(
                        item,
                        field_name
                    )

    discover_fields(data)

    if not numeric_fields:

        print("❌ No numeric fields found.")
        return data

    for field in sorted(numeric_fields):

        values = collect_numeric_values(
            data,
            field
        )

        if not values:
            continue

        count = len(values)
        total = sum(values)
        average = total / count
        minimum = min(values)
        maximum = max(values)

        print(
            f"Field: {field}"
        )

        print(
            f"  Count:   {count}"
        )

        print(
            f"  Sum:     {total}"
        )

        print(
            f"  Average: {average:.2f}"
        )

        print(
            f"  Minimum: {minimum}"
        )

        print(
            f"  Maximum: {maximum}"
        )

        print()

    return data


# ============================================================
# LARGE JSON FILE STREAMING
# ============================================================

def stream_json_array(filename):
    """
    Stream objects from a large top-level JSON array.

    This avoids loading the entire array into memory at once.
    """

    try:

        with open(
            filename,
            "r",
            encoding="utf-8"
        ) as file:

            decoder = json.JSONDecoder()

            buffer = ""
            started = False
            finished = False

            while not finished:

                chunk = file.read(8192)

                if not chunk:
                    break

                buffer += chunk

                while True:

                    buffer = buffer.lstrip()

                    if not started:

                        if not buffer.startswith("["):
                            raise ValueError(
                                "Streaming requires a "
                                "top-level JSON array."
                            )

                        buffer = buffer[1:]
                        started = True

                    buffer = buffer.lstrip()

                    if not buffer:
                        break

                    if buffer.startswith("]"):

                        finished = True
                        break

                    try:

                        item, index = decoder.raw_decode(
                            buffer
                        )

                    except json.JSONDecodeError:

                        break

                    yield item

                    buffer = buffer[index:]

                    buffer = buffer.lstrip()

                    if buffer.startswith(","):

                        buffer = buffer[1:]

                    elif buffer.startswith("]"):

                        finished = True
                        break

    except FileNotFoundError:

        print(
            f"❌ File not found: {filename}"
        )

    except Exception as error:

        print(
            f"❌ Streaming failed: {error}"
        )


def stream_json_menu():
    print("""
============================================================
🌊 LARGE JSON STREAMING
============================================================

This mode reads a large top-level JSON array incrementally
instead of loading the entire file into memory.

============================================================
""")

    filename = input(
        "JSON file: "
    ).strip()

    if not filename:
        print("❌ Filename is required.")
        return

    count = 0

    try:

        for item in stream_json_array(filename):

            count += 1

            if count <= 5:

                print(
                    f"\nRecord {count}:"
                )

                print(
                    json.dumps(
                        item,
                        indent=4,
                        ensure_ascii=False
                    )
                )

        print(
            f"\n✅ Streaming complete."
        )

        print(
            f"📦 Records processed: {count}"
        )

    except Exception as error:

        print(
            f"❌ Streaming failed: {error}"
        )

def create_sample_json(filename):

    sample_data = [
        {
            "id": "USER001",
            "name": "Damilola Ogunleye",
            "email": "dami@email.com",
            "age": 28,
            "address": {
                "city": "Lagos",
                "state": "Lagos",
                "country": "Nigeria"
            },
            "active": True
        },
        {
            "id": "USER002",
            "name": "Aisha Yusuf",
            "email": "aisha@email.com",
            "age": 32,
            "address": {
                "city": "Abuja",
                "state": "FCT",
                "country": "Nigeria"
            },
            "active": True
        },
        {
            "id": "USER003",
            "name": "John Smith",
            "email": "john@email.com",
            "age": 24,
            "address": {
                "city": "Lagos",
                "state": "Lagos",
                "country": "Nigeria"
            },
            "active": False
        }
    ]

    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            sample_data,
            file,
            indent=4,
            ensure_ascii=False
        )

# ============================================================
# AGGREGATIONS + GROUP BY
# ============================================================

def apply_aggregation(records, function, field=None):
    """Apply COUNT, SUM, AVG, MIN or MAX."""

    if function == "COUNT":
        return len(records)

    values = []

    for record in records:
        if field == "*" or field is None:
            value = record
        else:
            value = get_nested_value(record, field)

        if isinstance(value, (int, float)) and not isinstance(value, bool):
            values.append(value)

    if not values:
        return None

    if function == "SUM":
        return sum(values)

    if function == "AVG":
        return sum(values) / len(values)

    if function == "MIN":
        return min(values)

    if function == "MAX":
        return max(values)

    return None


def parse_aggregation(expression):
    """
    Parse:
        COUNT(*)
        SUM(age)
        AVG(age)
        MIN(age)
        MAX(age)
        SUM(age) AS total_age
    """

    pattern = re.compile(
        r"^\s*"
        r"(COUNT|SUM|AVG|MIN|MAX)"
        r"\s*\(\s*([^)]*)\s*\)"
        r"(?:\s+AS\s+([A-Za-z_][A-Za-z0-9_]*))?"
        r"\s*$",
        re.IGNORECASE
    )

    match = pattern.match(expression)

    if not match:
        return None

    function = match.group(1).upper()
    field = match.group(2).strip()
    alias = match.group(3)

    if not alias:
        if field == "*":
            alias = function.lower()
        else:
            alias = f"{function.lower()}_{field.replace('.', '_')}"

    return {
        "function": function,
        "field": field,
        "alias": alias
    }


def parse_advanced_select_query(query):
    """
    Parse queries such as:

        SELECT COUNT(*)
        SELECT SUM(age)
        SELECT SUM(age) AS total_age WHERE active = true
        SELECT address.city, COUNT(*) GROUP BY address.city
        SELECT address.city, AVG(age) GROUP BY address.city
        SELECT address.city, SUM(age) AS total_age
        WHERE address.city = 'Lagos'
        GROUP BY address.city
    """

    pattern = re.compile(
        r"^\s*SELECT\s+(.+?)"
        r"(?:\s+WHERE\s+(.+?))?"
        r"(?:\s+GROUP\s+BY\s+(.+?))?"
        r"\s*$",
        re.IGNORECASE
    )

    match = pattern.match(query)

    if not match:
        return None

    select_part = match.group(1).strip()
    where_part = match.group(2)
    group_part = match.group(3)

    fields = [
        field.strip()
        for field in select_part.split(",")
    ]

    return {
        "fields": fields,
        "where": where_part.strip() if where_part else None,
        "group_by": group_part.strip() if group_part else None
    }


def execute_advanced_query(data, query):
    """Execute aggregation and GROUP BY queries."""

    parsed = parse_advanced_select_query(query)

    if not parsed:
        print_error("Invalid advanced query.")
        return

    records = data

    if not isinstance(records, list):
        records = [records]

    # --------------------------------------------------------
    # WHERE
    # --------------------------------------------------------

    if parsed["where"]:
        records = [
            record
            for record in records
            if isinstance(record, dict)
            and evaluate_condition(
                record,
                parsed["where"]
            )
        ]

    fields = parsed["fields"]
    group_by = parsed["group_by"]

    # --------------------------------------------------------
    # GROUP BY
    # --------------------------------------------------------

    if group_by:

        groups = {}

        for record in records:

            if not isinstance(record, dict):
                continue

            group_value = get_nested_value(
                record,
                group_by
            )

            key = (
                json.dumps(
                    group_value,
                    sort_keys=True,
                    default=str
                )
            )

            if key not in groups:
                groups[key] = {
                    "value": group_value,
                    "records": []
                }

            groups[key]["records"].append(record)

        results = []

        for group in groups.values():

            result = {
                group_by: group["value"]
            }

            for field in fields:

                aggregation = parse_aggregation(field)

                if aggregation:

                    result[
                        aggregation["alias"]
                    ] = apply_aggregation(
                        group["records"],
                        aggregation["function"],
                        aggregation["field"]
                    )

            results.append(result)

        print(
            json.dumps(
                results,
                indent=4,
                ensure_ascii=False
            )
        )

        return results

    # --------------------------------------------------------
    # NORMAL AGGREGATION
    # --------------------------------------------------------

    aggregation_fields = []

    for field in fields:

        aggregation = parse_aggregation(field)

        if aggregation:
            aggregation_fields.append(
                aggregation
            )

    if aggregation_fields:

        result = {}

        for aggregation in aggregation_fields:

            result[
                aggregation["alias"]
            ] = apply_aggregation(
                records,
                aggregation["function"],
                aggregation["field"]
            )

        print(
            json.dumps(
                result,
                indent=4,
                ensure_ascii=False
            )
        )

        return result

    # --------------------------------------------------------
    # FALL BACK TO EXISTING SELECT QUERY
    # --------------------------------------------------------

    return execute_select_query(
        data,
        query
    )


def advanced_query_menu(data):
    while True:

        print("""
============================================================
📊 ADVANCED JSON QUERY
============================================================

Examples:

SELECT COUNT(*)

SELECT SUM(age)

SELECT AVG(age)

SELECT MIN(age)

SELECT MAX(age)

SELECT COUNT(*) WHERE active = true

SELECT SUM(age) WHERE active = true

SELECT address.city, COUNT(*) GROUP BY address.city

SELECT address.city, AVG(age) GROUP BY address.city

SELECT address.city, SUM(age) AS total_age
GROUP BY address.city

Type EXIT to return.

============================================================
""")

        query = input(
            "Advanced query: "
        ).strip()

        if query.upper() == "EXIT":
            break

        if not query:
            continue

        try:
            execute_advanced_query(
                data,
                query
            )
        except Exception as error:
            print(f"❌ Query failed: {error}")

def show_menu():
    print("""
============================================================
🔍 JSON READER
============================================================
1. Pretty Print JSON
2. JSON Summary
3. Dot Notation Query
4. Find All Occurrences of Key
5. JSONPath-like Query
6. Filter Array
7. Query Language
8. Aggregation + GROUP BY
9. Rename Keys
10. Extract Nested Value
11. Convert Array to Object
12. Add Computed Field
13. JSON Schema Validation
14. Required Fields Validation
15. Type Validation
16. Value Range Validation
17. Export JSON
18. Colored Pretty Print
19. Tree Visualization
20. Summary Statistics
21. Large JSON Streaming
22. Reload JSON File
0. Exit

============================================================
""")


def main():

    default_file = "users.json"

    filename = input(
        f"Enter path to JSON file [{default_file}]: "
    ).strip()

    if not filename:
        filename = default_file

    if not os.path.exists(filename):
        create_sample_json(filename)

        print(
            f"✅ Sample JSON created: {filename}"
        )

    data = load_json_file(filename)

    if data is None:
        return

    print(f"✅ Loaded JSON file: {filename}")

    while True:

        show_menu()

        choice = input(
            "\nChoose an option: "
        ).strip()

        if choice == "1":
            pretty_print(data)

        elif choice == "2":
            show_summary(data)

        elif choice == "3":
            dot_notation_query(data)

        elif choice == "4":
            find_key_menu(data)

        elif choice == "5":
            jsonpath_query(data)

        elif choice == "6":
            array_filter_menu(data)

        elif choice == "7":
            query_language_menu(data)

        elif choice == "8":

            advanced_query_menu(data)

        elif choice == "9":
        
            data = rename_keys_menu(data)

        elif choice == "10":
        
            data = extract_nested_menu(data)

        elif choice == "11":
        
            data = array_to_object_menu(data)

        elif choice == "12":
        
            data = computed_field_menu(data)

        elif choice == "13":
        
            data = schema_validation_menu(data)

        elif choice == "14":
        
            data = required_fields_menu(data)

        elif choice == "15":
        
            data = type_validation_menu(data)

        elif choice == "16":

            data = value_range_menu(data)

        elif choice == "17":
        
            data = export_json_menu(data)

        elif choice == "18":

            data = colored_pretty_print(data)

        elif choice == "19":
        
            data = tree_visualization_menu(data)

        elif choice == "20":
        
            data = summary_statistics(data)
        
        elif choice == "21":
        
            stream_json_menu()
        
        elif choice == "22":
        
            print("🔄 Reloading JSON file...")
            data = load_json_file("users.json")

        elif choice == "0":

            print(
                "\n👋 JSON Explorer closed."
            )

            break

        else:
            print("❌ Invalid option.")


if __name__ == "__main__":
    main()