from src.boundary.conversion_service import convert_all
from src.boundary.input_handler import InputHandler
from src.boundary.result_display import format_conversion_lines, format_error
from src.entity.constants import G1_INPUT


def main():
    input_str = input(f"Insert value for converting (ex: {G1_INPUT}): ")
    validation = InputHandler().validate(input_str)

    error_code = validation.get("error_code")
    if error_code:
        print(format_error(error_code, validation.get("unit")))
        return

    unit = validation["unit"]
    value = validation["value"]
    results = convert_all(unit, value)
    for line in format_conversion_lines(unit, value, results):
        print(line)


if __name__ == "__main__":
    main()
