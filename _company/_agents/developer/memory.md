# 💻 코다리 (시니어 풀스택 엔지니어) 개인 메모리

_코다리 에이전트만 읽고 쓰는 개인 노트. 학습·교훈·자주 쓰는 패턴이 누적됩니다._

## 학습 기록

- [2026-05-14] researcher가 정의한 Time-Series DB 구조 설계안과 데이터 요구사항을 기반으로, 파이썬 환경에서 실제 데이터를 수집하고 저장할 수 있는 초기 데이터 모델(스키마 초안)을 설계하세요. → 산출물 sessions/2026-05-14T01-54/developer.md
- [2026-05-14] Researcher가 정의한 Time-Series DB 구조 설계안과 데이터 요구사항을 기반으로, 키움 RestApi에서 실시간 주식 데이터를 수집하고 저장할 수 있는 초기 Python 데이터 모델(`StockTimeSeriesData` 클래스) 구현 및 F1(실시간 데이터 수집) 모듈 개발을 시작하라. → 산출물 sessions/2026-05-14T02-24/developer.md
- [2026-05-14] 📁 💻 코다리 파일 액션: ⚠️ 읽기 실패: sessions/2026-05-14T01-54/developer.md — 파일이 존재하지 않습니다.  <- 해당 문제 sessions 폴더는 _company 폴더 안에 sessions 폴더 참조해 → 산출물 sessions/2026-05-14T02-38/developer.md
- [2026-05-14] 이전 세션에서 정의된 Time-Series DB 구조와 StockTimeSeriesData 클래스를 기반으로, 키움 RestApi에서 실시간 주식 데이터를 수집하여 저장하는 F1 모듈의 코드를 재점검하고 오류 없이 완성하라. 파일 경로 문제를 해결하고 진행한다. → 산출물 sessions/2026-05-14T02-39/developer.md
- [2026-05-14] Researcher가 정의한 Feature Set(상승예측, 급등예측, 현재강성주 파악 관련 지표)을 기반으로, StockTimeSeriesData 클래스에 저장된 데이터를 활용하여 실시간 주식 검색 알고리즘의 핵심 예측 로직(F2 지표 계산 및 초기 학습 루프)을 구현하고 테스트할 코드를 작성하라. 파일 경로는 '_company/sessions/'를 기준으로 참조해야 한다. → 산출물 sessions/2026-05-14T03-09/developer.md
- [2026-05-14] f2_predictor.py에 실시간 데이터 기반 백테스팅 루프를 통합하여 예측 결과의 통계적 유효성을 확보하고, 오류 없이 실행되도록 코드를 수정 및 테스트하라. → 산출물 sessions/2026-05-14T03-39/developer.md