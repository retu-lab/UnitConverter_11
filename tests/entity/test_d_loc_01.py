from src.entity.convert_meter_to_feet import convert_meter_to_feet
from tests._approval import assert_matches_golden


def format_d_loc_01_golden(meters: float, feet: float) -> str:
    return (
        f"test_id: D-LOC-01\n"
        f"given_meters: {meters:.6f}\n"
        f"then_feet: {feet:.6f}\n"
    )


def test_d_loc_01_meter_to_feet(meters_g1):
    result = convert_meter_to_feet(meters_g1)
    actual = format_d_loc_01_golden(meters_g1, result)
    assert_matches_golden(actual, "golden/d_loc_01_g1_meter_to_feet.approved.txt")
