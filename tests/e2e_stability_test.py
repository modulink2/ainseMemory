import time
import random
from typing import List, Dict, Any

# --- Mocking Data Source (실제 API 호출 대신 시뮬레이션) ---
class MockAPIClient:
    """API 통신을 모킹하여 테스트 환경을 구축합니다."""
    def get_data(self, endpoint: str) -> Dict[str, Any]:
        # 10%의 오류율과 임의의 지연 시간을 시뮬레이션
        if random.random() < 0.1:
            raise ConnectionError("Simulated API Failure")
        time.sleep(random.uniform(0.05, 0.3))  # 50ms ~ 300ms 지연
        return {"status": "success", "data": f"mock_result_from_{endpoint}"}

# --- KPI 측정 및 로깅 모듈 ---
class StabilityMonitor:
    """시스템 안정성 KPI를 측정하고 로그를 기록하는 클래스입니다."""
    def __init__(self, error_threshold: float = 0.005, latency_threshold: float = 0.05):
        self.error_count = 0
        self.latency_sum = 0.0
        self.total_calls = 0
        self.start_time = time.time()
        self.end_time = None
        self.error_threshold = error_threshold  # 오류율 목표 (0.5% -> 0.005)
        self.latency_threshold = latency_threshold # 지연 시간 목표 (±5% -> 0.05)

    def record_call(self, call_duration: float, success: bool):
        self.total_calls += 1
        if not success:
            self.error_count += 1
        self.latency_sum += call_duration

    def finalize(self):
        self.end_time = time.time()
        total_duration = self.end_time - self.start_time
        
        # 오류율 계산 (Error Rate)
        error_rate = self.error_count / self.total_calls if self.total_calls > 0 else 0.0
        
        # 평균 지연 시간 계산 (Average Latency)
        avg_latency = self.latency_sum / self.total_calls if self.total_calls > 0 else 0.0

        self.error_rate = error_rate
        self.avg_latency = avg_latency
        self.total_duration = total_duration
        
        print("\n--- 📊 시스템 안정성 최종 보고서 ---")
        print(f"총 호출 횟수: {self.total_calls}")
        print(f"오류 발생 횟수: {self.error_count} (오류율: {error_rate:.4f})")
        print(f"평균 지연 시간: {avg_latency:.4f}초")
        print(f"총 소요 시간: {total_duration:.2f}초")

        # KPI 검증 로직 (CEO 목표 기준)
        is_stable = (error_rate <= self.error_threshold) and (avg_latency <= self.latency_threshold)
        print(f"\n✅ 시스템 안정성 검증 결과: {'통과' if is_stable else '실패'} (목표: 오류율 <= {self.error_threshold*100}%, 지연 시간 <= {self.latency_threshold*100}%)")

        if not is_stable:
            print("🚨 경고: 시스템 안정성 KPI 미달. 즉각적인 로직 검토가 필요합니다.")


def run_e2e_test(monitor: StabilityMonitor, client: MockAPIClient, test_scenarios: List[str]):
    """설정된 시나리오에 따라 E2E 테스트를 실행하고 모니터링합니다."""
    print("\n\n--- 🚀 E2E 통합 테스트 시작 ---")
    for i, scenario in enumerate(test_scenarios):
        print(f"\n[Scenario {i+1}/{len(test_scenarios)}]: {scenario}")
        try:
            # 실제 API 호출 시뮬레이션
            start = time.time()
            response = client.get_data(scenario)
            duration = time.time() - start
            
            monitor.record_call(duration, True)
            print(f"  -> 성공. 응답: {response.get('data')}, 소요 시간: {duration:.4f}초")

        except ConnectionError as e:
            # API 호출 실패 시 기록
            duration = time.time() - start
            monitor.record_call(duration, False)
            print(f"  -> ❌ 실패 (ConnectionError). 소요 시간: {duration:.4f}초")
        except Exception as e:
            # 기타 예외 처리
            print(f"  -> 💥 치명적 오류 발생: {e}")
            monitor.record_call(time.time() - start, False)

    # 테스트 종료 후 최종 보고서 생성
    monitor.finalize()


if __name__ == "__main__":
    # 1. 환경 초기화 및 설정
    print("⚙️ E2E 테스트 환경을 위한 모니터와 클라이언트 초기화 중...")
    monitor = StabilityMonitor(error_threshold=0.005, latency_threshold=0.05) # KPI 설정 적용
    client = MockAPIClient()

    # 2. E2E 시나리오 정의 (핵심 기능 흐름)
    test_scenarios = [
        "endpoint_a",  # 정상 경로 테스트
        "endpoint_b",  # 또 다른 정상 경로 테스트
        "endpoint_c",  # 오류 발생 확률을 높여 시스템 스트레스 테스트
        "endpoint_d"   # 마지막 데이터 무결성 검증
    ]

    # 3. 테스트 실행
    run_e2e_test(monitor, client, test_scenarios)