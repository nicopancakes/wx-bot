import discord
from discord import app_commands
from utils import geocode, get_json, make_embed, deg_to_dir


async def setup(tree):

    @tree.command(name="wind", description="Wind info")
    async def wind(interaction: discord.Interaction, city: str):
        await interaction.response.defer()

        geo = await geocode(city)
        if not geo:
            await interaction.followup.send(embed=make_embed("Error",[("City","Not found")]))
            return

        lat, lon, name = geo

        data = await get_json(
            f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        )

        c = data["current_weather"]

        await interaction.followup.send(embed=make_embed(
            "Wind",
            [
                ("Location", name),
                ("Speed", str(c["windspeed"])),
                ("Direction", deg_to_dir(c["winddirection"]))
            ]
        ))
