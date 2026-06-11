# Golden Master — D-LOC-01 (Entity · Logic Track)

pytest PASS 상태 확인 후 Golden Master만 구축해. `src/entity` 구현은 변경하지 마.

## 대상

| 항목 | 값 |
|------|-----|
| Phase | green |
| Layer | entity |
| Track | Logic |
| Test ID | **D-LOC-01** (FR-LOC-01 · `convert_meter_to_feet`) |
| 테스트 | `tests/entity/test_d_loc_01.py::test_d_loc_01_meter_to_feet` |
| Golden | `tests/golden/d_loc_01_g1_meter_to_feet.approved.txt` |

## 선행 조건

- `/green-minimal` 완료 — `test_d_loc_01_meter_to_feet` **PASS**
- `src/entity/convert_meter_to_feet.py` 존재
- `tests/conftest.py` — `meters_g1` = 2.5 (G1 SSOT)

선행 미충족 시 Golden Master 구축하지 말고 부족 항목만 보고.

## 작업 순서

### 1. `tests/_approval.py` — `assert_matches_golden(actual, relative)`

없으면 생성. 있으면 재사용.

| 동작 | 설명 |
|------|------|
| golden 루트 | `tests/golden/` |
| `UPDATE_GOLDEN=1` | approved 파일 갱신 (덮어쓰기) |
| 기본 | actual vs approved diff 비교 |
| 실패 | unified diff 출력 후 pytest fail |

### 2. 테스트에 golden 연결 — `tests/entity/test_d_loc_01.py`

| 단계 | 내용 |
|------|------|
| Given | `meters_g1` (= 2.5) |
| When | `convert_meter_to_feet(meters_g1)` |
| actual | `format_d_loc_01_golden(meters_g1, result)` — 테스트 파일 내 헬퍼 |
| Then | `assert_matches_golden(actual, "golden/d_loc_01_g1_meter_to_feet.approved.txt")` |

- 기존 `pytest.approx(8.2021)` assert는 **golden assert로 교체** (중복 assert 금지)

### 3. Golden 포맷 (고정 — 수동 편집으로 통과 우회 금지)

actual 문자열은 아래 **3줄**, 줄바꿈 LF, trailing newline 1개:

```
test_id: D-LOC-01
given_meters: {meters:.6f}
then_feet: {feet:.6f}
```

G1 예시:

```
test_id: D-LOC-01
given_meters: 2.500000
then_feet: 8.202100
```

SSOT: `METER_TO_FEET = 3.28084` → 2.5 × 3.28084 = 8.2021

### 4. 기준 파일 생성

bash:

```bash
UPDATE_GOLDEN=1 python -m pytest tests/entity/test_d_loc_01.py::test_d_loc_01_meter_to_feet -v
```

PowerShell:

```powershell
$env:UPDATE_GOLDEN=1; python -m pytest tests/entity/test_d_loc_01.py::test_d_loc_01_meter_to_feet -v
```

### 5. 검증 (UPDATE_GOLDEN 없음) → matched 확인

```bash
python -m pytest tests/entity/test_d_loc_01.py::test_d_loc_01_meter_to_feet -v
```

## ECB · Track 규칙

| 항목 | Logic Track |
|------|-------------|
| Domain Mock | **금지** |
| entity → boundary import | **금지** |
| E001~E005 emit | **금지** |
| golden 수동 편집 우회 | **금지** — `UPDATE_GOLDEN=1`로만 갱신 |
| approved 파일 위치 | `tests/golden/` 만 |

## 보고 형식

작업 후 아래만 짧게 보고:

1. golden 파일 경로 (`tests/golden/d_loc_01_g1_meter_to_feet.approved.txt`)
2. matched 여부
3. diff 있으면 내용 요약
4. pytest 최종 PASS/FAIL

## ARRR 위치

```
/red-test-plan → /red-skeleton → /green-minimal → /golden-master → /export
```

## 제약

- 커밋·push는 사용자가 요청할 때만
- `src/entity` 구현 변경 금지 (golden·테스트·`_approval.py`만)
- 한국어로 보고
