from langchain_groq import ChatGroq
from app.config import settings
import logging

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are a disruption classifier for an income insurance system for gig delivery workers in India.

Your job is to classify the worker's message into exactly one disruption type.

Disruption types:
- heavy_rain: Heavy rainfall, flooding, waterlogging preventing delivery
- flood: Flooding, waterlogging, roads submerged
- extreme_heat: Extreme heat above 45°C preventing safe delivery
- severe_aqi: Severe air quality / smog / pollution above AQI 300
- cyclone: Cyclone, storm, strong winds warning
- curfew_section_144: Curfew, Section 144, police blockade, shutdown, bandh
- unknown: Cannot classify into any of the above

Reply with ONLY the disruption type string, nothing else.
Examples:
- "it was raining heavily, couldn't deliver" → heavy_rain
- "police stopped movement near my area" → curfew_section_144
- "roads were flooded" → flood
- "too hot to ride today" → extreme_heat
- "very bad smog today, AQI was terrible" → severe_aqi
- "cyclone warning in my area" → cyclone
"""

VALID_TYPES = {
    "heavy_rain", "flood", "extreme_heat",
    "severe_aqi", "cyclone", "curfew_section_144", "unknown"
}


async def classify_disruption(message: str) -> str:
    """
    Classify worker's raw message into a disruption type.
    Returns one of the valid disruption type strings.
    """
    try:
        llm = ChatGroq(
            model=settings.LLM_MODEL,
            api_key=settings.GROQ_API_KEY,
            temperature=0,
        )
        response = await llm.ainvoke([
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": message},
        ])
        result = response.content.strip().lower()
        if result not in VALID_TYPES:
            logger.warning(f"Unexpected classification: {result} — defaulting to unknown")
            return "unknown"
        logger.info(f"Classified '{message}' → {result}")
        return result
    except Exception as e:
        logger.error(f"Classification error: {e}")
        return "unknown"