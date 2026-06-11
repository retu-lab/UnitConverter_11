# UnitConverter_11

길이 단위(`단위:값`)를 입력받아 **meter / feet / yard** 간 변환 결과를 출력하는 프로그램. Mom Test에서 도출한 **변환 비율 정확성·숫자 판정 비용** 문제를 **Dual-Track TDD**로 구현한다.

![unit-converter](./unit-converter.jpg)

> **한 줄 요약:** `meter:2.5` 입력 시 SSOT 비율로 feet·yard를 **정확히** 변환하고, 새 단위 추가 시 기존 코드 변경을 최소화한다.

**상세 세션 기록:** [Report/03.MomTest-Report.md](Report/03.MomTest-Report.md) · [Report/04.CursorAI-Report.md](Report/04.CursorAI-Report.md)

---

## 빠른 시작

```bash
# 가상환경 생성·활성화 (Windows)
python -m venv venv
venv\Scripts\activate

# 실행 (현재 — 레거시 main)
python UnitConverter.py

# 테스트 (Track B RED/GREEN 진행 후)
python -m pytest tests/entity/ -v
```

| 명령 | 설명 |
|------|------|
| `python UnitConverter.py` | CLI 변환 (레거시 `main()` if-else) |
| `python -m pytest tests/entity/ -v` | Track B — Entity 변환 로직 |
| `python -m pytest tests/ -v` | 전체 회귀 (구조 확장 후) |

---

## 배경 (Mom Test)

인테리어 시공팀 현장 반장 페르소나에서 확인된 **진짜 문제**:

> 서로 다른 단위·기준(도면 yard / 견적 meter / 여유분 적용 순서)으로 치수를 손으로 맞추다 보니, **어느 숫자가 '맞는 값'인지 판단·재확인**에 시간이 크게 들고 발주·견적·현장 공유 숫자가 어긋난다.

| 성공 기준 | 요약 |
|-----------|------|
| SC-1 | 변환·확정 작업 **30분 이내** (현재: 예상 30분 → 약 4시간) |
| SC-2 | 기준이 다른 두 숫자(예: 11.43m vs 12.57m)를 **보내기 전에** 판정 |
| SC-3 | 견적 재발송·재설명 **0회** |
| SC-4 | yard / 순수 환산 meter / 여유 포함 meter **구분 전달** |

---

## 이번 릴리스 범위 (Dual-Track TDD)

| 포함 | 설명 |
|------|------|
| **ARRR** | Ask=RED → Respond=GREEN → Refine=REFACTOR → Repeat |
| **Track B (Logic)** | Entity — `FR-LOC-01` `convert_meter_to_feet` (D-LOC-01) |
| **Track A (UI)** | Boundary — CLI 입력·출력·입력검증 (후속) |
| **Command** | `/red-test-plan` → `/red-skeleton` → `/green-minimal` (도입 예정) |

### Dual-Track

| Track | Layer | Test ID | Mock | 테스트 경로 |
|-------|-------|---------|------|-------------|
| **B — Logic** | entity | `D-*` | Domain Mock **금지** | `tests/entity/` |
| **A — UI** | boundary | `U-*` | Domain Mock **허용** | `tests/boundary/` |

| 제외 (의도적·후속) | 이유 |
|-------------------|------|
| JSON/CSV 출력 | 추가 요구사항 — GREEN 이후 |
| 동적 단위 등록 (cubit) | OCP 검증 시나리오 — 별도 RED 묶음 |
| `UnitConverter.py` `main()` 리팩터 | boundary Track 후속 |

---

## 도메인 상수 (SSOT)

| 상수 | 값 | 출처 |
|------|-----|------|
| `METER_TO_FEET` | `3.28084` | README §비즈니스 로직 |
| `METER_TO_YARD` | `1.09361` | README §비즈니스 로직 |

- feet/yard 간 비율은 **meter 기준**으로 계산
- Mom Test: *"어떤 사이트는 3.28, 어떤 건 3.28084"* → 테스트·구현은 **3.28084 SSOT** (`src/entity/constants.py` 예정)
- 매직넘버 금지 — 상수 파일 단일 출처

---

## 핵심 API (Track B · Entity)

```python
def convert_meter_to_feet(meters: float) -> float: ...
```

| 항목 | 내용 |
|------|------|
| **FR-LOC-01** | `meter` 길이 값을 `feet`로 SSOT 비율 적용해 **정확히** 변환 |
| **Test ID** | **D-LOC-01** — G1 `2.5` → `8.2021` (= 2.5 × 3.28084) |
| **ECB** | entity는 boundary/control **import 금지**, **E001~E005 emit 금지** |

### G1 픽스처 SSOT (`tests/conftest.py` → `meters_g1`)

| 항목 | 값 |
|------|-----|
| 입력 | `2.5` meter (README `meter:2.5` 예시) |
| 기대 feet | `8.2021` |
| 기대 yard (후속 D-LOC-02) | `2.734025` (= 2.5 × 1.09361) |

---

## 기본 요구사항

1. 사용자 입력 예시:
   ```
   meter:2.5
   ```
   → 출력:
   ```
   2.5 meter = 8.2 feet
   2.5 meter = 2.7 yard
   ...
   ```

2. 현재 지원 단위: **meter**, **feet**, **yard**

3. 새 단위 추가 시 기존 코드 변경 **최소화** (OCP)

