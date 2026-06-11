SUPPORTED_UNITS = frozenset({"meter", "feet", "yard"})


class InputHandler:
    def validate(self, input_str: str) -> dict:
        if ":" not in input_str:
            return {"error_code": "E001"}

        unit, value_str = input_str.split(":", 1)

        try:
            float(value_str)
        except ValueError:
            return {"error_code": "E002"}

        if unit not in SUPPORTED_UNITS:
            return {"error_code": "E003"}

        return {"error_code": None, "unit": unit, "value": float(value_str)}
