import nextcord

VIEW_NAME = "RoleView"


async def handle_click(
        button: nextcord.ui.Button, interaction: nextcord.Interaction
):
    # get role from the role id
    role = interaction.guild.get_role(int(button.custom_id.split(":")[-1]))
    assert isinstance(role, nextcord.Role)
    # if member has the role, remove it
    if role in interaction.user.roles:
        await interaction.user.remove_roles(role)
        # send confirmation message
        await interaction.response.send_message(
            f"Your {button.label} role has been removed", ephemeral=True
        )
    # if the member does not have the role, add it
    else:
        await interaction.user.add_roles(role)
        # send confirmation message
        await interaction.response.send_message(
            f"You have been given the {button.label} role", ephemeral=True
        )


class Study(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(
        label="Subscriber",
        emoji="💖",
        style=nextcord.ButtonStyle.primary,
        # set custom id to be the bot name : the class name : the role id
        custom_id="dasdasd",
    )
    async def subscriber_button(self, button, interaction):
        await handle_click(button, interaction)

    @nextcord.ui.button(
        label="Developer",
        emoji="💻",
        style=nextcord.ButtonStyle.primary,
        custom_id="sadas",
    )
    async def developer_button(self, button, interaction):
        await handle_click(button, interaction)

    @nextcord.ui.button(
        label="Content Creator",
        emoji="✍",
        style=nextcord.ButtonStyle.primary,
        custom_id="sadasd",
    )
    async def content_creator_button(self, button, interaction):
        await handle_click(button, interaction)

    @nextcord.ui.button(
        label="YouTube Ping",
        emoji="🔔",
        style=nextcord.ButtonStyle.primary,
        custom_id="dsadas",
    )
    async def youtube_ping_button(self, button, interaction):
        await handle_click(button, interaction)