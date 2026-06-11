# 세션 Export — Report + Prompting Transcript

이번 대화(세션) 내용을 정리해서 **두 파일**을 생성해줘.

## 저장 위치·이름 규칙

| 산출물 | 경로·형식 | 예시 |
|--------|-----------|------|
| 보고서 | `Report/NN.<주제>-Report.md` | `05.OCP-Refactor-Report.md` |
| Transcript | `Prompting/NN.Export-Transcript.md` | `05.Export-Transcript.md` |

- `NN` = 두 자리 번호 (01, 02, 03 …)
- **Report와 Prompting은 같은 NN**을 사용
- 채팅에서 번호를 따로 적었다면 그 번호 사용 (예: `/export 05`)
- 번호가 없으면 `Report/`, `Prompting/` 폴더를 스캔해 **가장 큰 번호 + 1**을 사용
- 기존 파일을 덮어쓰지 말 것 (명시적으로 "덮어써"라고 하지 않는 한)

## Report 작성 지침

기존 스타일 참고: `Report/01.MomTest-Report.md`, `Report/04.CursorAI-Report.md`

포함할 내용:
- 제목: `# UnitConverter_11 — STEP N <주제> 보고서` (또는 세션에 맞는 제목)
- 선행 세션·관련 Report 링크 (있을 때)
- 세션 목표·핵심 결론 요약
- 결정 사항·산출물·체크리스트 (표 활용)
- 다음 단계 (있을 때)

## Prompting (Export Transcript) 작성 지침

기존 스타일 참고: `Prompting/01.Export-Transcript.md`, `Prompting/04.Export-Transcript.md`

포함할 내용:
- 헤더: 프로젝트, 단계, 선행 세션, 브랜치(해당 시)
- Turn별 구분: `## Turn N — <제목>`
- **User:** 사용자가 입력한 프롬프트 (코드 블록으로 원문 또는 핵심 유지)
- **Assistant (요약 출력):** Agent 응답·작업 결과 요약 (bullet)
- 부록: 복사용 프롬프트 모음 (해당 시)

## 작업 순서

1. `Report/`, `Prompting/` 목록 확인 → NN 결정
2. 이번 대화 전체 맥락에서 Report 작성
3. Turn 순서대로 Transcript 작성
4. 파일 생성 후 **생성한 경로 2개만** 짧게 알려줘

## 제약

- 커밋·push는 사용자가 요청할 때만
- 대화에 없는 내용을 지어내지 말 것
- 한국어로 작성
