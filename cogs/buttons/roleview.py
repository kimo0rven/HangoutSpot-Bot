import nextcord


import bot_config.config

COET = bot_config.config.College_of_Engineering
CASS = bot_config.config.College_of_Arts_and_Social_Sciences
CCS = bot_config.config.College_of_Computer_Studies
CON = bot_config.config.College_of_Nursing
CSM = bot_config.config.College_of_Science_Mathematics
CED = bot_config.config.College_of_Education
CBAA = bot_config.config.College_of_Business_Administration_and_Accountancy
IDS = bot_config.config.Integrated_Developmental_School
NONIITIAN = bot_config.config.Non_IItian


async def handle_click(button: nextcord.ui.Button, interaction: nextcord.Interaction):
    role = interaction.guild.get_role(int(button.custom_id))
    gatekeep = interaction.guild.get_role(int(774133374990286872))
    assert isinstance(role, nextcord.Role)
    if gatekeep in interaction.user.roles:
        await interaction.user.add_roles(role)
        await interaction.user.remove_roles(gatekeep)
        # send confirmation message
        await interaction.response.send_message(
            f"You have been given the {button.label} role", ephemeral=True
        )
    else:
        await interaction.response.send_message(f"You already have a college role!", ephemeral=True)


class RoleView(nextcord.ui.View):
    """Creates buttons that assign roles"""

    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(label='COET',
                        emoji='😡',
                        style=nextcord.ButtonStyle.blurple,
                        custom_id=str(COET))
    async def COET_Button(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await handle_click(button, interaction)

    @nextcord.ui.button(label='CASS',
                        emoji='🍀',
                        style=nextcord.ButtonStyle.blurple,
                        custom_id=str(CASS))
    async def CASS_Button(self, button: nextcord.ui.Button, interaction):
        await handle_click(button, interaction)

    @nextcord.ui.button(label='CBAA',
                        emoji='🔔',
                        style=nextcord.ButtonStyle.blurple,
                        custom_id=str(CBAA))
    async def CBAA_Button(self, button: nextcord.ui.Button, interaction):
        await handle_click(button, interaction)

    @nextcord.ui.button(label='CCS',
                        emoji='🌀',
                        style=nextcord.ButtonStyle.blurple,
                        custom_id=str(CCS))
    async def CCS_Button(self, button: nextcord.ui.Button, interaction):
        await handle_click(button, interaction)

    @nextcord.ui.button(label='CON',
                        emoji='👻',
                        style=nextcord.ButtonStyle.blurple,
                        custom_id=str(CON))
    async def CON_Button(self, button: nextcord.ui.Button, interaction):
        await handle_click(button, interaction)

    @nextcord.ui.button(label='CSM',
                        emoji='🍊',
                        style=nextcord.ButtonStyle.blurple,
                        custom_id=str(CSM))
    async def CSM_Button(self, button: nextcord.ui.Button, interaction):
        await handle_click(button, interaction)

    @nextcord.ui.button(label='CED',
                        emoji='🕉️',
                        style=nextcord.ButtonStyle.blurple,
                        custom_id=str(CED))
    async def CED_Button(self, button: nextcord.ui.Button, interaction):
        await handle_click(button, interaction)

    @nextcord.ui.button(label='IDS',
                        emoji='🌸',
                        style=nextcord.ButtonStyle.blurple,
                        custom_id=str(IDS))
    async def IDS_Button(self, button: nextcord.ui.Button, interaction):
        await handle_click(button, interaction)

    @nextcord.ui.button(label='Non-IITian',
                        emoji='🍖',
                        style=nextcord.ButtonStyle.grey,
                        custom_id=str(NONIITIAN))
    async def NonIITian_Button(self, button: nextcord.ui.Button, interaction):
        await handle_click(button, interaction)


