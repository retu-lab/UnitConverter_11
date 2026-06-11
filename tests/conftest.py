import pytest

from src.entity.constants import METERS_G1


@pytest.fixture
def meters_g1() -> float:
    return METERS_G1
