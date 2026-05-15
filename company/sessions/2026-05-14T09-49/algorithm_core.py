# -*- coding: utf-8 -*-
"""
주식 예측 알고리즘의 핵심 로직 모듈 (Algorithm Core Module)
시스템 안정성(PTI) 및 리스크 헷지(Risk Hedge) 통합을 최우선으로 고려하여 설계합니다.
"""

import json
from datetime import datetime
import pandas as pd

# 시스템 안전장치 및 KPI 참조
SYSTEM_SAFE_MODE = False  # 데이터 무결성 실패 시 시스템 정지 플래그
MDD_LIMIT = 0.05          # 최대 허용 손실률 (5%)
SR_TARGET = 0.03          # 목표 수익률 (3%)

class RiskHedgeModule:
    """
    예측 결과에 따른 자동 실행/정지 로직을 관리하는 모듈.
    시스템 안정성 지수(PTI)와 수익률(ROI) 연관성을 반영합니다.
    """
    def __init__(self, pti_score: float):
        self.pti = pti_score
        self.risk_status = "NORMAL"

    def check_stability(self, current_roi: float, mdd: float) -> bool:
        """시스템 안정성 및 리스크 기준을 점검합니다."""
        if self.pti < 50:
            print("🚨 경고: 시스템 안정성 지수(PTI)가 50 이하입니다. 안전 모드 진입 준비.")
            return False  # 불안정하면 즉시 실행 금지

        if current_roi < SR_TARGET:
            print(f"⚠️ 주의: 현재 ROI({current_roi:.2%})가 목표치({SR_TARGET:.2%}) 미달입니다. 리스크 헷지 활성화 고려.")
            return True # 리스크 헷지 활성화

        if mdd > MDD_LIMIT:
            print(f"🛑 위험: MDD({mdd:.2%})가 허용 한계({MDD_LIMIT:.2%})를 초과했습니다. 자동 실행 정지.")
            return False # 리스크 초과 시 즉시 중단

        return True # 안정적이며 목표 범위 내

    def execute_hedge_logic(self, prediction_result: dict) -> str:
        """실제 헷지 로직을 실행합니다 (Case A, B, C 통합)."""
        if not self.check_stability(prediction_result['roi'], prediction_result['mdd']):
            return "HALT"  # 안정성 문제 발생 시 즉시 정지

        # Case A: 상승 예측 기반 실행
        if prediction_result['type'] == 'RISE':
            action = f"ACTION_BUY_{prediction_result['symbol']} (Confidence: {prediction_result['confidence']:.2f})"
        # Case B: 급등 예측 기반 실행
        elif prediction_result['type'] == 'SURGE':
            action = f"ACTION_AGGRESSIVE_BUY_{prediction_result['symbol']} (Confidence: {prediction_result['confidence']:.2f})"
        # Case C: 현재 강성주 기반 실행
        elif prediction_result['type'] == 'STRONG':
            action = f"ACTION_HOLD_LONG_{prediction_result['symbol']} (Trend: {prediction_result['trend']})"
        else:
            action = "ACTION_WAIT"

        return action

# --- 예시 사용 ---
if __name__ == "__main__":
    print("--- 리스크 헷지 모듈 테스트 시작 ---")
    # 시스템 안정성 지수(PTI)를 80으로 가정하고 초기화
    hedge = RiskHedgeModule(pti_score=80.0)

    # 시나리오 1: 안정적이지만 수익률 목표 미달 (경고 발생)
    result_low = {'type': 'RISE', 'symbol': '005930', 'confidence': 0.75, 'roi': 0.02, 'mdd': 0.01}
    print(f"\n[테스트 1: ROI 미달] 결과: {hedge.execute_hedge_logic(result_low)}")

    # 시나리오 2: 리스크 초과 (정지 발생)
    result_high = {'type': 'RISE', 'symbol': '005930', 'confidence': 0.85, 'roi': 0.06, 'mdd': 0.07}
    print(f"\n[테스트 2: MDD 초과] 결과: {hedge.execute_hedge_logic(result_high)}")

    # 시나리오 3: 시스템 불안정 (PTI 낮은 경우)
    hedge_unstable = RiskHedgeModule(pti_score=40.0)
    result_safe = {'type': 'RISE', 'symbol': '005930', 'confidence': 0.80, 'roi': 0.01, 'mdd': 0.00}
    print(f"\n[테스트 3: PTI 불안정] 결과: {hedge_unstable.execute_hedge_logic(result_safe)}")

print("--- 리스크 헷지 모듈 테스트 완료 ---")