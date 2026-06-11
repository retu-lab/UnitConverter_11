from src.boundary.input_handler import InputHandler


def test_u_in_02_unknown_unit_returns_e003():
    handler = InputHandler()
    result = handler.validate("unknown:1")
    assert result["error_code"] == "E003"
