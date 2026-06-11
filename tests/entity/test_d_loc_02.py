import pytest

from src.entity.convert_meter_to_yard import convert_meter_to_yard


def test_d_loc_02_meter_to_yard(meters_g1):
    result = convert_meter_to_yard(meters_g1)
    assert result == pytest.approx(2.734025)
