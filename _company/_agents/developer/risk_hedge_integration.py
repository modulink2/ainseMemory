import sys
import json
from typing import Dict, Any

# --- 설정 및 상수 (가정된 값) ---
SYSTEM_SAFE_MODE = "system_safe_mode"
LOSS_LIMIT = 0.1  # 예시: 최대 허용 손실 제한 (MDD 기반)
TARGET_SR = 1.5   # 예시: 목표 샤프 비율 (SR 기반)

class RiskHedgeModule:
    """리스크 헷지 모듈의 핵심 로직을 담당합니다."""
    def __init__(self, prediction_results: Dict[str, Any]):
        self.results = prediction_results
        self.is_safe = True

    def calculate_risk(self) -> Dict[str, float]:
        """예측 결과에 따른 실시간 위험도를 계산합니다."""
        # 실제 구현에서는 TS, VSI, MSI 등을 기반으로 복잡한 수학적 모델을 적용해야 합니다.
        predicted_loss = self.results.get('predicted_loss', 0.0)
        current_mdd = self.results.get('current_mdd', float('inf'))

        # 예시: MDD 및 SR 기반 위험도 계산 (수학적 일관성 반영)
        risk_score = predicted_loss * 1.5  # 단순 예시 공식
        if current_mdd > TARGET_SR * 2:
            risk_score += 0.5 # 목표 대비 과도한 변동성 페널티

        return {
            "risk_score": risk_score,
            "is_critical": risk_score > 1.0  # 임계값 설정
        }

    def execute_hedge(self) -> str:
        """Case A, B, C 기반의 리스크 헷지 자동 실행 로직을 시뮬레이션합니다."""
        print("--- Risk Hedge Execution Simulation ---")
        
        if not self.is_safe:
            return f"SYSTEM HALTED: {SYSTEM_SAFE_MODE} is ACTIVE. Loss limit enforced."

        # Case A: 예측된 손실이 임계값을 초과할 경우 (자동 정지/경고)
        if self.results.get('predicted_loss', 0.0) > LOSS_LIMIT * 1.2:
            self.is_safe = False
            return f"RISK ALERT (Case A): Predicted loss ({self.results.get('predicted_loss')}) exceeds threshold. System safe mode activated."

        # Case B: 데이터 무결성 실패 시 (가정)
        if self.results.get('data_integrity_fail', False):
            self.is_safe = False
            return f"DATA INTEGRITY FAILURE (Case B): Data integrity check failed. System safe mode activated and loss limit enforced."

        # Case C: 정상 실행
        if self.results.get('predicted_loss', 0.0) > LOSS_LIMIT:
            print("Hedge executed: Loss limit triggered.")
            return "Hedge Action Taken: Loss limit enforced based on risk calculation."
        else:
            print("Hedge successful: No immediate hedge required.")
            return "Hedge Successful: Market conditions stable. No action taken."

class CentralController:
    """시스템의 중앙 제어 및 안전장치 관리 모듈입니다."""
    def __init__(self, risk_module: RiskHedgeModule):
        self.risk_module = risk_module
        self.safe_mode_active = False
        self.final_decision = ""

    def run_prediction_and_hedge(self, prediction_data: Dict[str, Any]):
        """예측을 실행하고 리스크 헷지 모듈을 통합하여 최종 결정을 내립니다."""
        print("\n[Central Controller]: Starting prediction and risk assessment...")
        
        # 1. 예측 결과에 기반한 위험도 계산
        risk_metrics = self.risk_module.calculate_risk()
        
        # 2. 데이터 무결성 검증 통합 (가장 중요한 안전장치)
        data_integrity_fail = prediction_data.get('data_integrity_fail', False)
        
        if data_integrity_fail:
            print("[Controller]: CRITICAL ERROR - Data Integrity Failure detected.")
            self.safe_mode_active = True
            final_message = self.risk_module.execute_hedge()
        else:
            # 3. 정상적인 리스크 헷지 실행
            final_message = self.risk_module.execute_hedge()

        # 4. 최종 결정 및 상태 기록
        self.final_decision = final_message
        print(f"[Controller]: Final Decision: {self.final_decision}")
        
        if self.safe_mode_active:
            print("SYSTEM STATUS: SAFE MODE ON.")
        else:
            print("SYSTEM STATUS: NORMAL OPERATION.")

# --- 메인 실행 로직 (테스트 환경) ---
if __name__ == "__main__":
    # 테스트 데이터 1: 정상적인 예측 시나리오
    test_data_normal = {
        "predicted_loss": 0.05,  # 예상 손실 5%
        "current_mdd": 1.2,      # 현재 MDD 1.2 (SR 대비 안전)
        "data_integrity_fail": False
    }
    print("==============================================")
    print("TEST 1: Normal Scenario Execution")
    print("==============================================")

    risk_mod_normal = RiskHedgeModule(test_data_normal)
    controller_normal = CentralController(risk_mod_normal)
    controller_normal.run_prediction_and_hedge(test_data_normal)


    print("\n\n==============================================")
    print("TEST 2: Data Integrity Failure Scenario (Safety Check)")
    print("==============================================")

    # 테스트 데이터 2: 데이터 무결성 실패 시나리오 (시스템 안전장치 작동 확인)
    test_data_fail = {
        "predicted_loss": 0.15,  # 예상 손실 15%
        "current_mdd": 3.5,      # MDD가 높음
        "data_integrity_fail": True # 데이터 무결성 실패 플래그 설정
    }

    risk_mod_fail = RiskHedgeModule(test_data_fail)
    controller_fail = CentralController(risk_mod_fail)
    controller_fail.run_prediction_and_hedge(test_data_fail)
    
    print("\n==============================================")
    print("✅ 최종 검증 완료.")
    print("==============================================")