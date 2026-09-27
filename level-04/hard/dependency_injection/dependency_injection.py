from __future__ import annotations

'''
Q7: The Dependency Injection Container (Very Hard)

Create a dependency injection container that manages object creation and dependencies.

Requirements:

    Create container.py that implements a DI container:
    python

    container = Container()
    container.register("database", Database)
    container.register("logger", Logger)
    container.register("service", MyService, dependencies=["database", "logger"])

    Features:

        Register classes with dependencies

        Resolve dependencies automatically

        Support singleton and transient lifetimes

        Handle circular dependency detection

    Service Registration:
    python

    @container.register("user_service")
    class UserService:
        def __init__(self, db: Database, logger: Logger):
            self.db = db
            self.logger = logger

    Dependency Resolution:
    python

    service = container.resolve("user_service")
    # Automatically creates Database, Logger, and UserService

    Configuration:

        Load configuration from JSON

        Override implementations for testing

        Environment-specific configurations

    Advanced Features:

        Factory functions for complex creation

        Tagging services (e.g., "api" tag)

        Lifecycle hooks (on_create, on_destroy)

        Scope management (request scope, thread scope)

Sample Output:
text

🔌 DEPENDENCY INJECTION CONTAINER 🔌

Registering services...
✅ Registered: database (singleton)
✅ Registered: logger (transient)
✅ Registered: user_service (singleton)
  Dependencies: database, logger

Container info:
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

Concepts: Advanced OOP, metaclasses, dependency injection, registry pattern, singleton pattern, factory pattern, configuration management, error detection
'''


# container.py
"""
Dependency Injection Container
Supports: register, resolve, singletons, transients, factories,
tags, lifecycle hooks, scopes, config loading, circular detection.
"""


# dependency_injection.py
"""Demo entry point wiring the DI container together."""


import json

from container import (
    Container,
    CircularDependencyError,
)
from services import Database, Logger, Cache, Router, UserService, APIService


def build_container() -> Container:
    c = Container()

    print("Registering services...")

    c.register("database", Database, lifetime="singleton", tags=["db", "api"])
    c.register("logger",   Logger,   lifetime="transient", tags=["logging"])
    c.register("cache",    Cache,    lifetime="singleton", tags=["api"])
    c.register("router",   Router,   lifetime="transient", tags=["api"])

    @c.register("user_service", lifetime="singleton", tags=["service"])
    class _UserService(UserService):
        pass

    c.register(
        "api_service", APIService,           # ← proper class that accepts all 3
        lifetime="singleton",
        dependencies=["database", "cache", "router"],
        tags=["api", "service"],
    )
    return c


def print_registrations(c: Container) -> None:
    for name in c.services():
        reg = c.get_registration(name)
        print(f"✅ Registered: {name} ({reg.lifetime.value})")
        if reg.dependencies:
            print(f"  Dependencies: {', '.join(reg.dependencies)}")


def main() -> None:
    print("🔌 DEPENDENCY INJECTION CONTAINER 🔌\n")

    container = build_container()
    print()
    print_registrations(container)

    info = container.info()
    print("\nContainer info:")
    print(f"📦 Registered services: {info['services']}")
    print(f"🔗 Dependencies: {info['dependencies']}")
    print(f"🏷️ Tags: {info['tags']}\n")

    # ---- Resolve ----
    print("Resolving user_service...")
    svc: UserService = container.resolve("user_service")
    print("✅ Created user_service\n")

    print("Test call:")
    print("user_service.get_user(1)")
    result = svc.get_user(1)
    print(f"   -> Return: {result}\n")

    # ---- Configuration ----
    sample_config = {
        "database": {"url": "postgresql://localhost:5432/mydb", "pool_size": 10},
        "logging": {"level": "INFO", "file": "app.log"},
    }
    container.load_config_dict(sample_config)
    print("Configuration loaded:")
    print(json.dumps(sample_config, indent=4))
    print()

    # ---- API service ----
    print("Creating API service with dependencies:")
    reg = container.get_registration("api_service")
    print(f"API Service ({reg.lifetime.value})")
    for dep in reg.dependencies:
        d = container.get_registration(dep)
        print(f"  -> {dep.capitalize()}: {d.lifetime.value}")
    api = container.resolve("api_service")
    print(f"  -> Router routes: {api.router.routes}\n")

    # ---- Circular dependency demo ----
    print("Circular dependency detected!")
    c2 = Container()
    c2.register("ServiceA", lambda serviceb: None, dependencies=["ServiceB"])
    c2.register("ServiceB", lambda servicea: None, dependencies=["ServiceA"])
    try:
        c2.resolve("ServiceA")
    except CircularDependencyError as e:
        print(f"   ❌ {' -> '.join(e.chain)}")
        print("   💡 Suggestion: Use lazy loading or redesign dependencies")


if __name__ == "__main__":
    main()