import difflib
import os
from pathlib import Path

import pytest

_TESTS_DIR = Path(__file__).resolve().parent


def assert_matches_golden(actual: str, relative: str) -> None:
    approved_path = _TESTS_DIR / relative

    if os.environ.get("UPDATE_GOLDEN") == "1":
        approved_path.parent.mkdir(parents=True, exist_ok=True)
        approved_path.write_text(actual, encoding="utf-8", newline="\n")
        return

    if not approved_path.exists():
        pytest.fail(
            f"Golden file not found: {approved_path}\n"
            "Run with UPDATE_GOLDEN=1 to create it."
        )

    expected = approved_path.read_text(encoding="utf-8")
    if actual == expected:
        return

    diff = difflib.unified_diff(
        expected.splitlines(keepends=True),
        actual.splitlines(keepends=True),
        fromfile=f"approved/{approved_path.name}",
        tofile="actual",
    )
    pytest.fail("Golden mismatch:\n" + "".join(diff))
