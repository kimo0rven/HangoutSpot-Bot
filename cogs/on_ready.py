import nextcord
import time
import datetime
import asyncio

from nextcord.ext import commands
from cogs.buttons.roleview import RoleView
from nextcord.ext import tasks


class ChangePresence(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(RoleView())
        print(f'\nLogged in as {self.bot.user.name} (ID:{str(self.bot.user.id)})'
            f'\nListening to {str(len(set(self.bot.get_all_members())))} users'
            f'\nConnected to {str(len(self.bot.guilds))} servers:')
        for guild in self.bot.guilds:
            print(f' •{guild.name}')
        await self.bot.change_presence(
            activity=nextcord.Activity(type=nextcord.ActivityType.listening, name=f"your demands!"))

    @commands.command(name="setstatus")
    @commands.has_role(764030966997712946)
    @commands.cooldown(1, 3600, commands.BucketType.member)
    async def setstatus(self, ctx: commands.Context, *, text: str):
        """Set the bot's status."""

        await self.bot.change_presence(activity=nextcord.Game(name=text))


def setup(bot: commands.Bot):
    bot.add_cog(ChangePresence(bot))
