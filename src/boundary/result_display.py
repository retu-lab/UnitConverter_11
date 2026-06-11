ERROR_MESSAGES = {
    "E001": "형식 오류 — unit:value 형식으로 입력하세요 (예: meter:2.5)",
    "E002": "숫자 오류 — 값은 숫자여야 합니다",
    "E003": "단위 오류 — 지원 단위: meter, feet, yard",
}


def format_error(error_code: str, unit: str | None = None) -> str:
    message = ERROR_MESSAGES.get(error_code, f"오류 ({error_code})")
    if error_code == "E003" and unit:
        return f"{message} (입력: {unit})"
    return message


def format_conversion_lines(
    source_unit: str, source_value: float, results: dict[str, float]
) -> list[str]:
    lines: list[str] = []
    for target_unit in ("meter", "feet", "yard"):
        value = results[target_unit]
        lines.append(f"{source_value:g} {source_unit} = {value:.4f} {target_unit}")
    return lines


def format_g1_verification(actual_feet: float, expected_feet: float = 8.2021) -> str:
    delta = abs(actual_feet - expected_feet)
    passed = delta < 1e-4
    status = "PASS" if passed else "FAIL"
    return (
        f"D-LOC-01 G1 검증 — Given: 2.5 meter\n"
        f"  Expected feet: {expected_feet:.4f}\n"
        f"  Actual feet:   {actual_feet:.4f}\n"
        f"  Status: {status}"
    )
