from typing import TypedDict
from datetime import datetime


class ClaimState(TypedDict):
    # --- Worker & message ---
    whatsapp_id: str
    worker_id: int
    policy_id: int | None
    raw_message: str
    platform: str
    partner_id: str

    # --- Classification ---
    disruption_type: str

    # --- Time window ---
    claimed_window_start: datetime | None
    claimed_window_end: datetime | None

    # --- Tool results ---
    shift_verified: bool | None
    weather_data: dict | None
    gov_feed_data: dict | None
    policy_rule: dict | None
    fraud_history: dict | None

    # --- ML outputs ---
    anomaly_score: float | None
    effective_hours: float | None
    phr: float | None
    slf: float | None
    final_payout: float | None

    # --- Decision ---
    decision: str | None
    decision_reason: str | None
    smart_receipt: str | None

    # --- Agent control ---
    tool_errors: list[str]
    steps_completed: list[str]