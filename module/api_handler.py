# API 응답 및 데이터 구조 구현 파일
import json
from typing import Dict, Any

# PTI 기반 시스템 안정성 지수 계산 로직 (가정치 - 실제 로직은 다른 모듈에서 가져온다고 가정)
def calculate_pti(risk_score: float, safety_mode: bool) -> float:
    """시스템 안정성 지수(PTI)를 계산합니다. 안전모드가 활성화되면 점수가 급격히 하락합니다."""
    if safety_mode:
        # 안전 모드 활성화 시 시스템 안정성 지수를 극단적으로 낮춤
        return risk_score * 0.1 
    # 일반 모드에서는 리스크 점수에 기반하여 계산 (예시 로직)
    return risk_score * 1.0

def generate_final_response(algorithm_result: Dict[str, Any], pti: float, roi: float) -> str:
    """알고리즘 결과와 시스템 안정성 지수를 통합하여 최종 JSON 응답을 생성합니다."""
    
    # 알고리즘 결과 매핑 (가정)
    prediction = algorithm_result.get("prediction", "N/A")
    risk_level = algorithm_result.get("risk_level", "Medium")

    # PTI 중심의 데이터 구조 정의
    response_data = {
        "status": "Success",
        "timestamp": "2026-05-15T10:00:00Z", # 실제 시간으로 대체 필요
        "prediction": prediction,
        "risk_level": risk_level,
        "system_stability_pti": round(pti, 4), # PTI 최우선 강조
        "profitability_roi": round(roi, 2),
        "safety_status": "Normal" if pti > 0.5 else "Warning",
        "risk_assessment": {
            "base_risk_score": algorithm_result.get("base_risk_score"),
            "pti_score": round(pti, 4), # PTI 점수를 명확히 제시
            "safety_mode_active": "True" if pti < 0.5 else "False",
            "action_recommendation": "Proceed with caution based on PTI."
        }
    }
    
    return json.dumps(response_data, indent=4, ensure_ascii=False)

# --- 테스트 시나리오 ---
def run_e2e_test():
    print("--- E2E 시스템 안정성 및 데이터 반영 테스트 시작 ---")
    
    # 1. 성공적인 예측 시나리오 (안정 상태)
    print("\n[테스트 1: 일반 모드 성공]")
    mock_algo_success = {
        "prediction": "Strong Buy",
        "base_risk_score": 0.75,
        "market_data": {"volume": 100000, "change": 2.5}
    }
    pti_success = calculate_pti(mock_algo_success["base_risk_score"], False) # 안전 모드 False
    roi_success = 1.5 # 수익률 가정

    final_json_success = generate_final_response(mock_algo_success, pti_success, roi_success)
    print("Generated JSON (Success):")
    print(final_json_success)
    # 데이터 무결성 검증: PTI가 높고 안정 상태인지 확인
    if float(final_json_success.split('"system_stability_pti":')[1].split(',')[0]) > 0.5:
        print("✅ 데이터 무결성 검증 통과: 일반 모드에서 높은 PTI가 성공적으로 반영됨.")
    else:
        print("❌ 데이터 무결성 실패: 예상치 못한 낮은 PTI 값이 발생함.")


    # 2. 위험 상황 시나리오 (안전 모드 활성화)
    print("\n[테스트 2: 안전 모드 발동 시나리오]")
    mock_algo_risk = {
        "prediction": "Hold",
        "base_risk_score": 0.9,
        "market_data": {"volume": 50000, "change": -1.0}
    }
    pti_risk = calculate_pti(mock_algo_risk["base_risk_score"], True) # 안전 모드 True
    roi_risk = -0.2 # 손실 가정

    final_json_risk = generate_final_response(mock_algo_risk, pti_risk, roi_risk)
    print("Generated JSON (Risk):")
    print(final_json_risk)
    # 데이터 무결성 검증: 안전 모드 활성화 시 PTI가 급락하고 시스템 상태가 반영되었는지 확인
    if float(final_json_risk.split('"system_stability_pti":')[1].split(',')[0]) < 0.5:
        print("✅ 데이터 무결성 검증 통과: 안전 모드 활성화 시 PTI가 급락하고 시스템 상태가 정확히 반영됨.")
    else:
        print("❌ 데이터 무결성 실패: 안전 모드에서의 안정성 지수 변화가 충분히 강조되지 않음.")

if __name__ == "__main__":
    run_e2e_test()