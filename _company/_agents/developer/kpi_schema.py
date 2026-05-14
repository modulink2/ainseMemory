# KPI Schema Definition for Risk Management and Profitability
from typing import TypedDict, Literal
from datetime import datetime

class Tier(TypedDict):
    name: str  # e.g., "Basic Shield", "Pro Hedger"
    price_monthly: float  # Monthly subscription price
    system_safety_score: float  # System Safety KPI (0.0 to 1.0)
    hedging_roi: float  # Hedging ROI (Risk Management KPI)
    features: list[str] # Key features associated with the tier

class RiskMetric(TypedDict):
    timestamp: datetime
    tier_name: str
    system_safety_score: float
    hedging_roi: float
    status: Literal["Safe", "Warning", "Critical"] # System Status based on risk integration

# Example data structure for initial tracking
def get_initial_data() -> list[Tier]:
    return [
        {"name": "Basic Shield", "price_monthly": 19.0, "system_safety_score": 0.85, "hedging_roi": 0.2, "features": ["Basic Risk Limit"]},
        {"name": "Pro Hedger", "price_monthly": 49.0, "system_safety_score": 0.98, "hedging_roi": 0.5, "features": ["Advanced Hedge Logic", "Real-time Monitoring"]}
    ]

def get_initial_metrics() -> list[RiskMetric]:
    # Placeholder for dynamic metric collection
    now = datetime.now()
    return [
        {"timestamp": now, "tier_name": "Basic Shield", "system_safety_score": 0.85, "hedging_roi": 0.2, "status": "Safe"},
        {"timestamp": now, "tier_name": "Pro Hedger", "system_safety_score": 0.98, "hedging_roi": 0.5, "status": "Safe"}
    ]