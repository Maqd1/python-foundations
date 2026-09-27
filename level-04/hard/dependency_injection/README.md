# The Dependency Injection Container (Very Hard)

Create a dependency injection container that manages object creation and dependencies.

## Requirements:

1. Dependency Injection Container (container.py):

    Create container.py that implements a DI container:

    container = Container()

    container.register("database", Database)
    container.register("logger", Logger)
    container.register(
        "service",
        MyService,
        dependencies=["database", "logger"]
    )


2. Features:

    Register classes with dependencies

    Resolve dependencies automatically

    Support singleton and transient lifetimes

    Handle circular dependency detection


3. Service Registration:

    @container.register("user_service")
    class UserService:
        def __init__(self, db: Database, logger: Logger):
            self.db = db
            self.logger = logger


4. Dependency Resolution:

    service = container.resolve("user_service")

    # Automatically creates Database, Logger, and UserService


5. Configuration:

    Load configuration from JSON

    Override implementations for testing

    Environment-specific configurations


6. Advanced Features:

    Factory functions for complex creation

    Tagging services (e.g., "api" tag)

    Lifecycle hooks (on_create, on_destroy)

    Scope management (request scope, thread scope)


Sample Output:

🔌 DEPENDENCY INJECTION CONTAINER 🔌

Registering services...

✅ Registered: database (singleton)
✅ Registered: logger (transient)
✅ Registered: user_service (singleton)
  Dependencies: database, logger

## Container info:

📦 Registered services: 12
🔗 Dependencies: 18
🏷️ Tags: ["database", "api", "service"]

Resolving user_service...

✅ Created database (singleton)
✅ Created logger (transient)
✅ Created user_service

Test call:

user_service.get_user(1)

   -> database.query("SELECT * FROM users WHERE id=1")
   -> logger.info("User 1 fetched")
   -> Return: {"id": 1, "name": "Damilola"}

Configuration loaded:

{
    "database": {
        "url": "postgresql://localhost:5432/mydb",
        "pool_size": 10
    },
    "logging": {
        "level": "INFO",
        "file": "app.log"
    }
}

Creating API service with dependencies:

API Service (singleton)
  -> Database: singleton
  -> Cache: singleton
  -> Router: transient

Circular dependency detected!

   ❌ ServiceA -> ServiceB -> ServiceA

   💡 Suggestion: Use lazy loading or redesign dependencies


## Concepts Tested:

- Advanced OOP
- Metaclasses
- Dependency injection
- Registry pattern
- Singleton pattern
- Factory pattern
- Configuration management
- Error detection