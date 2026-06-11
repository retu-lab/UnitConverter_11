from src.entity.convert_meter_to_feet import METER_TO_FEET, convert_meter_to_feet
from src.entity.convert_meter_to_yard import METER_TO_YARD, convert_meter_to_yard


def to_meters(unit: str, value: float) -> float:
    if unit == "meter":
        return value
    if unit == "feet":
        return value / METER_TO_FEET
    if unit == "yard":
        return value / METER_TO_YARD
    raise ValueError(f"Unknown unit: {unit}")


def convert_all(unit: str, value: float) -> dict[str, float]:
    meters = to_meters(unit, value)
    return {
        "meter": meters,
        "feet": convert_meter_to_feet(meters),
        "yard": convert_meter_to_yard(meters),
    }
