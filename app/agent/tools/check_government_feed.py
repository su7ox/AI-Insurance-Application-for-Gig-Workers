import httpx
import logging
from app.config import settings
from app.agent.state import ClaimState

logger = logging.getLogger(__name__)

CURFEW_KEYWORDS = [
    "curfew", "section 144", "bandh", "shutdown",
    "police blockade", "prohibitory orders", "144 crpc"
]


async def check_government_feed(state: ClaimState, zone: str) -> ClaimState:
    try:
        city = zone.split(",")[0].strip() if "," in zone else zone.split()[0]
        query = f"curfew OR section 144 OR bandh {city} India"

        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{settings.GOV_FEED_API_BASE_URL}/everything",
                params={
                    "q": query,
                    "language": "en",
                    "sortBy": "publishedAt",
                    "pageSize": 5,
                    "apiKey": settings.GOV_FEED_API_KEY,
                },
                timeout=10,
            )
            resp.raise_for_status()
            data = resp.json()

        articles = data.get("articles", [])
        curfew_detected = False
        matched_headlines = []

        for article in articles:
            title = (article.get("title") or "").lower()
            description = (article.get("description") or "").lower()
            if any(kw in title or kw in description for kw in CURFEW_KEYWORDS):
                curfew_detected = True
                matched_headlines.append(article.get("title", ""))

        state["gov_feed_data"] = {
            "curfew_detected": curfew_detected,
            "matched_headlines": matched_headlines[:3],
            "articles_checked": len(articles),
            "zone": zone,
        }
        state["steps_completed"].append("check_gov_feed:fetched")
        logger.info(f"Gov feed for {zone}: curfew_detected={curfew_detected}")

    except Exception as e:
        logger.error(f"Gov feed error: {e}")
        state["gov_feed_data"] = {"curfew_detected": False, "matched_headlines": []}
        state["tool_errors"].append(f"check_gov_feed: {str(e)}")

    return state