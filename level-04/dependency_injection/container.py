# container.py
"""Core dependency injection container."""

from __future__ import annotations

import inspect
import threading
from collections import defaultdict
from contextlib import contextmanager
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Iterable, Optional


class Lifetime(Enum):
    SINGLETON = "singleton"
    TRANSIENT = "transient"
    SCOPED = "scoped"


class Scope(Enum):
    GLOBAL = "global"
    REQUEST = "request"
    THREAD = "thread"


class ContainerError(Exception): ...
class CircularDependencyError(ContainerError):
    def __init__(self, chain: list[str]):
        self.chain = chain
        super().__init__(f"Circular dependency detected: {' -> '.join(chain)}")


class ServiceNotFoundError(ContainerError): ...


@dataclass
class Registration:
    name: str
    factory: Callable[..., Any]
    lifetime: Lifetime = Lifetime.SINGLETON
    dependencies: list[str] = field(default_factory=list)
    tags: set[str] = field(default_factory=set)
    scope: str = Scope.GLOBAL.value
    on_create: Optional[Callable[[Any], None]] = None
    on_destroy: Optional[Callable[[Any], None]] = None
    is_class: bool = False
    instance: Any = None
    _has_instance: bool = False


class Container:
    def __init__(self, config: Optional[dict] = None, parent: Optional["Container"] = None):
        self._registrations: dict[str, Registration] = {}
        self._tags: dict[str, set[str]] = defaultdict(set)
        self._config: dict = config or {}
        self._parent = parent
        self._lock = threading.RLock()
        self._scope_instances: dict[str, dict[str, Any]] = defaultdict(dict)
        self._thread_local = threading.local()

    # ---------- Registration ----------
    def register(
        self,
        name: str,
        factory: Optional[Callable[..., Any]] = None,
        *,
        lifetime: Lifetime | str = Lifetime.SINGLETON,
        dependencies: Optional[list[str]] = None,
        tags: Optional[Iterable[str]] = None,
        scope: str = Scope.GLOBAL.value,
        on_create: Optional[Callable[[Any], None]] = None,
        on_destroy: Optional[Callable[[Any], None]] = None,
    ):
        def _do(target):
            lt = Lifetime(lifetime) if isinstance(lifetime, str) else lifetime
            deps = list(dependencies) if dependencies is not None else self._infer_dependencies(target)
            reg = Registration(
                name=name, factory=target, lifetime=lt,
                dependencies=deps, tags=set(tags or ()),
                scope=scope, on_create=on_create, on_destroy=on_destroy,
                is_class=inspect.isclass(target),
            )
            with self._lock:
                self._registrations[name] = reg
                for t in reg.tags:
                    self._tags[t].add(name)
            return target

        return _do if factory is None else _do(factory)

    def register_instance(self, name: str, instance: Any, *, tags: Optional[Iterable[str]] = None):
        reg = Registration(
            name=name, factory=lambda: instance,
            lifetime=Lifetime.SINGLETON, tags=set(tags or ()),
            instance=instance, _has_instance=True,
        )
        with self._lock:
            self._registrations[name] = reg
            for t in reg.tags:
                self._tags[t].add(name)
        return instance

    def register_factory(
        self, name: str, factory: Callable[..., Any], *,
        lifetime: Lifetime | str = Lifetime.TRANSIENT,
        dependencies: Optional[list[str]] = None,
        tags: Optional[Iterable[str]] = None,
        scope: str = Scope.GLOBAL.value,
    ):
        return self.register(
            name, factory, lifetime=lifetime,
            dependencies=dependencies, tags=tags, scope=scope,
        )

    # ---------- Resolution ----------
    def resolve(self, name: str, *, scope: Optional[str] = None) -> Any:
        with self._lock:
            return self._resolve(name, chain=[], scope=scope)

    def _resolve(self, name: str, chain: list[str], scope: Optional[str]) -> Any:
        if name not in self._registrations and self._parent is not None:
            return self._parent._resolve(name, chain, scope)
        if name not in self._registrations:
            raise ServiceNotFoundError(f"Service not registered: {name}")
        if name in chain:
            raise CircularDependencyError(chain + [name])

        reg = self._registrations[name]
        active_scope = scope or reg.scope

        if reg.lifetime is Lifetime.SINGLETON and reg._has_instance:
            return reg.instance
        if reg.lifetime is Lifetime.SCOPED:
            store = self._get_scope_store(active_scope)
            if name in store:
                return store[name]

        chain.append(name)
        try:
            kwargs = {dep: self._resolve(dep, chain, scope) for dep in reg.dependencies}
        finally:
            chain.pop()

        instance = self._create_instance(reg, kwargs)
        if reg.on_create:
            reg.on_create(instance)

        if reg.lifetime is Lifetime.SINGLETON:
            reg.instance = instance
            reg._has_instance = True
        elif reg.lifetime is Lifetime.SCOPED:
            self._get_scope_store(active_scope)[name] = instance
        return instance

    def _create_instance(self, reg: Registration, kwargs: dict) -> Any:
        if reg.is_class:
            # Classes: always keyword args (only pass what __init__ accepts)
            sig = inspect.signature(reg.factory)
            accepted = {
                p.name for p in sig.parameters.values()
                if p.kind in (p.POSITIONAL_OR_KEYWORD, p.KEYWORD_ONLY)
            }
            filtered = {k: v for k, v in kwargs.items() if k in accepted}
            return reg.factory(**filtered)
        # Non-class factories: kwargs if provided, else no args
        return reg.factory(**kwargs) if kwargs else reg.factory()

    def _get_scope_store(self, scope: str) -> dict:
        if scope == Scope.THREAD.value:
            if not hasattr(self._thread_local, "store"):
                self._thread_local.store = {}
            return self._thread_local.store
        return self._scope_instances[scope]

    @contextmanager
    def scope(self, name: str):
        scoped = _ScopedContainer(self, name)
        try:
            yield scoped
        finally:
            store = self._scope_instances.get(name, {})
            for svc_name, inst in list(store.items()):
                reg = self._registrations.get(svc_name)
                if reg and reg.on_destroy:
                    try:
                        reg.on_destroy(inst)
                    except Exception:
                        pass
            self._scope_instances.pop(name, None)

    # ---------- Introspection ----------
    def is_registered(self, name: str) -> bool:
        return name in self._registrations or (
            self._parent is not None and self._parent.is_registered(name)
        )

    def get_registration(self, name: str) -> Registration:
        if name not in self._registrations:
            raise ServiceNotFoundError(name)
        return self._registrations[name]

    def services(self) -> list[str]:
        names = set(self._registrations)
        if self._parent:
            names |= set(self._parent.services())
        return sorted(names)

    def by_tag(self, tag: str) -> list[str]:
        names = set(self._tags.get(tag, ()))
        if self._parent:
            names |= set(self._parent.by_tag(tag))
        return sorted(names)

    def all_tags(self) -> list[str]:
        tags = set(self._tags)
        if self._parent:
            tags |= set(self._parent.all_tags())
        return sorted(tags)

    def dependency_count(self) -> int:
        return sum(len(r.dependencies) for r in self._registrations.values())

    def info(self) -> dict:
        return {
            "services": len(self.services()),
            "dependencies": self.dependency_count(),
            "tags": self.all_tags(),
        }

    # ---------- Config (basic in-memory; see config.py for file loading) ----------
    @property
    def config(self) -> dict:
        if self._parent is not None:
            merged = dict(self._parent.config)
            merged.update(self._config)
            return merged
        return dict(self._config)

    def load_config_dict(self, data: dict) -> None:
        self._config.update(data)

    def get_config(self, key: str, default: Any = None) -> Any:
        return self.config.get(key, default)

    # ---------- Testing ----------
    def override(self, name: str, factory: Callable[..., Any] | Any) -> None:
        if not callable(factory):
            self.register_instance(name, factory)
            return
        existing = self._registrations.get(name)
        self.register(
            name, factory,
            dependencies=existing.dependencies if existing else None,
            tags=existing.tags if existing else None,
        )

    @contextmanager
    def override_context(self, overrides: dict[str, Any]):
        saved = {k: self._registrations.get(k) for k in overrides}
        try:
            for name, val in overrides.items():
                self.override(name, val)
            yield self
        finally:
            for name, reg in saved.items():
                if reg is None:
                    self._registrations.pop(name, None)
                else:
                    self._registrations[name] = reg

    # ---------- Helpers ----------
    @staticmethod
    def _infer_dependencies(target: Callable) -> list[str]:
        try:
            sig = inspect.signature(target)
        except (TypeError, ValueError):
            return []
        deps = []
        for pname, param in sig.parameters.items():
            if pname == "self":
                continue
            if param.kind in (param.VAR_POSITIONAL, param.VAR_KEYWORD):
                continue
            if param.default is not inspect.Parameter.empty:
                continue
            deps.append(pname)
        return deps


class _ScopedContainer:
    def __init__(self, parent: Container, scope_name: str):
        self._parent = parent
        self._scope = scope_name

    def resolve(self, name: str) -> Any:
        return self._parent.resolve(name, scope=self._scope)

    def __getattr__(self, item):
        return getattr(self._parent, item)