from src.entity.constants import METER_TO_FEET, METER_TO_YARD
from src.entity.convert_meter_to_feet import convert_meter_to_feet
from src.entity.convert_meter_to_yard import convert_meter_to_yard

_UNIT_TO_METERS_DIVISOR = {
    "meter": 1.0,
    "feet": METER_TO_FEET,
    "yard": METER_TO_YARD,
}


def to_meters(unit: str, value: float) -> float:
    divisor = _UNIT_TO_METERS_DIVISOR.get(unit)
    if divisor is None:
        raise ValueError(f"Unknown unit: {unit}")
    return value / divisor


def convert_all(unit: str, value: float) -> dict[str, float]:
    meters = to_meters(unit, value)
    return {
        "meter": meters,
        "feet": convert_meter_to_feet(meters),
        "yard": convert_meter_to_yard(meters),
    }
