import discord
from discord import app_commands
import os
import importlib

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


async def load_commands():
    for file in os.listdir("commands"):
        if file.endswith(".py"):
            mod = importlib.import_module(f"commands.{file[:-3]}")
            await mod.setup(tree)


@client.event
async def on_ready():
    await load_commands()
    from error_handler import setup_error_handler
    setup_error_handler(tree)

    await tree.sync()
    print(f"WX-BOT Is Online!: {client.user}")


if __name__ == "__main__":
    token = input("Enter the Token: ").strip()
    client.run(token)
