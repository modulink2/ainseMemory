# API 핸들러 모듈: KPI 데이터 제공을 위한 엔드포인트 정의 및 로직 통합
import json
from typing import Dict, Any
from datetime import datetime

# 이 파일은 백엔드에서 계산된 최종 KPI 데이터를 프론트엔드로 제공하는 역할을 담당합니다.

def calculate_kpi_data(prediction_result: Dict[str, Any], risk_status: str) -> Dict[str, Any]:
    """
    예측 결과와 리스크 상태를 기반으로 최종 PTI 및 ROI 데이터를 계산하고 구조화합니다.
    이 함수는 시스템 안정성 지수(PTI)와 수익화 지수(ROI)를 통합하여 제공합니다.
    """
    # 1. 예측 데이터에서 기본값 추출 (가정: prediction_result에 필요한 키가 존재한다고 가정)
    predicted_value = prediction_result.get("predicted_value", 0.0)
    confidence = prediction_result.get("confidence", 0.0)

    # 2. 리스크 상태 반영 (system_safe_mode의 영향을 최종 지표에 반영)
    if risk_status == "SAFE":
        safety_multiplier = 1.0
    elif risk_status == "WARNING":
        safety_multiplier = 0.95  # 경고 시 안전성 점수 약간 하향 조정
    else: # DANGER 또는 기타 실패 상태
        safety_multiplier = 0.5  # 위험 상태 시 안전성 지수 대폭 하향

    # 3. PTI 및 ROI 계산 로직 (기존 모듈의 결과를 통합한다고 가정)
    # 실제 구현에서는 sessions/2026-05-14T09-49/developer.md 등에서 정의된 수학적 모델을 여기에 적용해야 합니다.
    try:
        # 예시 계산 로직 (실제는 더 복잡한 공식 사용 필요)
        pti = (predicted_value * confidence) * safety_multiplier * 100  # 시스템 안정성 지수
        roi = (predicted_value - 100) / 100 if predicted_value > 100 else 0.0 # 헤징 ROI
    except Exception as e:
        # 계산 중 오류 발생 시 안전 모드 적용
        pti = 0.0
        roi = 0.0
        print(f"KPI 계산 중 예외 발생: {e}. system_safe_mode가 활성화되었습니다.")

    # 4. 최종 데이터 구조화 (Designer 요구사항 반영)
    final_data = {
        "timestamp": datetime.now().isoformat(),
        "prediction_source": "KiwoomRestApi",
        "asset_id": prediction_result.get("asset_id"),
        "predicted_price": round(predicted_value, 2),
        "confidence_score": round(confidence * 100, 2), # 백분율로 변환
        "system_safety_index_pti": round(pti, 2),  # 핵심 안전성 지수 (Deep Navy Blue 강조)
        "hedging_roi": round(roi, 4),              # 수익화 지수 (System Green 강조)
        "risk_status": risk_status,                 # 시스템 상태 (SAFE/WARNING/DANGER)
        "safety_level_visualization": "High" if pti > 80 else ("Medium" if pti > 50 else "Low") # 시각화 레벨
    }

    return final_data

def get_kpi_endpoint(asset_id: str, risk_status: str) -> Dict[str, Any]:
    """
    특정 자산 ID에 대한 최종 KPI를 조회하는 API 엔드포인트 함수.
    실제로는 DB/계산 모듈 호출을 포함해야 합니다.
    """
    # TODO: 실제 데이터베이스 또는 계산 엔진 호출 로직 삽입 필요 (현재는 Mock 데이터 반환)
    
    # Mock 데이터 시뮬레이션 (실제 구현 시 이 부분을 백엔드 계산 결과로 대체)
    mock_prediction = {
        "asset_id": asset_id,
        "predicted_value": 150.5,  # 예시 예측값
        "confidence": 0.85       # 예시 신뢰도
    }

    calculated_data = calculate_kpi_data(mock_prediction, risk_status)
    return calculated_data

if __name__ == '__main__':
    # 테스트 실행 예시
    test_asset = "005930"
    test_risk = "SAFE"
    result = get_kpi_endpoint(test_asset, test_risk)
    print(json.dumps(result, indent=4, ensure_ascii=False))