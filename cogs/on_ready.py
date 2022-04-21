import nextcord
import json
import time
import datetime
import asyncio

from nextcord.ext import commands
from cogs.buttons.roleview import RoleView
from nextcord.ext import tasks

secret_file = json.load(open('./bot_config/secrets.json'))


class ChangePresence(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.scheduled_task.start()

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

    @tasks.loop()
    async def scheduled_task(self, ctx):
        await self.bot.wait_until_ready()
        weekday = datetime.datetime.weekday(datetime.datetime.now())
        users = []
        member_nick_role = ctx.guild.get_role(845790842521780265)
        member_nick = member_nick_role.members

        if weekday == 6:
            for person in member_nick:
                users.append(person.mention)
                await asyncio.sleep(3)
            channel = self.bot.get_channel(748708955500445737)
            message = 'test'
            await ctx.bot.remove_roles(ctx.person.id, member_nick_role)
            await channel.send(message)


def setup(bot: commands.Bot):
    bot.add_cog(ChangePresence(bot))
