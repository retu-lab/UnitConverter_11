from src.boundary.input_handler import InputHandler


def test_u_in_01_meter_abc_returns_e002():
    handler = InputHandler()
    result = handler.validate("meter:abc")
    assert result["error_code"] == "E002"
