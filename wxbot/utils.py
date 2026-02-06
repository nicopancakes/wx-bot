import discord
import aiohttp
from datetime import datetime

timeout = aiohttp.ClientTimeout(total=10)

async def get_json(url):
    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url, headers={"User-Agent": "WeatherBot"}) as r:
                if r.status != 200:
                    return None
                return await r.json()
    except:
        return None


async def geocode(city):
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    data = await get_json(url)
    if not data or "results" not in data:
        return None
    r = data["results"][0]
    return r["latitude"], r["longitude"], r["name"]


def make_embed(title, fields, color=discord.Color.blue()):
    e = discord.Embed(title=title, color=color)
    for name, value in fields:
        e.add_field(name=name, value=value, inline=False)
    e.timestamp = datetime.utcnow()
    return e


def deg_to_dir(deg):
    dirs = ['N','NNE','NE','ENE','E','ESE','SE','SSE',
            'S','SSW','SW','WSW','W','WNW','NW','NNW']
    ix = int((deg + 11.25)/22.5)
    return dirs[ix % 16]
