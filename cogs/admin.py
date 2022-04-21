import sys
import os
import nextcord
from nextcord.ext import commands
from cogs.buttons.roleview import RoleView


def restart_bot():
    os.execv(sys.executable, ['python'] + sys.argv)


class Admin(commands.Cog, name="Admin"):
    """ Admin only commands
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    COG_EMOJI = "❤️‍🔥"

    @commands.command(name='Restart')
    @commands.has_role(748176787670040596)
    async def restart(self, ctx):
        """
        This command is used to restart the bot immediately.
        """
        message = await ctx.send("Restarting bot...")
        await message.edit(content=f"Done!")
        restart_bot()

    @commands.command
    async def giverole(self, ctx):
        testrole = nextcord.utils.find(
            lambda r: r.name == 'Executive', ctx.guild.roles)
        if testrole in ctx.author.roles:
            await ctx.send('You already have this role')
        else:
            await ctx.send('Role assigned')
            await ctx.author.add_roles(testrole)

    @commands.command(name="members")
    async def roles(self, ctx, *, role_wanted: nextcord.Role):
        for role in ctx.guild.roles:
            if role == role_wanted:
                for member in role.members:
                    await ctx.send(member.name)

    @commands.command()
    async def vcmembers(self, ctx):
        # First getting the voice channels
        voice_channel_list = ctx.guild.voice_channels

        # getting the members in the voice channel
        for voice_channels in voice_channel_list:
            # list the members if there are any in the voice channel
            if len(voice_channels.members) != 0:
                if len(voice_channels.members) == 1:
                    await ctx.send("{} member in {}".format(len(voice_channels.members), voice_channels.name))
                else:
                    await ctx.send("{} members in {}".format(len(voice_channels.members), voice_channels.name))
                for members in voice_channels.members:
                    # if user does not have a nickname in the guild, send thier discord name. Otherwise, send thier guild nickname
                    if members.nick is None:
                        await ctx.send(f"{members.name}({members.name.id}")
                    else:
                        await ctx.send(f"{members.nick}({members.nick.id})")

    @commands.command(name="Log")
    @commands.has_any_role(748176787670040596, 763760912058286090)
    async def get_log(self, ctx, member: nextcord.Member, limit: int):
        """
        Shows log for specific user.
        Provide name and number of entries to display
        """
        logs = await ctx.guild.audit_logs(limit=limit, user=member).flatten()
        for log in logs:
            await ctx.channel.send('Performed {0.action} on {0.target}'.format(log))

        await ctx.channel.send("All logs requested have been shown.")

    @commands.command(name="CollegeRoles")
    @commands.has_any_role(748176787670040596, 763760912058286090)
    async def collegeroles(self, ctx: commands.Context):
        """ Used to deploy the college button roles """
        embed = nextcord.Embed(title='🚨 Select your college role',
                               description='**Click** the button below with your corresponding **college**. \n'
                               'After that, head over to <#773935668240973854> to unlock more channels. ',
                               color=15799643)
        await ctx.send(embed=embed, view=RoleView())

    @commands.command(alisas=["removee"])
    @commands.has_any_role(748176787670040596, 763760912058286090)
    async def emojiremove(self, ctx, emoji: nextcord.Emoji):
        """
            Removes the specified emoji from the server.
        """
        guild = ctx.guild
        if ctx.author.guild_permissions.manage_emojis:
            em = nextcord.Embed(
                title="Emoji Success",
                description=f"Successfully deleted (or not :P) {emoji}",
            )
            await ctx.send(embed=em)
            await emoji.delete()


def setup(bot: commands.Bot):
    bot.add_cog(Admin(bot))
