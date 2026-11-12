"""Behavioral tests for the generated storage.py and cache.py modules."""

import importlib.util
import sys
from collections.abc import Iterator
from pathlib import Path
from types import ModuleType

import pytest

from mcp_generator.templates.cache_middleware import generate_cache_middleware
from mcp_generator.templates.storage_backend import generate_storage_backend


def _load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def generated_modules(tmp_path: Path) -> Iterator[tuple[ModuleType, ModuleType]]:
    (tmp_path / "storage.py").write_text(generate_storage_backend(), encoding="utf-8")
    (tmp_path / "cache.py").write_text(generate_cache_middleware(), encoding="utf-8")
    storage = _load_module("storage", tmp_path / "storage.py")
    cache = _load_module("cache", tmp_path / "cache.py")
    yield storage, cache
    sys.modules.pop("storage", None)
    sys.modules.pop("cache", None)


async def test_cached_result_survives_filesystem_storage(
    generated_modules: tuple[ModuleType, ModuleType], tmp_path: Path
) -> None:
    storage_module, cache_module = generated_modules
    backend = storage_module.FilesystemStorage(storage_dir=str(tmp_path / "store"))
    cache = cache_module.get_cache_middleware(backend, default_ttl=300)
    calls: list[str] = []

    @cache.cached(ttl=600)
    async def lookup(param: str) -> dict[str, str]:
        calls.append(param)
        return {"param": param}

    assert await lookup("a") == {"param": "a"}
    assert await lookup("a") == {"param": "a"}
    assert calls == ["a"]
