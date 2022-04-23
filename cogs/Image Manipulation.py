import nextcord
import json
import requests
import firebase_admin
import datetime

from firebase_admin import credentials, firestore
from nextcord.ext import commands
from PIL import Image, ImageChops, ImageDraw, ImageFont
from io import BytesIO
from json import load
from pathlib import Path

import words.backgrounds
import bot_config.config

with Path("bot_config/unb_token.json").open() as f:
    config = load(f)

cred = credentials.Certificate('./bot_config/database_credentials.json')
firebase_admin.get_app()
db = firestore.client()
token = config["token"]
init_link = config["init_link"]
options = words.backgrounds.options
am = nextcord.AllowedMentions(replied_user=False)
cwd = Path(__file__).parents[1]
cwd = str(cwd)
print(cwd + " test")
def circle(pfp, size=(210, 210)):
    pfp = pfp.resize(size, Image.ANTIALIAS).convert("RGBA")

    bigSize = (pfp.size[0] * 3, pfp.size[1] * 3)
    mask = Image.new('L', bigSize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigSize, fill=250)
    mask = mask.resize(pfp.size, Image.ANTIALIAS)
    mask = ImageChops.darker(mask, pfp.split()[-1])
    pfp.putalpha(mask)
    return pfp


def checkBalance(api_token, gamblerID):
    credit_link = init_link + str(gamblerID)
    unb_cred = requests.get(credit_link,
                            headers={'Authorization': api_token},
                            params={'q': 'requests+language:python'})
    set1 = unb_cred.json()
    cash = set1.get('cash')
    return int(cash)


def unbAPI(amount, reason, api_token, gamblerID):
    credit_link = init_link + str(gamblerID)
    unb_cred = requests.patch(credit_link, data=json.dumps({'cash': amount, 'reason': reason}),
                            headers={'Authorization': api_token}, params={'q': 'requests+language:python'})
    credit = unb_cred.json()
    print(f"{reason}: {credit}")


def option():
    for index in range(len(options)):
        return f"{index}:"


'''def option():
    for count, item in enumerate(options):
        print(f"{count}:{item}")
        return f"{count}:{item}"'''


