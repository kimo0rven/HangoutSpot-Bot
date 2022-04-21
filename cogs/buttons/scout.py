import nextcord
import random

from words.scout import scout_locations
from util import unbAPI
from json import load
from pathlib import Path

import bot_config.config

with Path("bot_config/unb_token.json").open() as f:
    config = load(f)

token = config["token"]
init_link = config["init_link"]
currency = bot_config.config.currency


class RandomButton(nextcord.ui.Button['RandomButton']):
    def __init__(self, value: bool):
        super().__init__(label=random.choice(scout_locations), style=nextcord.ButtonStyle.blurple)
        self.value = value


    async def callback(self, interaction: nextcord.Interaction):
        assert self.view is not None
        view: Scout = self.view

        money = random.randint(2000, 5000)
        if self.label == "OC":
            money = random.randint(5000, 10000)
        reason = 'Scouting'
        unbAPI(money, reason, interaction.user.id)
        embed = nextcord.Embed(description=f"You went to the {self.label} and found {currency}{'{:,}'.format(money)}",
                               color=15799643
                               )
        await interaction.response.edit_message(embed=embed)
        view.value = self.value
        view.stop()


class Scout(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(RandomButton(True))
        self.add_item(RandomButton(True))
        self.add_item(RandomButton(True))



