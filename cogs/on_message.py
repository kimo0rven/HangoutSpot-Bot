import nextcord
from nextcord.ext import commands
from nextcord.utils import get
from PIL import Image, ImageChops, ImageDraw, ImageFont
from io import BytesIO


def circle(pfp, size=(220, 220)):
    pfp = pfp.resize(size, Image.ANTIALIAS).convert("RGBA")

    bigsize = (pfp.size[0] * 3, pfp.size[1] * 3)
    mask = Image.new('L', bigsize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(pfp.size, Image.ANTIALIAS)
    mask = ImageChops.darker(mask, pfp.split()[-1])
    pfp.putalpha(mask)
    return pfp


class Others(commands.Cog):
    """ Other Commands
    """
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    COG_EMOJI = "💬"

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        ignored = (commands.CommandNotFound, commands.UserInputError)
        if isinstance(error, ignored):
            return

        if isinstance(error, commands.CommandOnCooldown):
            m, s = divmod(error.retry_after, 60)
            h, m = divmod(m, 60)
            if int(h) == 0 and int(m) == 0:
                second = int(s)
                embed = nextcord.Embed(
                    description=ctx.author.mention + ", you're still on cooldown! You must wait `" + str(
                        second) + " seconds` to use this command!", color=nextcord.Colour.random())
                await ctx.send(embed=embed)
            elif int(h) == 0 and int(m) != 0:
                minute = int(m)
                second = int(s)
                embed = nextcord.Embed(
                    description=ctx.author.mention + ", you're still on cooldown! You must wait `" + str(
                        minute) + " minutes and " + str(second) + " seconds` to use this command!",
                    color=nextcord.Colour.random())
                await ctx.send(embed=embed)
            else:
                hour = int(h)
                minute = int(m)
                second = int(s)
                embed = nextcord.Embed(
                    description=ctx.author.mention + ", you're still on cooldown! You must wait `" + str(
                        hour) + " hours, " + str(minute) + " minutes and " + str(second) +
                                "seconds` to use this command!", color=nextcord.Colour.random())
                await ctx.send(embed=embed)

        elif isinstance(error, commands.CheckFailure):
            await ctx.send("Hey! You lack the permission to use this command.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == 895302696402288720:
            await message.add_reaction("✅")

    @commands.Cog.listener()
    async def on_message(self, message):
        if "invite link" in message.content:
            await message.channel.send('https://discord.gg/msuiit or https://discord.gg/VxV2NXD')


def setup(bot: commands.Bot):
    bot.add_cog(Others(bot))
