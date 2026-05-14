# 시스템 안정성 KPI 최종 디자인 사양 (V1.0)

## 1. 디자인 철학 및 목표
*   **철학:** 신뢰 기반 대시보드 (Trust-Based Dashboard). 데이터의 정확성과 시스템의 안정성을 최우선으로 시각화한다.
*   **목표:** 사용자가 단 몇 초 안에 시스템 상태(안정성)를 파악하고, 문제가 발생했을 때 즉각적인 조치 방향을 제시한다.

## 2. 컬러 팔레트 (Color Palette)
*   **Primary (Success/Stable):** `#4CAF50`
*   **Warning (Caution):** `#FFC107`
*   **Critical (Danger):** `#F44336`
*   **Background:** `#121212` (Dark Mode)

## 3. 핵심 KPI 시각화 상세 사양
### A. 오류율 (Error Rate)
*   **표시 형태:** 대형 원형 게이지(Gauge) + 추이 라인 차트(Trend Line).
*   **게이지 로직:** 전체 영역(0%~100%) 중 실제 오류율의 비율을 채움.
    *   Green: $\le 0.5\%$
    *   Amber: $0.5\% < \text{Error Rate} \le 1.0\%$
    *   Red: $> 1.0\%$
*   **차트 로직:** 지난 24시간/7일 간의 오류율 변화 추이를 선 그래프로 표시하여 안정성 흐름을 보여준다.

### B. 지연 시간 (Latency)
*   **표시 형태:** 시계형 게이지(Clock Gauge).
*   **게이지 로직:** 목표 지연 시간($T_{target}$) 대비 실제 지연 시간($T_{actual}$)의 상대적 위치를 표시한다.
    *   $T_{actual} \le T_{target} \times 1.05$: Green Zone (목표 달성 또는 약간 초과)
    *   $1.05 \times T_{target} < T_{actual} \le 1.20 \times T_{target}$: Amber Zone (주의 필요)
    *   $T_{actual} > 1.20 \times T_{target}$: Red Zone (심각한 지연 발생)

## 4. 레이아웃 및 컴포넌트 흐름
*   **섹션 제목:** "시스템 안정성 대시보드" (System Stability Dashboard)
*   **상단 배치:** 전체 시스템 안정성 점수 (Overall Stability Score: 95%)를 가장 큰 폰트로 표시.
*   **중앙 배치:** 오류율 및 지연 시간 게이지를 나란히 배치하여 즉각적인 비교가 가능하도록 한다. 각 KPI 아래에는 해당 상태에 따른 간단한 설명(예: "안정", "주의")을 명시한다.

## 5. 개발 우선순위 (Implementation Priority)
1.  **P1 (MVP):** 오류율/지연 시간의 현재 상태를 실시간으로 표시하는 색상 기반 게이지 컴포넌트 구현.
2.  **P2 (Data Integration):** 실제 API 데이터 스트림을 받아와 위 P1 컴포넌트에 동적으로 업데이트하는 로직 통합.
3.  **P3 (Visualization):** 과거 데이터를 활용하여 추이 라인 차트를 추가하고, 상태 변화에 따른 애니메이션 효과를 적용하여 시각적 임팩트 강화.
4.  **P4 (Actionable Feedback):** Critical 상태 발생 시 알림 및 상세 로그 링크 기능을 연결하여 사용자 행동을 유도.