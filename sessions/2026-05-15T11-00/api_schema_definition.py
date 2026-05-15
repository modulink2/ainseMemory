# API 응답 스키마 및 데이터 구조 정의 파일

def define_prediction_response(prediction_data: dict, pti_score: float, roi_value: float) -> dict:
    """
    알고리즘 예측 결과와 시스템 안정성 지표(PTI), 수익률(ROI)을 결합하여 최종 API 응답을 생성합니다.

    Args:
        prediction_data (dict): 알고리즘이 산출한 기본 예측 데이터 (예: 주식 코드, 예측 종류 등).
        pti_score (float): 계산된 시스템 안정성 지수 (0~100).
        roi_value (float): 계산된 투자 수익률 (%).

    Returns:
        dict: 최종 사용자에게 제공될 API 응답 JSON 구조.
    """
    # PTI와 ROI를 기반으로 신뢰 점수를 계산하여 최종 메시지를 구성합니다.
    trust_score = 100 - (100 - pti_score) * 0.5  # 안정성 지수가 높을수록 신뢰도 증가
    risk_reward_factor = roi_value / (pti_score + 1e-6) # 리스크 대비 보상 비율

    response = {
        "status": "success",
        "data": {
            "prediction_result": prediction_data.get("result", "N/A"),
            "base_stability_index_pti": round(pti_score, 2),  # 시스템 안정성 지수 (PTI)
            "risk_reward_metric_roi": round(roi_value, 2),     # 수익률 (ROI)
            "system_trust_score": round(trust_score, 2),       # 시스템 신뢰 점수 (PTI 기반)
            "risk_reward_factor": round(risk_reward_factor, 4), # 리스크/보상 비율
            "status_message": f"예측 결과: {prediction_data.get('result')}. 안정성 지수({pti_score:.2f})를 기반으로 판단합니다."
        },
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "version": "1.0",
            "source": "Kiwoom_RestApi_Engine"
        }
    }
    return response

# 참고: 이 함수는 실제 백엔드 API 엔드포인트에서 호출될 최종 형태입니다.