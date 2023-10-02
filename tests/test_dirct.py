from datetime import datetime
from pathlib import Path
from typing import Any

import pytest
import toml

from dirct import Dirct


@pytest.fixture
def self_data() -> dict[str, Any]:
    return {
        "name": "Dungeons, Dungeons, and More Dungeons",
        "release_date": datetime(2015, 10, 13, 0, 0, 0),
    }


@pytest.fixture
def publisher() -> dict[str, Any]:
    return {"name": "Probabilitor the Annoying", "founded": 2015}


@pytest.fixture
def version() -> str:
    return "1.0"


@pytest.fixture
def levels() -> dict[str, dict[str, Any]]:
    return {
        "castle.lvl.toml": {"level": "Castle"},
        "dungeon.lvl.toml": {"level": "Dungeon"},
        "forest.lvl.toml": {"level": "Forest"},
    }


@pytest.fixture
def exe() -> bytes:
    return bytes(range(256))


@pytest.fixture
def expected(
    self_data: dict[str, Any],
    publisher: dict[str, Any],
    version: str,
    levels: dict[str, dict[str, Any]],
    exe: bytes,
) -> dict[str, Any]:
    return {
        **self_data,
        "publisher.toml": publisher,
        "version": version,
        "levels": levels,
        "exe": exe,
    }


@pytest.fixture
def directory(
    tmp_path: Path,
    self_data: dict[str, Any],
    publisher: dict[str, Any],
    version: str,
    levels: dict[str, dict[str, Any]],
    exe: bytes,
) -> Path:
    base_dir = tmp_path / "directory"
    base_dir.mkdir()

    (base_dir / "__self__.toml").write_text(toml.dumps(self_data))
    (base_dir / "publisher.toml").write_text(toml.dumps(publisher))
    (base_dir / "version").write_text(version)
    (base_dir / "exe").write_bytes(exe)

    levels_dir = base_dir / "levels"
    levels_dir.mkdir()
    for name, data in levels.items():
        (levels_dir / name).write_text(toml.dumps(data))

    return base_dir


def test_dirct(directory: Path, expected: dict[str, Any]):
    assert Dirct(directory).to_dict() == expected
