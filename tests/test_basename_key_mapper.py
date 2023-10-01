from pathlib import Path
from typing import Iterable

import pytest

from dirct import BasenameKeyMapper, KeyMapper


@pytest.fixture
def files() -> Iterable[str]:
    return (
        "file_no_ext",
        "file_with_ext.ext",
        ".file_hidden_no_ext",
        ".file_hidden_with_ext.ext",
    )


@pytest.fixture
def subdirs() -> Iterable[str]:
    return (
        "dir_no_ext",
        "dir_with_ext.ext",
        ".dir_hidden_no_ext",
        ".dir_hidden_with_ext.ext",
    )


@pytest.fixture
def directory(tmp_path: Path, files: Iterable[str], subdirs: Iterable[str]) -> Path:
    d = tmp_path / "directory"
    d.mkdir()
    for f in files:
        (d / f).touch()
    for s in subdirs:
        (d / s).mkdir()
    return d


@pytest.fixture
def keymapper() -> KeyMapper:
    return BasenameKeyMapper()


def test_get_path(
    keymapper: KeyMapper,
    directory: Path,
    files: Iterable[str],
    subdirs: Iterable[str],
):
    for item in (*files, *subdirs):
        no_dot = item.lstrip(".")
        no_suffix = no_dot.removesuffix(".ext")
        assert keymapper.get_path(item, directory) == directory / item
        assert keymapper.get_path(no_dot, directory) == directory / item
        assert keymapper.get_path(no_suffix, directory) == directory / item
        assert keymapper.get_path(f".{no_dot}", directory) == directory / item
        assert keymapper.get_path(f".{no_suffix}", directory) == directory / item
        assert keymapper.get_path(f"{item}.foo", directory) == directory / item
        assert keymapper.get_path(f"{item}.foo.bar", directory) == directory / item
        assert keymapper.get_path(f".{no_suffix}.foo", directory) == directory / item


def test_get_path_missing(keymapper: KeyMapper, directory: Path):
    assert keymapper.get_path("missing", directory) is None
