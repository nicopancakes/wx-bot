import discord
from discord import app_commands
from utils import geocode, get_json, make_embed, deg_to_dir


async def setup(tree):

    @tree.command(name="weather", description="Current weather for an Area")
    async def weather(interaction: discord.Interaction, city: str):
        await interaction.response.defer()

        geo = await geocode(city)
        if not geo:
            await interaction.followup.send(embed=make_embed("Error",[("City","Not found")]))
            return

        lat, lon, name = geo

        data = await get_json(
            f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        )

        if not data:
            await interaction.followup.send(embed=make_embed("Error",[("Weather","Unavailable")]))
            return

        c = data["current_weather"]

        temp_c = round(c["temperature"])
        temp_f = round(temp_c * 9/5 + 32)

        await interaction.followup.send(embed=make_embed(
            "Current Weather",
            [
                ("Location", name),
                ("Temp Celsius", str(temp_c)),
                ("Temp Fahrenheit", str(temp_f)),
                ("Wind Speed", str(c["windspeed"])),
                ("Wind Dir", deg_to_dir(c["winddirection"]))
            ]
        ))
