import discord
from discord import app_commands
from datetime import datetime, timedelta
from utils import geocode, get_json, make_embed


async def setup(tree):

    @tree.command(name="forecast", description="3 day forecast")
    async def forecast(interaction: discord.Interaction, city: str):

        geo = await geocode(city)
        if not geo:
            await interaction.response.send_message(embed=make_embed("Error",[("City","Not found")]))
            return

        lat, lon, name = geo

        data = await get_json(
            f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,temperature_2m_min"
        )

        d = data["daily"]
        fields = []

        for i in range(3):
            date = (datetime.utcnow()+timedelta(days=i)).strftime("%Y-%m-%d")
            fields.append((date,
                f"Max {d['temperature_2m_max'][i]}C / Min {d['temperature_2m_min'][i]}C"))

        await interaction.response.send_message(
            embed=make_embed(f"Forecast — {name}", fields)
        )
