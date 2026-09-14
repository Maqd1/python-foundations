# services.py
"""Example services wired by the DI container."""

from __future__ import annotations


class Database:
    def __init__(self, url: str = "postgresql://localhost:5432/mydb"):
        self.url = url

    def query(self, sql: str):
        print(f"   -> database.query({sql!r})")
        return {"id": 1, "name": "Damilola"}


class Logger:
    def __init__(self, level: str = "INFO"):
        self.level = level

    def info(self, msg: str):
        print(f"   -> logger.info({msg!r})")


class Cache:
    def __init__(self):
        self.data: dict = {}


class Router:
    def __init__(self):
        self.routes: list[tuple[str, str]] = []

    def add(self, path: str, method: str = "GET"):
        self.routes.append((method, path))


class UserService:
    def __init__(self, database: Database, logger: Logger):
        self.db = database
        self.logger = logger

    def get_user(self, uid: int):
        row = self.db.query(f"SELECT * FROM users WHERE id={uid}")
        self.logger.info(f"User {uid} fetched")
        return row


class APIService:
    """Depends on database, cache, router — matches the demo output."""

    def __init__(self, database: Database, cache: Cache, router: Router):
        self.db = database
        self.cache = cache
        self.router = router
        self.router.add("/users/{id}")
        self.router.add("/health")