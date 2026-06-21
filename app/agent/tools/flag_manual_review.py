import logging
from app.agent.state import ClaimState

logger = logging.getLogger(__name__)

ANOMALY_THRESHOLD = 0.7


async def flag_for_manual_review(state: ClaimState) -> ClaimState:
    try:
        anomaly_score = state.get("anomaly_score", 0.0) or 0.0
        tool_errors = state.get("tool_errors", [])

        if anomaly_score >= ANOMALY_THRESHOLD:
            state["decision"] = "manual_review"
            state["decision_reason"] = f"High anomaly score: {anomaly_score}"
            logger.warning(f"Flagged for manual review: anomaly={anomaly_score}")
        elif len(tool_errors) >= 2:
            state["decision"] = "manual_review"
            state["decision_reason"] = f"Multiple tool failures: {tool_errors}"
            logger.warning(f"Flagged for manual review: tool errors={tool_errors}")

        state["steps_completed"].append("flag_manual_review:checked")

    except Exception as e:
        logger.error(f"Manual review flag error: {e}")
        state["tool_errors"].append(f"flag_manual_review: {str(e)}")

    return state