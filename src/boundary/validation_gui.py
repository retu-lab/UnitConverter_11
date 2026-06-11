import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QApplication,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from src.boundary.conversion_service import convert_all
from src.boundary.input_handler import InputHandler
from src.boundary.result_display import (
    format_conversion_lines,
    format_error,
    format_g1_verification,
)

G1_INPUT = "meter:2.5"
G1_EXPECTED_FEET = 8.2021
G1_EXPECTED_YARD = 2.734025
EXAMPLE_INPUTS = ("meter:2.5", "yard:12.5", "feet:8.2021")


class ValidationWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self._handler = InputHandler()
        self._setup_ui()

    def _setup_ui(self) -> None:
        self.setWindowTitle("UnitConverter_11 — 검증 GUI")
        self.setMinimumSize(560, 520)

        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setSpacing(12)

        root.addWidget(self._build_header())
        root.addWidget(self._build_input_group())
        root.addWidget(self._build_results_group())
        root.addWidget(self._build_verification_group())
        root.addWidget(self._build_status_bar())

    def _build_header(self) -> QWidget:
        title = QLabel("길이 단위 변환 검증 (meter / feet / yard)")
        title.setFont(QFont("", 14, QFont.Weight.Bold))
        subtitle = QLabel("입력 형식: unit:value — SSOT 비율 3.28084 / 1.09361")
        subtitle.setStyleSheet("color: #555;")

        wrapper = QWidget()
        box = QVBoxLayout(wrapper)
        box.addWidget(title)
        box.addWidget(subtitle)
        return wrapper

    def _build_input_group(self) -> QGroupBox:
        group = QGroupBox("입력")
        layout = QVBoxLayout(group)

        row = QHBoxLayout()
        self._input_field = QLineEdit()
        self._input_field.setPlaceholderText("meter:2.5")
        self._input_field.returnPressed.connect(self._on_convert)

        convert_btn = QPushButton("변환")
        convert_btn.setDefault(True)
        convert_btn.clicked.connect(self._on_convert)

        row.addWidget(QLabel("unit:value"))
        row.addWidget(self._input_field, stretch=1)
        row.addWidget(convert_btn)
        layout.addLayout(row)

        examples = QHBoxLayout()
        examples.addWidget(QLabel("예시:"))
        for sample in EXAMPLE_INPUTS:
            btn = QPushButton(sample)
            btn.clicked.connect(lambda _checked=False, s=sample: self._set_input(s))
            examples.addWidget(btn)
        examples.addStretch()
        layout.addLayout(examples)

        return group

    def _build_results_group(self) -> QGroupBox:
        group = QGroupBox("변환 결과")
        layout = QVBoxLayout(group)

        self._results_view = QTextEdit()
        self._results_view.setReadOnly(True)
        self._results_view.setFont(QFont("Consolas", 11))
        self._results_view.setPlaceholderText("변환 결과가 여기에 표시됩니다.")
        layout.addWidget(self._results_view)

        return group

    def _build_verification_group(self) -> QGroupBox:
        group = QGroupBox("테스트 픽스처 검증")
        layout = QVBoxLayout(group)

        grid = QGridLayout()
        grid.addWidget(QLabel("D-LOC-01 (G1)"), 0, 0)
        grid.addWidget(QLabel("입력: 2.5 meter"), 0, 1)
        grid.addWidget(QLabel(f"기대 feet: {G1_EXPECTED_FEET}"), 1, 0)
        grid.addWidget(QLabel(f"기대 yard: {G1_EXPECTED_YARD}"), 1, 1)

        g1_btn = QPushButton("G1 실행 (meter:2.5)")
        g1_btn.clicked.connect(self._on_run_g1)
        grid.addWidget(g1_btn, 2, 0, 1, 2)

        layout.addLayout(grid)

        self._verification_view = QTextEdit()
        self._verification_view.setReadOnly(True)
        self._verification_view.setMaximumHeight(110)
        self._verification_view.setFont(QFont("Consolas", 10))
        layout.addWidget(self._verification_view)

        return group

    def _build_status_bar(self) -> QFrame:
        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.StyledPanel)
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(8, 4, 8, 4)

        self._status_label = QLabel("준비")
        self._status_label.setStyleSheet("color: #2e7d32;")
        layout.addWidget(self._status_label)
        layout.addStretch()

        about_btn = QPushButton("U-IN 테스트")
        about_btn.clicked.connect(self._on_show_boundary_tests)
        layout.addWidget(about_btn)

        return frame

    def _set_input(self, text: str) -> None:
        self._input_field.setText(text)
        self._input_field.setFocus()

    def _on_convert(self) -> None:
        raw = self._input_field.text().strip()
        if not raw:
            self._show_error("입력값이 비어 있습니다.")
            return

        validation = self._handler.validate(raw)
        error_code = validation.get("error_code")
        if error_code:
            unit = validation.get("unit")
            self._show_error(format_error(error_code, unit))
            return

        unit = validation["unit"]
        value = validation["value"]
        results = convert_all(unit, value)
        lines = format_conversion_lines(unit, value, results)

        self._results_view.setPlainText("\n".join(lines))
        self._set_status(f"변환 완료 — {raw}", ok=True)

    def _on_run_g1(self) -> None:
        self._set_input(G1_INPUT)
        self._on_convert()

        results = convert_all("meter", 2.5)
        feet_ok = abs(results["feet"] - G1_EXPECTED_FEET) < 1e-4
        yard_ok = abs(results["yard"] - G1_EXPECTED_YARD) < 1e-4

        report = format_g1_verification(results["feet"], G1_EXPECTED_FEET)
        report += (
            f"\nD-LOC-02 G1 — Expected yard: {G1_EXPECTED_YARD:.6f}"
            f"  Actual: {results['yard']:.6f}"
            f"  {'PASS' if yard_ok else 'FAIL'}"
        )

        self._verification_view.setPlainText(report)
        all_pass = feet_ok and yard_ok
        self._set_status(
            "G1 픽스처 검증 PASS" if all_pass else "G1 픽스처 검증 FAIL",
            ok=all_pass,
        )

    def _on_show_boundary_tests(self) -> None:
        cases = [
            ("meter:abc", "E002", "U-IN-01"),
            ("unknown:1", "E003", "U-IN-02"),
            ("invalid", "E001", "형식 오류"),
        ]
        lines = ["Boundary 입력 검증 (InputHandler):"]
        for raw, expected_code, test_id in cases:
            result = self._handler.validate(raw)
            actual = result["error_code"]
            status = "PASS" if actual == expected_code else "FAIL"
            lines.append(f"  [{test_id}] {raw!r} → {actual} ({status})")

        QMessageBox.information(self, "Boundary 테스트", "\n".join(lines))

    def _show_error(self, message: str) -> None:
        self._results_view.setPlainText(message)
        self._set_status(message, ok=False)

    def _set_status(self, message: str, *, ok: bool) -> None:
        color = "#2e7d32" if ok else "#c62828"
        self._status_label.setStyleSheet(f"color: {color};")
        self._status_label.setText(message)


def main() -> int:
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = ValidationWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
