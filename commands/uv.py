import discord
from discord import app_commands
from utils import geocode, make_embed


async def setup(tree):

    @tree.command(name="uv", description="UV index")
    async def uv(interaction: discord.Interaction, city: str):

        geo = await geocode(city)
        if not geo:
            await interaction.response.send_message(embed=make_embed("Error",[("City","Not found")]))
            return

        await interaction.response.send_message(
            embed=make_embed("UV Index",[("Location",geo[2]),("Value","Unavailable")])
        )
