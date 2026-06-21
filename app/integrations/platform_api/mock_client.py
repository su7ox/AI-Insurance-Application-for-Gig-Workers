import json
import os
import logging

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
PLATFORM_DATA_FILE = os.path.join(BASE_DIR, "data", "mock", "platform_data.json")


def _load_json() -> dict:
    with open(PLATFORM_DATA_FILE, "r") as f:
        return json.load(f)


def get_worker_profile(platform: str, partner_id: str) -> dict | None:
    """Simulate fetching full worker profile from platform API."""
    try:
        data = _load_json()
        return data.get(platform.lower(), {}).get(partner_id.upper())
    except Exception as e:
        logger.error(f"Mock platform API error: {e}")
        return None


def get_shift_data(platform: str, partner_id: str) -> dict | None:
    """Simulate fetching active shift from platform telemetry API."""
    try:
        worker = get_worker_profile(platform, partner_id)
        if not worker:
            return None
        return worker.get("active_shift")
    except Exception as e:
        logger.error(f"Mock shift API error: {e}")
        return None