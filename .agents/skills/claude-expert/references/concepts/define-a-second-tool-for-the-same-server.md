---
title: Define a second tool for the same server
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: sdk
---

# Define a second tool for the same server
@tool(
    "get_precipitation_chance",
    "Get the hourly precipitation probability for a location. "
    "Optionally pass 'hours' (1-24) to control how many hours to return.",
    {"latitude": float, "longitude": float},
)
async def get_precipitation_chance(args: dict[str, Any]) -> dict[str, Any]:
    # 'hours' isn't in the schema - read it with .get() to make it optional
    hours = args.get("hours", 12)
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": args["latitude"],
                "longitude": args["longitude"],
                "hourly": "precipitation_probability",
                "forecast_days": 1,
            },
        )
        data = response.json()
    chances = data["hourly"]["precipitation_probability"][:hours]

    return {
        "content": [
            {
                "type": "text",
                "text": f"Next {hours} hours: {'%, '.join(map(str, chances))}%",
            }
        ]
    }