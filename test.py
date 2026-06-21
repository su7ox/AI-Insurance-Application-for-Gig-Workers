import asyncio
import httpx
from app.config import settings
from app.agent.tools.check_weather import resolve_zone_coords

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"
AQI_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"


async def test_weather(zone: str):
    print(f"\n--- Weather: {zone} ---")
    lat, lon = await resolve_zone_coords(zone)
    print(f"Resolved coords: ({lat}, {lon})")

    async with httpx.AsyncClient() as client:
        r = await client.get(
            OPEN_METEO_URL,
            params={
                "latitude": lat,
                "longitude": lon,
                "current": [
                    "temperature_2m",
                    "precipitation",
                    "rain",
                    "weathercode",
                    "windspeed_10m",
                ],
                "timezone": "Asia/Kolkata",
            },
        )
        current = r.json()["current"]
        print(f"Temp: {current['temperature_2m']}°C")
        print(f"Rainfall: {current.get('rain', 0.0)} mm")
        print(f"Wind: {current.get('windspeed_10m')} km/h")

        r2 = await client.get(
            AQI_URL,
            params={
                "latitude": lat,
                "longitude": lon,
                "current": ["european_aqi", "pm2_5"],
                "timezone": "Asia/Kolkata",
            },
        )
        aqi = r2.json()["current"]
        print(f"AQI: {aqi.get('european_aqi')} | PM2.5: {aqi.get('pm2_5')} μg/m³")


async def test_news(city: str):
    print(f"\n--- News: {city} ---")
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"{settings.GOV_FEED_API_BASE_URL}/everything",
            params={
                "q": f"curfew OR section 144 OR bandh {city} India",
                "language": "en",
                "sortBy": "publishedAt",
                "pageSize": 5,
                "apiKey": settings.GOV_FEED_API_KEY,
            },
        )
        articles = r.json().get("articles", [])
        print(f"Articles found: {len(articles)}")
        for a in articles:
            print(f"  → {a['title']}")


async def main():
    # Test varied Indian zones
    await test_weather("Koramangala, Bengaluru")
    await test_weather("Andheri, Mumbai")
    await test_weather("Salt Lake, Kolkata")
    await test_weather("T Nagar, Chennai")
    await test_weather("Banjara Hills, Hyderabad")

    await test_news("Mumbai")
    await test_news("Bengaluru")


asyncio.run(main())