class ImageManipulation(commands.Cog, name="Image"):
    """
    Shows the list of Image Manipulation Commands
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.colors = [0x0dd2ff, 0x03f5ff, 0x2affa9, 0x18e6ff, 0x17ffc2, 0x03f5ff, 0x30e79d]

    COG_EMOJI = "🖼️"

    @commands.command(name="Profile")
    async def Profile(self, ctx, member: nextcord.Member = None):
        """
        Generates an image of your economy profile
        """
        allowed_channel = [887626373991120946, 846425542165004338]
        if ctx.channel.id not in allowed_channel:
            return
        print(2)
        if not member:
            member = ctx.author
        print(3)
        doc_ref = db.collection(u'users').document(str(member.id))
        doc = doc_ref.get()
        print(doc.exists)
        if not doc.exists:
            doc_ref.set({
                u'Background': "background.png",
                u'Frame': "default.png",
                u'Base': "default.png",
                u'Reborn': 0,
            })
            await ctx.send(f"Registered **{member.display_name}**! `!profile` again.")
            print(doc.exists)
        print('1')
        userid = str(member.id)
        credit_link = init_link + userid
        unb_cred = requests.get(credit_link,
                                headers={'Authorization': token},
                                params={'q': 'requests+language:python'})
        set1 = unb_cred.json()
        rank, cash, bank, total = set1.get('rank'), set1.get(
            'cash'), set1.get('bank'), set1.get('total')
        cash, bank, total = "{:,}".format(
            cash), "{:,}".format(bank), "{:,}".format(total)
        name, nick, memberID = str(member), str(
            member.display_name), str(member.id)
        print('6')
        print(cwd + "/assets/based.png")
        base = Image.open(cwd + "/assets/based.png").convert("RGBA")
        user_bg = doc.to_dict()
        userBackground = user_bg.get("Background")
        print(userBackground)
        background = Image.open(cwd + "/assets/backgrounds/" + userBackground).convert("RGBA")
        print('7')
        pfp = member.display_avatar
        data = BytesIO(await pfp.read())
        pfp = Image.open(data).convert('RGBA')
        name = f"{name[:16]}..." if len(name) > 16 else name
        nick = f"AKA - {nick[:17]}..." if len(nick) > 16 else f"AKA {nick}"
        draw = ImageDraw.Draw(base)

        pfp = circle(pfp, (215, 215))
        font = ImageFont.truetype(cwd + "/assets/AlteHaasGroteskBold.ttf", 38)
        nickFont = ImageFont.truetype(cwd + "/assets/AlteHaasGroteskBold.ttf", 25)
        subfont = ImageFont.truetype(cwd + "/assets/Roboto-Regular.ttf", 25)
        print('10')
        draw.text((280, 245), name, font=font)
        draw.text((270, 310), nick, font=nickFont)
        draw.text((350, 340), rank, font=subfont)
        draw.text((405, 490), total, font=subfont)
        draw.text((65, 490), memberID, font=subfont)
        draw.text((65, 635), cash, font=subfont)
        draw.text((405, 635), bank, font=subfont)
        print('11')
        base.paste(pfp, (56, 158), pfp)
        print('12')
        background.paste(base, (0, 0), base)
        print('13')
        with BytesIO() as a:
            background.save(a, "PNG")
            a.seek(0)
            await ctx.send(file=nextcord.File(a, "profile.png"))
            embed = nextcord.Embed()
            # embed.set_image(url="attachment://profile.png")
            # await ctx.send(embed=embed)

    @commands.command(name="Backgrounds", aliases=["bgs"])
    async def backgrounds(self, ctx):
        for count, item in enumerate(options):
            embed = nextcord.Embed(
                color=15799643
            )
            embed.add_field(name="Backgrounds",
                            value=f"{count}:{item}", inline=True)
            await ctx.send(embed=embed)

    @commands.command(name="SetBG")
    async def setbackground(self, ctx, option: int):
        """
        A command used to change the background of your Economy profile
        """
        if checkBalance(token, ctx.author.id) < 100000:
            embed = nextcord.Embed(
                description=f"You don't have enough money!",
                color=15799643
            )
            embed.set_author(name=ctx.author.name + "#" + ctx.author.discriminator,
                            icon_url=ctx.author.avatar.url)
            embed.timestamp = datetime.datetime.utcnow()
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=embed, allowed_mentions=am)
        doc_ref = db.collection(u'users').document(str(ctx.author.id))

        doc_ref.set({
            u'Background': list(options.values())[option]
        })
        reason = 'Changed profile background'
        amount = -100000
        unbAPI(amount, reason, token, ctx.author.id)
        embed = nextcord.Embed(
            description=f"Successfully changed your background to **{list(options.keys())[option]}** {bot_config.config.currency}"
                        f"-100,000",
            color=15799643
        )
        embed.set_author(name=ctx.author.name + "#" + ctx.author.discriminator,
                         icon_url=ctx.author.avatar.url)
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.reply(embed=embed, allowed_mentions=am)
        print(list(options.values())[option])

    @commands.command(name="Tweet")
    async def _tweet(self, ctx, *, text: str):
        """ Generate a tweet image with your name """
        allowed_channel = [887626373991120946, 866219322421805056, 866385308698017804, 848771072933363732,
                           880375753538170880, 748708955500445737]
        now = datetime.datetime.utcnow()
        if ctx.channel.id not in allowed_channel:
            return
        dateToday = now.strftime("%I:%M %p • %B %d, %Y")

        if len(text) > 140:
            text = f"{text[:140]}"
        total = text
        tweet = ""
        if text.isupper():
            for i, letter in enumerate(total):
                if i % 35 == 0:
                    tweet += '\n'
                tweet += letter
            tweet = tweet[1:]
        if text.islower():
            for i, letter in enumerate(total):
                if i % 45 == 0:
                    tweet += '\n'
                tweet += letter
            tweet = tweet[1:]
        name = str(ctx.author.display_name)
        nick = str(ctx.author)
        base = Image.open(cwd + "/assets/tweet.png").convert("RGBA")
        pfp = ctx.author.display_avatar
        data = BytesIO(await pfp.read())
        pfp = Image.open(data).convert('RGBA')
        name = f"{name}"
        nick = f"@{nick[:17]}..." if len(nick) > 16 else f"@{nick}"
        draw = ImageDraw.Draw(base)

        pfp = circle(pfp, (123, 123))  # avatar size
        font = ImageFont.truetype(cwd + "/assets/segoeuib.ttf", 40)
        nickFont = ImageFont.truetype(cwd + "/assets/segoeui.ttf", 38)
        subfont = ImageFont.truetype(cwd + "/assets/Roboto-Regular.ttf", 51)
        datefont = ImageFont.truetype(cwd + "/assets/Roboto-Regular.ttf", 38)
        draw.text((186, 33), name, font=font)
        draw.text((184, 87), nick, font=nickFont, fill=(129, 151, 166))
        draw.text((32, 182), tweet, font=subfont)
        draw.text((39, 487), dateToday, font=datefont, fill=(129, 151, 166))
        base.paste(pfp, (36, 24), pfp)  # avatar position
        with BytesIO() as a:
            base.save(a, "PNG")
            a.seek(0)
            await ctx.message.delete()
            await ctx.send(file=nextcord.File(a, "profile.png"))


def setup(bot: commands.Bot):
    bot.add_cog(ImageManipulation(bot))