4. 단위 간 변환 **정확** — 테스트로 검증

### 품질 요구사항

- OCP — Converter 인터페이스, `main()` if-else 확장 금지
- SRP — 변환·입력검증·출력 클래스 분리
- 입력 검증 — 음수, 잘못된 형식, 없는 단위 (boundary Track)

### 추가 요구사항 (후속)

- **설정 외부화** — JSON/YAML 비율 로드
- **동적 단위 등록** — `1 cubit = 0.4572 meter`
- **출력 포맷** — JSON / CSV / 표

---

## 테스트 케이스

### Track B — Entity (Logic)

| ID | 설명 | Given → Then | 구현 |
|----|------|--------------|------|
| **D-LOC-01** | meter → feet | G1 `2.5` → `8.2021` | **RED 설계 완료** |
| D-LOC-02 | meter → yard | G1 `2.5` → `2.734025` | *(후속)* |
| D-VAL-01 | 음수 입력 | 음수 → 검증 실패 | *(boundary)* |

### Track A — Boundary (UI, 후속)

| ID | Given | Then |
|----|-------|------|
| U-IN-01 | `meter:abc` | 형식 오류 처리 |
| U-IN-02 | `unknown:1` | 없는 단위 처리 |

---

## 테스트 플랜 (D-LOC-01 · RED)

[ `/red-test-plan` 산출 — `tests/`·`src/` 미생성 ]

### C2C (Rule 1~3)

| FR | To-Do | Test ID | Given | When | Then |
|----|-------|---------|-------|------|------|
| FR-LOC-01 | G1에서 `convert_meter_to_feet`가 `8.2021` 반환 | D-LOC-01 | `meters_g1`=2.5 | `convert_meter_to_feet(...)` | `pytest.approx(8.2021)` |

### 실행 메타

| 항목 | 값 |
|------|-----|
| 파일 | `tests/entity/test_d_loc_01.py` |
| 함수 | `test_d_loc_01_meter_to_feet` |
| pytest | `python -m pytest tests/entity/test_d_loc_01.py::test_d_loc_01_meter_to_feet -v` |
| RED 묶음 | **D-LOC-01** 단독 |

### ECB · Mock

| 점검 | 결과 |
|------|------|
| Domain Mock 금지 | OK |
| entity → boundary import 금지 | OK |
| E001~E005 emit 금지 (Logic) | OK |
| Mom Test 비율 SSOT (3.28084) | OK |

---

## ARRR 실습 순서

```
/red-test-plan     # Ask — C2C·테스트 플랜 (파일 없음)
/red-skeleton      # Agent — pytest.fail 스켈레톤 (tests/만)
/green-minimal     # Agent — src/entity 최소 구현
/export            # Report + Prompting Transcript
```

### RED 설계 프롬프트 예시 (Track B)

```
/red-test-plan
Phase: red | Layer: entity | Track: Logic
이번 RED 묶음: D-LOC-01 (FR-LOC-01)
(표 4블록 작성, tests/·src/ 만들지 마)
```

---

## 프로젝트 구조 (목표)

```
UnitConverter_11/
├── .cursor/commands/       # /export 등
├── Report/                 # Mom Test · Cursor AI 보고서
├── Prompting/              # Export Transcript
├── src/
│   └── entity/
│       ├── constants.py    # METER_TO_FEET, METER_TO_YARD
│       └── convert_meter_to_feet.py
├── tests/
│   ├── conftest.py         # meters_g1
│   └── entity/             # D-LOC-01 …
├── UnitConverter.py        # 레거시 CLI (리팩터 대상)
└── README.md
```

---

## 브랜치 전략 (ARRR)

```
main → spec → red → green → refactoring
```

| 브랜치 | ARRR | 수정 범위 |
|--------|------|-----------|
| `spec` | 준비 | docs, .cursor/, Harness |
| `red` | Ask=RED | `tests/`만 |
| `green` | Respond | `src/` + 해당 tests |

---

## 문서

| 문서 | 설명 |
|------|------|
| [Report/01.MomTest-Report.md](Report/01.MomTest-Report.md) | Mom Test 워크북·인터뷰 |
| [Report/03.MomTest-Report.md](Report/03.MomTest-Report.md) | R-G-I-O·성공 기준 |
| [Report/04.CursorAI-Report.md](Report/04.CursorAI-Report.md) | Cursor 8계층·Test Loop |
| [Report/05.Command-Export-Report.md](Report/05.Command-Export-Report.md) | `/export` Command |

---

## 생성형AI를 활용한 Activities (6 시간)

1. 문제 코드 및 기본 요구사항 분석 (0.5시간)
   - 기본 코드구조, 로직 이해
2. 기본 요구사항 및 품질 요구사항 구현 (2시간)
   - OCP를 만족하는 인터페이스 구현
   - SRP를 만족하도록 클래스 구현
   - 입력값 검증을 위한 구현
3. TC 구현 (0.5시간)
   - 단위변환 기능 검증 및 입력 값 검증 TC 작성
4. 추가 요구사항 구현 (2시간)
   - 3개 요구사항 구현 및 TC 작성
5. 회고 및 발표 (1시간)
   - 실습 목표와 달성도
   - AI를 어떻게 활용했나? 도움이 된 순간과 한계는?
   - TC를 추가보면서 개선에 미친 영향, TC 작성 팁
   - 클린코드와 리팩토링에서 느낀 장점과 어려운점
