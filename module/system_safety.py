# module/system_safety.py

import logging
from typing import Dict, Any

# 시스템 안정성 및 안전 모드 관련 설정 상수
SYSTEM_SAFE_MODE = "SYSTEM_SAFE_MODE_ACTIVE"
NORMAL_MODE = "NORMAL_TRADING_MODE"

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SystemSafetyManager:
    """
    시스템의 안정성 지수(PTI)와 데이터 무결성을 기반으로 자동매매 허용 여부를 제어하는 관리자 클래스.
    안정성이 수익률보다 우선한다는 원칙을 구현합니다.
    """
    def __init__(self, pti_threshold: float = 0.85):
        """
        초기화: PTI 임계값 설정 및 안전 모드 상태 초기화
        :param pti_threshold: 자동매매를 허용할 최소 시스템 안정성 지수 (예: 0.85)
        """
        self.pti_threshold = pti_threshold
        self._is_safe_mode_active = False
        logging.info(f"SystemSafetyManager 초기화 완료. PTI 임계값: {self.pti_threshold}")

    def check_stability(self, current_pti: float, data_integrity_ok: bool) -> str:
        """
        현재 시스템 안정성 지수와 데이터 무결성 상태를 기반으로 운영 모드를 결정합니다.
        :param current_pti: 현재 계산된 시스템 안정성 지수 (0.0 ~ 1.0)
        :param data_integrity_ok: 데이터 무결성 검증 성공 여부 (True/False)
        :return: 현재 운영 상태 ('NORMAL' 또는 'SAFE_MODE')
        """
        if not data_integrity_ok:
            # 데이터 무결성 실패 시 즉시 안전 모드 활성화 (최우선 안전장치)
            self.activate_safe_mode(f"데이터 무결성 실패 감지: {current_pti:.2f}PTI")
            return self._is_safe_mode_active

        if current_pti >= self.pti_threshold:
            # 안정성 기준 충족 시 정상 매매 허용
            self.deactivate_safe_mode()
            logging.info(f"시스템 안정성 확보. 현재 PTI: {current_pti:.2f}. 정상 매매 모드 활성화.")
            return NORMAL_MODE
        else:
            # 안정성 기준 미달 시 안전 모드 유지
            self._is_safe_mode_active = True
            logging.warning(f"시스템 안정성 임계값 미달. 현재 PTI: {current_pti:.2f}. 안전 모드 유지.")
            return SYSTEM_SAFE_MODE

    def activate_safe_mode(self, reason: str):
        """
        안전 모드를 활성화하고 모든 자동매매 및 리스크 계산을 정지시킵니다.
        :param reason: 안전 모드가 활성화된 구체적인 이유
        """
        if not self._is_safe_mode_active:
            self._is_safe_mode_active = True
            logging.error(f"!!! 시스템 안전 모드 활성화 !!! 원인: {reason}")
            # TODO: 여기에 실제 자동매매 실행 함수 정지 로직을 호출해야 합니다.

    def deactivate_safe_mode(self):
        """
        안전 모드를 해제하고 정상적인 운영 상태로 복귀시킵니다.
        """
        if self._is_safe_mode_active:
            self._is_safe_mode_active = False
            logging.info("시스템 안전 모드 해제. 시스템 정상 작동 모드로 복귀.")

    def get_status(self) -> str:
        """현재 안전 모드 상태 반환"""
        return self._is_safe_mode_active if self._is_safe_mode_active else "NORMAL"

# --- 통합 예시 함수 (실제 시스템에서는 데이터 연동 필요) ---

def integrate_safety_with_hedge(current_pti: float, integrity_status: bool):
    """
    PTI와 데이터 무결성 상태를 기반으로 리스크 헷지 모듈을 제어합니다.
    """
    manager = SystemSafetyManager(pti_threshold=0.85)
    status = manager.check_stability(current_pti, integrity_status)

    if status == SYSTEM_SAFE_MODE:
        logging.critical("!!! 리스크 헷지 모듈: 안전 모드에 진입하여 모든 거래를 중단합니다. !!!")
        # TODO: 실제 자동매매 실행 함수 호출을 여기서 정지시킵니다.
    else:
        logging.info(f"리스크 헷지 모듈: 안정 상태 확인. 현재 상태: {status}")
        # TODO: 정상적인 매매/계산 로직을 진행합니다.

# 테스트 예시 (실제 통합 시 이 부분을 실제 데이터 흐름에 연결해야 함)
if __name__ == '__main__':
    print("--- 시스템 안전 모드 프로토타입 실행 ---")
    
    # 케이스 1: 안정성 확보 (PTI > Threshold, Data OK)
    print("\n[테스트 Case 1: 정상 운영]")
    integrate_safety_with_hedge(current_pti=0.92, integrity_status=True)

    # 케이스 2: 안정성 미달 (PTI < Threshold, Data OK)
    print("\n[테스트 Case 2: 안정성 경고]")
    integrate_safety_with_hedge(current_pti=0.78, integrity_status=True)

    # 케이스 3: 데이터 무결성 실패 (시스템 안전장치 작동)
    print("\n[테스트 Case 3: 데이터 무결성 실패 -> 안전 모드]")
    integrate_safety_with_hedge(current_pti=0.95, integrity_status=False)

    print("\n--- 프로토타입 실행 완료 ---")