# JSON Configuration Manager

## Difficulty

Mid

## Description

A command-line configuration manager that loads JSON configuration files, displays nested settings, allows values to be modified using dot notation, validates required fields, and saves changes with automatic backups.

## Features

* Loads configuration from a JSON file
* Displays nested configuration values using dot notation
* Navigates nested dictionaries
* Updates existing configuration values
* Creates new keys
* Creates new nested sections
* Converts user input to appropriate JSON data types
* Validates required configuration fields
* Creates a backup before saving
* Saves JSON with pretty printing
* Handles missing files
* Handles invalid JSON

## Example

```text
⚙️ CONFIGURATION MANAGER ⚙️
Loaded config from: config.json

Current settings:
database.host = localhost
database.port = 5432
database.credentials.username = admin
database.credentials.password = secret123
logging.level = INFO

Enter key to modify (or 'save' to save): database.port
Enter new value: 5433
✅ Updated database.port to 5433

Enter key to modify (or 'save' to save): logging.level
Enter new value: DEBUG
✅ Updated logging.level to DEBUG

Enter key to modify (or 'save' to save): save

📁 Saving config...
Backup created: config.json.bak
✅ Config saved successfully!
```

## Concepts

* JSON serialization and deserialization
* `json.load()`
* `json.dump()`
* Nested dictionaries
* Dot notation
* Recursive functions
* File handling
* Exception handling
* `FileNotFoundError`
* `JSONDecodeError`
* Data validation
* Type conversion
* Backup/versioning
* User input
* Formatted strings
