import nextcord
from nextcord.ext import commands


class Sinner(commands.Converter):
    async def convert(self, ctx, argument):
        argument = await commands.MemberConverter().convert(ctx, argument)  # gets a member object
        permission = argument.guild_permissions.manage_messages  # can change into any permission
        if not permission:  # checks if user has the permission
            return argument  # returns user object
        else:
            raise commands.BadArgument(
                "You cannot punish other staff members")  # tells user that target is a staff member


class Moderation(commands.Cog):
    """ Shows the list of Moderation Commands
        """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    COG_EMOJI = "🔨"

    @commands.command(name="clean")
    async def clean(self, ctx, limit: int):
        """Bulk deletes messages"""
        await ctx.purge(limit=limit + 1)  # also deletes your own message
        await ctx.send(f"Bulk deleted `{limit}` messages")

    @commands.command(name="Ban", aliases=["banish"])
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: nextcord.Member = None, reason=None):
        """Casts users out of heaven."""

        if not member:  # checks if there is a user
            return await ctx.send("You must specify a user")

        try:  # Tries to ban user
            await ctx.guild.ban(member, f"By {ctx.author} for {reason}" or f"By {ctx.author} for None Specified")
            await ctx.send(f"{member.mention} was cast out of heaven for {reason}.")
        except nextcord.Forbidden:
            return await ctx.send("Are you trying to ban someone higher than the bot")

    @commands.command(name="SoftBan")
    @commands.has_permissions(ban_members=True)
    async def softban(self, ctx, member: nextcord.Member = None, reason=None):
        """Temporarily restricts access to heaven."""

        if not member:  # checks if there is a user
            return await ctx.send("You must specify a user")

        try:  # Tries to soft-ban user
            await ctx.guild.ban(member, f"By {ctx.author} for {reason}" or f"By {ctx.author} for None Specified")
            await ctx.guild.unban(member, "Temporarily Banned")
        except nextcord.Forbidden:
            return await ctx.send("Are you trying to soft-ban someone higher than the bot?")

    @commands.command(name="SoftBlock")
    @commands.has_permissions(ban_members=True)
    async def softblock(self, ctx, member: nextcord.Member = None):
        """
        Blocks a user from chatting in current channel.

        Similar to mute but instead of restricting access
        to all channels it restricts in current channel.
        """

        if not member:  # checks if there is user
            return await ctx.send("You must specify a user")
        await ctx.channel.set_permissions(member, send_messages=False)

    @commands.command(name="SoftUnblock")
    @commands.has_permissions(ban_members=True)
    async def softunblock(self, ctx, member: nextcord.Member = None):
        """
        Unblocks a user from chatting in current channel.

        Similar to mute but instead of restricting access
        to all channels it restricts in current channel.
        """

        if not member:  # checks if there is user
            return await ctx.send("You must specify a user")
        await ctx.channel.set_permissions(member, send_messages=None)

    @commands.command(name="Block")
    @commands.has_permissions(ban_members=True)
    async def block(self, ctx, member: nextcord.Member = None):
        """
        Blocks a user from viewing in current channel.

        Similar to mute but instead of restricting access
        to all channels it restricts in current channel.
        """

        if not member:  # checks if there is user
            return await ctx.send("You must specify a user")
        await ctx.channel.set_permissions(member, send_messages=False, read_messages=False)

    @commands.command(name="Unblock")
    @commands.has_permissions(ban_members=True)
    async def unblock(self, ctx, member: nextcord.Member = None):
        """
        Unblocks a user from viewing in current channel.

        Similar to mute but instead of restricting access
        to all channels it restricts in current channel.
        """

        if not member:  # checks if there is user
            return await ctx.send("You must specify a user")
        await ctx.channel.set_permissions(member, send_messages=None, read_messages=None)


def setup(bot):
    bot.add_cog(Moderation(bot))
