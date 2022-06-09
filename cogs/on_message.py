import nextcord
import datetime
import pytz
from nextcord.ext import commands
from nextcord.utils import get
from PIL import Image, ImageChops, ImageDraw, ImageFont
from io import BytesIO
from datetime import datetime
from pathlib import Path

cwd = Path(__file__).parents[1]
cwd = str(cwd)

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

def split(string):
    return string.split()


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
            
    @commands.Cog.listener()
    async def on_message(self, message):
        allowed_channel = [984424711658295326, 866219322421805056, 866385308698017804]
        if message.author.bot: return
        if message.channel.id not in allowed_channel:
            return
        text = message.content
        now = datetime.now(pytz.timezone('Asia/Manila'))
        dateToday = now.strftime("%I:%M %p • %B %d, %Y")
        total = text
        messageContent = " "
        # if text.isupper():
        if text.islower():
            for i, letter in enumerate(total):
                if i % 45 == 0:
                    messageContent += '\n'
                messageContent += letter
            messageContent = messageContent[1:]
        else:
            for i, letter in enumerate(total):
                if i % 36 == 0:
                    messageContent += '\n'
                messageContent += letter
            messageContent = messageContent[1:]
        nick = str(message.author.display_name) #nickname
        name = str(message.author) #username
        base = Image.open(cwd + "/assets/tweet.png").convert("RGBA")
        pfp = message.author.display_avatar
        data = BytesIO(await pfp.read())
        pfp = Image.open(data).convert('RGBA')
        nick = f"{nick}"
        name = f"@{name[:17]}..." if len(name) > 16 else f"@{name}"
        draw = ImageDraw.Draw(base)
        pfp = circle(pfp, (123, 123))
        font = ImageFont.truetype(cwd + "/assets/segoeuib.ttf", 40)
        nickFont = ImageFont.truetype(cwd + "/assets/segoeui.ttf", 38)
        subfont = ImageFont.truetype(cwd + "/assets/Roboto-Regular.ttf", 51)
        datefont = ImageFont.truetype(cwd + "/assets/Roboto-Regular.ttf", 38)
        draw.text((186, 33), nick, font=font)
        draw.text((184, 87), name, font=nickFont, fill=(129, 151, 166))
        draw.text((32, 182), messageContent, font=subfont)
        draw.text((39, 487), dateToday, font=datefont, fill=(129, 151, 166))
        base.paste(pfp, (36, 24), pfp)  # avatar position
        with BytesIO() as a:
            base.save(a, "PNG")
            a.seek(0)
            await message.delete()
            await message.channel.send(file=nextcord.File(a, "profile.png"))

def setup(bot: commands.Bot):
    bot.add_cog(Others(bot))
