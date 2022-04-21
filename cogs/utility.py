import nextcord
import time
import psutil
import random
import datetime
from nextcord.ext import commands
from datetime import timedelta
from platform import python_version
from time import time
from psutil import Process, virtual_memory
from nextcord import Embed
from nextcord import __version__ as discord_version
from util import unbAPI, convert


am = nextcord.AllowedMentions(replied_user=False)


class Utility(commands.Cog):
    """ A List of Utility commands
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    COG_EMOJI = "🔧"

    @commands.command(name="Report", aliases=["r"])
    async def _report(self, ctx, *, report: str):
        channel = self.bot.get_channel(904737429225865227)
        embed = nextcord.Embed(
            title=f"A new report has been made",
            description=report,
            color=nextcord.Color.red()
        )
        embed.set_author(name=f"{ctx.author}({ctx.author.id})",
                         icon_url=ctx.author.avatar.url)
        embed.timestamp = datetime.datetime.utcnow()
        message = await channel.send(embed=embed)
        await ctx.message.delete()

    @property
    def message(self):
        return self.message.format(users=len(self.bot.users), guilds=len(self.bot.guilds))

    @commands.command(name="Stats", description="")
    async def show_bot_stats(self, ctx):
        """ Displays the current stats of the bot """
        embed = Embed(title=f"{self.bot.user.name} stats",
                      color=self.bot.color,
                      timestamp=nextcord.utils.utcnow()
                      )
        proc = Process()
        with proc.oneshot():
            uptime = timedelta(seconds=time() - proc.create_time())
            cpu_time = timedelta(
                seconds=(cpu := proc.cpu_times()).system + cpu.user)
            mem_total = virtual_memory().total / (1024 ** 2)
            mem_of_total = proc.memory_percent()
            mem_usage = mem_total * (mem_of_total / 100)

        fields = [
            ("Python", python_version(), True),
            ("Nextcord", discord_version, True),
            ("Uptime", uptime, True),
            ("CPU time", cpu_time, True),
            ("CPU Usage",
             f"{psutil.cpu_percent()}% - {psutil.cpu_count()} Threads", True),
            ("Memory usage",
             f"{mem_usage:,.3f} / {mem_total:,.0f} MiB ({psutil.virtual_memory()[2]}%)", True)
        ]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=embed)

    @commands.command(name="userinfo", aliases=["whois"])
    async def userinfo(self, ctx, *, user: nextcord.Member = None):
        """
        Shows the user's info.
        """
        if user is None:
            user = ctx.author
        date_format = "%a, %d %b %Y %I:%M %p"
        embed = nextcord.Embed(color=0xDFA3FF, description=user.mention)
        embed.set_author(name=str(user.name), icon_url=user.display_avatar.url)
        embed.set_thumbnail(url=user.display_avatar.url)
        embed.add_field(
            name="Joined", value=user.joined_at.strftime(date_format))
        members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
        embed.add_field(name="Join position",
                        value=str(members.index(user) + 1))
        embed.add_field(name="Registered",
                        value=user.created_at.strftime(date_format))
        if len(user.roles) > 1:
            role_string = " ".join([r.mention for r in user.roles][1:])
            embed.add_field(
                name="Roles [{}]".format(len(user.roles) - 1),
                value=role_string,
                inline=False,
            )
        embed.set_footer(
            text=self.bot.user.name, icon_url=self.bot.user.display_avatar.url
        )
        return await ctx.send(embed=embed)

    @commands.command(name="ServerInfo")
    async def serverinfo(self, ctx):
        """
        Shows the server's description.
        """
        role_count = len(ctx.guild.roles)
        embed2 = nextcord.Embed(
            timestamp=ctx.message.created_at, color=ctx.author.color
        )
        embed2.add_field(
            name="Verification Level",
            value=str(ctx.guild.verification_level),
            inline=True,
        )
        embed2.add_field(name="Number of roles",
                         value=str(role_count), inline=True)
        embed2.add_field(
            name="Number Of Members", value=ctx.guild.member_count, inline=True
        )
        embed2.add_field(
            name="Created At",
            value=ctx.guild.created_at.__format__("%A, %d. %B %Y @ %H:%M:%S"),
            inline=True,
        )
        embed2.set_thumbnail(url=ctx.guild.icon.url)
        embed2.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon.url)
        embed2.set_footer(
            text=self.bot.user.name, icon_url=self.bot.user.display_avatar.url
        )
        await ctx.send(embed=embed2)

    @commands.command(name='Hub')
    async def hub(self, ctx: commands.Context):
        """ Gives you the link to the school hub """
        await ctx.reply("https://discord.gg/CAmZ2nFBd5")

    @commands.Cog.listener()
    async def inviteLink(self, ctx: commands.Context, message):
        if "invite" in message.content:
            if message.author == self.bot.user:
                return
            await ctx.reply("https://discord.gg/msuiit \n or https://discord.gg/GmPdy6qaSw")

    @commands.command(name="Ping")
    async def _ping(self, ctx: commands.Context):
        """Get the bot's current websocket and API latency."""
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms")

    @commands.command(name="Timestamps")
    async def timestamp(self, ctx):
        message = "```<t:1624385691:t>\n<t:1624385691:T>\n<t:1624385691:d>\n<t:1624385691:D>\n<t:1624385691:f>\n<t:1624385691:F>```\n<t:1624385691:t>\n<t:1624385691:T>\n<t:1624385691:d>\n<t:1624385691:D>\n<t:1624385691:f>\n<t:1624385691:F>"
        await ctx.send(message)

    @commands.command(name="Nick")
    async def nick(self, ctx, *, nickname):
        member = ctx.author
        reason = "Nick Change"
        amount = -20000
        unbAPI(amount, reason, ctx.author.id)
        await member.edit(nick=nickname)
        await ctx.send(f"{member.mention}, your new nickname is `{nickname}`.")

    @commands.command(name="Avatar", aliases=['av', 'pfp'])
    @commands.has_any_role(748176787670040596, 763760912058286090, 897837522925789244, 764030966997712946)
    async def avatar(self, ctx, member: nextcord.Member, arg=''):

        if arg == '':
            member = await self.bot.fetch_user(member.id)
            avatar_embed = nextcord.Embed(
                title='Avatar', color=nextcord.Colour.random())
            avatar_embed.set_image(url=member.avatar.url)
            avatar_embed.set_author(name='{0}#{1}'.format(member.name, member.discriminator),
                                    icon_url=member.avatar.url)

            await ctx.send(embed=avatar_embed)
        else:
            try:
                avatar_embed = nextcord.Embed(
                    title='Guild Avatar', color=nextcord.Colour.random())
                avatar_embed.set_image(url=member.avatar.url)
                avatar_embed.set_author(name='{0}#{1}'.format(member.name, member.discriminator),
                                        icon_url=member.guild_avatar.url)

                await ctx.send(embed=avatar_embed)
            except:
                await ctx.send('The user has no guild avatar set')

    @commands.command(name="cooldowns", aliases=["cd", "cooldown"])
    async def cmdcds(self, ctx):
        """
        Displays the cooldown status of Economy commands.
        """
        cmdlist = [
            'Hourly', 'Beg', 'Fish', 'Hunt', 'Scout', 'GuessTheNumber'
        ]
        embed = nextcord.Embed(
            color=15799643
        )
        cmdView = []
        for cmd in cmdlist:
            cmdName = self.bot.get_command(cmd)
            cd = cmdName.get_cooldown_retry_after(ctx)
            if cmdName.is_on_cooldown(ctx):
                data = {
                    u"Emoji": "<:unavailable:905640472792428625>",
                    u"Command": cmd,
                    u"Cooldown": f"{convert(int(cd))}"
                }
                data = data.copy()
                cmdView.append(data)
            else:
                data = {
                    u"Emoji": "<:available:905640472431718481>",
                    u"Command": cmd,
                    u"Cooldown": "Ready"
                }
                data = data.copy()
                cmdView.append(data)
        embed.set_author(name=ctx.author,
                         icon_url=ctx.author.avatar.url)
        embed.timestamp = datetime.datetime.utcnow()
        embed.add_field(name=f"Commands Cooldown Status", value='\n'.join(
            [f"{bot['Emoji']}{bot['Command']}: `{bot['Cooldown']}`" for bot in cmdView]))
        await ctx.send(embed=embed)

    @commands.command(name="MusicBots", aliases=["Available", "MB"])
    async def available(self, ctx):
        """
        Displays the list of music bots and its status.
        """
        music_bot_role = ctx.guild.get_role(844253341986062336)
        music_bots = music_bot_role.members
        available = []
        unavailable = []
        message_embed = nextcord.Embed(
            title="Music Bots",
            color=15799643
        )
        for bot in music_bots:
            if bot.voice or bot.raw_status == 'offline':
                data = {
                    u"Name": bot.nick,
                    u"ID": bot.id
                }
                data = data.copy()
                unavailable.append(data)
                # embed_from_dict["description"] += f"{bot.mention} - **Unavailable**\n"
            else:
                data = {
                    u"Name": bot.nick,
                    u"ID": bot.id
                }
                data = data.copy()
                available.append(data)
                # embed_from_dict["description"] += f"{bot.mention} - **Available**\n
        available = sorted(available, key=lambda d: d["Name"])
        unavailable = sorted(unavailable, key=lambda d: d["Name"])
        message_embed.add_field(name="Available",
                                value='\n'.join(
                                    [f"🔹{bot['Name']}" for bot in available])
                                )
        message_embed.add_field(name="Unavailable",
                                value='\n'.join(
                                    [f"🔻{bot['Name']}" for bot in unavailable])
                                )
        await ctx.send(embed=message_embed)


def setup(bot: commands.Bot):
    bot.add_cog(Utility(bot))
