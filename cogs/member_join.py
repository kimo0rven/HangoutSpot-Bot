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


class cog_member_join(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: nextcord.Member):
        role = get(member.guild.roles, id=774133374990286872)

        channel = self.bot.get_channel(748393898564518019)
        am = nextcord.AllowedMentions(users=False)
        if not channel:
            return
        await member.add_roles(role)
        await channel.send(
            f"<a:e_duckdance:849776223609421844> Welcome, {member.mention}! <a:e_catclap:827350115408281610>",
            allowed_mentions=am)

        to = f"{member.guild.name.title()}"
        if len(to) > 20:
            to = f"{to[:20]}.."
        memberName = member.name.title()
        if len(memberName) > 15:
            memberName = f"{memberName[:15]}"

        asset = member.display_avatar
        data = BytesIO(await asset.read())
        pfp = Image.open(data).convert("RGB")
        pfp.save("./HS.py/assets/profilereal.png")

        pfp = circle(pfp, (150, 150))
        welcome = Image.open('./assets/welcome.png')
        welcome.paste(pfp, (497, 81), pfp)
        draw = ImageDraw.Draw(welcome)
        frame = Image.open('./assets/frame.png')
        welcome.paste(frame, (398, 7), frame)
        draw = ImageDraw.Draw(welcome)
        w, h = draw.textsize(str(memberName))
        myFont = ImageFont.truetype('./assets/Bella Safira.otf', 30)
        centerX = w/2
        draw.text((572-centerX, 252), memberName, align='center',
                  font=myFont, fill=(245, 222, 85))

        embed = nextcord.Embed(
        )
        channel = get(member.guild.channels, id=887626373991120946)
        with BytesIO() as a:
            welcome.save(a, 'PNG')
            a.seek(0)
            embed.set_image(url="attachment://profile.py.png")
            await channel.send(file=nextcord.File(a, "profile.py.png"))
            # await channel.send(content=member.mention, file=nextcord.File(a, filename="profile.py.png"), embed=embed)


def setup(bot):
    bot.add_cog(cog_member_join(bot))
