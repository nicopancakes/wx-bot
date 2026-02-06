import discord
from discord import app_commands
from utils import get_json, make_embed


async def setup(tree):

    @tree.command(name="alerts", description="Weather Alerts for US Territory")
    async def alerts(interaction: discord.Interaction, state: str):

        data = await get_json(
            f"https://api.weather.gov/alerts/active?area={state.upper()}"
        )

        if not data or not data["features"]:
            await interaction.response.send_message(
                embed=make_embed("Alerts",[("Status","None")])
            )
            return

        a = data["features"][0]["properties"]

        await interaction.response.send_message(embed=make_embed(
            "Weather Alert",
            [
                ("Event", a["event"]),
                ("Severity", a["severity"]),
                ("Area", a["areaDesc"])
            ],
            discord.Color.red()
        ))
