from utils import make_embed

def setup_error_handler(tree):

    @tree.error
    async def on_app_command_error(interaction, error):
        await interaction.response.send_message(
            embed=make_embed("Error", [("Details", str(error)[:900])]),
            ephemeral=True
        )
