import sys
import time
from PyQt5.QtCore import QThread, pyqtSignal
import json

# --- 1. API 설정 및 인증 (Mocking for demonstration) ---
class KiwoomAPI:
    def __init__(self, api_key, secret):
        self.api_key = api_key
        self.secret = secret
        print("Kiwoom API 연결 초기화 완료.")

    def request_data(self, url):
        """실제 키움 API 호출을 모킹합니다."""
        # 실제 환경에서는 여기에 requests 라이브러리 등을 사용하여 API를 호출해야 합니다.
        if "error" in url:
            raise ConnectionError(f"API 요청 실패: {url} - 인증 오류 발생")
        
        # Mock 데이터 반환 (실제로는 서버 응답을 받아야 함)
        print(f"API 요청 성공: {url}")
        return {"status": "success", "data": [100, 200, 300]}

    def start_stream(self, symbol):
        """실시간 데이터 스트리밍을 시작하는 함수 (Mock)"""
        print(f"스트리밍 시작 요청: {symbol}")
        return True

# --- 2. 에러 핸들링 로직 구현 ---
class APIError(Exception):
    """API 연동 중 발생하는 모든 에러를 처리하기 위한 커스텀 예외."""
    def __init__(self, message, status_code=None):
        super().__init__(message)
        self.status_code = status_code

# --- 3. 실시간 스트리밍 및 데이터 흐름 구축 (Thread 기반) ---
class DataStreamer(QThread):
    """키움 API로부터 실시간 데이터를 받아오는 스레드."""
    data_received = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)

    def __init__(self, api: KiwoomAPI, symbol: str):
        super().__init__()
        self.api = api
        self.symbol = symbol
        self._running = True

    def run(self):
        print(f"[{self.symbol}] 데이터 스트리밍 스레드 시작.")
        try:
            while self._running:
                # 1초 간격으로 데이터 요청 시뮬레이션
                time.sleep(1)
                
                # API 호출 및 에러 핸들링 로직 적용
                try:
                    result = self.api.request_data(f"/stream/{self.symbol}")
                    if result and result.get("status") == "success":
                        # 데이터 수신 성공 시 시그널 발생
                        self.data_received.emit({"symbol": self.symbol, "timestamp": time.time(), "price_data": result.get("data")})
                    else:
                         raise APIError(f"API 응답 형식 오류: {result}")

                except ConnectionError as e:
                    # 네트워크 또는 연결 오류 처리
                    self.error_occurred.emit(f"연결 오류 발생 ({self.symbol}): {e}")
                    print(f"CRITICAL ERROR: {e}")
                    break # 치명적 오류 시 스트리밍 중단
                except APIError as e:
                    # API 자체에서 발생한 오류 처리 (인증, 데이터 형식 등)
                    self.error_occurred.emit(f"API 실행 오류 ({self.symbol}): {e}")
                    print(f"API ERROR: {e}")
                except Exception as e:
                    # 기타 예상치 못한 오류 처리
                    self.error_occurred.emit(f"알 수 없는 시스템 오류 ({self.symbol}): {e}")
                    print(f"UNEXPECTED ERROR: {e}")
                    break

        print(f"[{self.symbol}] 데이터 스트리밍 스레드 종료.")

    def stop(self):
        self._running = False
        self.wait()

# --- 4. 메인 실행 로직 ---
if __name__ == "__main__":
    # API 키는 보안상 실제 값이 아닌 Mock 값 사용
    API_KEY = "MOCK_KEY"
    SECRET = "MOCK_SECRET"
    TARGET_SYMBOL = "005930" # 삼성전자 예시

    print("="*50)
    print("🚀 갓더주식 API 스트리밍 시스템 시작")
    print("="*50)

    kiwoom = KiwoomAPI(API_KEY, SECRET)

    # 데이터 스트리머 스레드 생성 및 시작
    streamer = DataStreamer(kiwoom, TARGET_SYMBOL)
    streamer.data_received.connect(lambda data: print(f"\n[DATA RECEIVED] {json.dumps(data)}"))
    streamer.error_occurred.connect(lambda error: print(f"\n[ERROR ALERT] !!! {error} !!!"))
    
    streamer.start()

    # 10초 동안 스트리밍 데이터 수신 대기 (실제로는 무한 루프)
    try:
        time.sleep(10) 
    except KeyboardInterrupt:
        print("\n사용자 요청으로 스트리밍을 중단합니다.")
        streamer.stop()

    print("="*50)
    print("✅ 시스템 종료")
    print("="*50)