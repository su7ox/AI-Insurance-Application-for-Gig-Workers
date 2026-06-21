import logging
from app.agent.state import ClaimState
from app.config import settings

logger = logging.getLogger(__name__)


async def calculate_payout(state: ClaimState, risk_score: float, weekly_premium: float) -> ClaimState:
    try:
        if risk_score <= 0:
            risk_score = 0.1
        phr = (weekly_premium / risk_score) * settings.PHR_K
        state["phr"] = round(phr, 2)

        effective_hours = state.get("effective_hours") or 2.0
        state["effective_hours"] = effective_hours

        claim_density = 0.1
        slf = 1 / (1 + settings.SLF_ALPHA * claim_density)
        state["slf"] = round(slf, 4)

        adjusted_rate = phr * slf
        final_payout = min(adjusted_rate * effective_hours, settings.MAX_DAILY_PAYOUT)
        state["final_payout"] = round(final_payout, 2)

        state["steps_completed"].append("calculate_payout:done")
        logger.info(f"Payout: PHR={phr} SLF={slf} hours={effective_hours} → ₹{final_payout}")

    except Exception as e:
        logger.error(f"Payout calculation error: {e}")
        state["final_payout"] = 0.0
        state["tool_errors"].append(f"calculate_payout: {str(e)}")

    return state