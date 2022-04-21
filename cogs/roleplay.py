import nextcord
import json
import requests

from nextcord.ext import commands
secret_file = json.load(open('bot_config/secrets.json'))
kawaii_token = secret_file['kawaii_token']
color = 15799643


def kawaii(sub):
    r = requests.get(f"https://kawaii.red/api/gif/{sub}/token={kawaii_token}/")
    return str(r.json()["response"])


class Roleplay(commands.Cog):
    """ A List of Roleplay commands
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    COG_EMOJI = "🫂"

    @commands.command(name="Kiss")
    async def kiss(self, ctx, member: nextcord.Member = None):
        """ Kiss someone """
        name = "kiss"
        emoji = "💋"
        if not member:
            member = ctx.author
            target = "someone"
        else:
            target = member.name
        embed = nextcord.Embed(
            description=f"{emoji}**{ctx.author.name}** {name}ed **{target}**", color=color)
        embed.set_image(url=kawaii(name))
        await ctx.send(embed=embed)

    @commands.command(name="Hug")
    async def hug(self, ctx, member: nextcord.Member = None):
        """ Hug someone """
        name = "hug"
        emoji = "👐"
        if not member:
            member = ctx.author
            target = "someone"
        else:
            target = member.name
        embed = nextcord.Embed(
            description=f"{emoji}**{ctx.author.name}** {name}ed **{target}**", color=color)
        embed.set_image(url=kawaii(name))
        await ctx.send(embed=embed)

    @commands.command(name="Slap")
    async def slap(self, ctx, member: nextcord.Member = None):
        """ Slap someone """
        name = "slap"
        emoji = "👋"
        if not member:
            member = ctx.author
            target = "someone"
        else:
            target = member.name
        embed = nextcord.Embed(
            description=f"{emoji}**{ctx.author.name}** {name}ed **{target}**", color=color)
        embed.set_image(url=kawaii(name))
        await ctx.send(embed=embed)

    @commands.command(name="Stone")
    async def stone(self, ctx, member: nextcord.Member = None):
        """ Stone someone """
        name = "stone"
        emoji = "🪨"
        if not member:
            member = ctx.author
            target = "someone"
        else:
            target = member.name
        embed = nextcord.Embed(
            description=f"{emoji}**{ctx.author.name}** {name}ed **{target}**", color=color)
        embed.set_image(url=kawaii(name))
        await ctx.send(embed=embed)

    @commands.command(name="Purr")
    async def purr(self, ctx, member: nextcord.Member = None):
        """ Purr someone """
        name = "purr"
        emoji = "🐱"
        if not member:
            member = ctx.author
            target = "someone"
        else:
            target = member.name
        embed = nextcord.Embed(
            description=f"{emoji}**{ctx.author.name}** {name}ed **{target}**", color=color)
        embed.set_image(url=kawaii(name))
        await ctx.send(embed=embed)

    @commands.command(name="Spin")
    async def spin(self, ctx, member: nextcord.Member = None):
        """ Spin someone """
        name = "spin"
        emoji = "🟡"
        if not member:
            member = ctx.author
            target = "someone"
        else:
            target = member.name
        embed = nextcord.Embed(
            description=f"{emoji}**{ctx.author.name}** {name}ed **{target}**", color=color)
        embed.set_image(url=kawaii(name))
        await ctx.send(embed=embed)

    @commands.command(name="Kill")
    async def kill(self, ctx, member: nextcord.Member = None):
        """ Kill someone """
        name = "kill"
        emoji = "🔪"
        if not member:
            member = ctx.author
            target = "someone"
        else:
            target = member.name
        embed = nextcord.Embed(
            description=f"{emoji}**{ctx.author.name}** {name}ed **{target}**", color=color)
        embed.set_image(url=kawaii(name))
        await ctx.send(embed=embed)

    @commands.command(name="Laugh")
    async def laugh(self, ctx, member: nextcord.Member = None):
        """ Laugh at someone """
        name = "laugh"
        emoji = "😆"
        if not member:
            member = ctx.author
            target = "someone"
        else:
            target = member.name
        embed = nextcord.Embed(
            description=f"{emoji}**{ctx.author.name}** {name}ed **{target}**", color=color)
        embed.set_image(url=kawaii(name))
        await ctx.send(embed=embed)

    @commands.command(name="Love")
    async def love(self, ctx, member: nextcord.Member = None):
        """ Love someone """
        name = "love"
        emoji = "♥️"
        if not member:
            member = ctx.author
            target = "someone"
        else:
            target = member.name
        embed = nextcord.Embed(
            description=f"{emoji}**{ctx.author.name}** {name}ing **{target}**", color=color)
        embed.set_image(url=kawaii(name))
        await ctx.send(embed=embed)

    @commands.command(name="Smile")
    async def smile(self, ctx, member: nextcord.Member = None):
        """ Smile at someone """
        name = "smile"
        emoji = "😄"
        if not member:
            member = ctx.author
            target = "someone"
        else:
            target = member.name
        embed = nextcord.Embed(
            description=f"{emoji}**{ctx.author.name}** {name}ed **{target}**", color=color)
        embed.set_image(url=kawaii(name))
        await ctx.send(embed=embed)

    @commands.command(name="Pat")
    async def pat(self, ctx, member: nextcord.Member = None):
        """ Pat someone """
        name = "Pat"
        emoji = "🤚"
        if not member:
            member = ctx.author
            target = "someone"
        else:
            target = member.name
        embed = nextcord.Embed(
            description=f"{emoji}**{ctx.author.name}** {name}ed **{target}**", color=color)
        embed.set_image(url=kawaii(name))
        await ctx.send(embed=embed)

    @commands.command(name="Happy")
    async def happy(self, ctx):
        """ Celebrate that you're happy """
        name = "happy"
        emoji = "😄"

        embed = nextcord.Embed(
            description=f"{emoji}**{ctx.author.name}** is feeling {name}", color=color)
        embed.set_image(url=kawaii(name))
        await ctx.send(embed=embed)

    @commands.command(name="Cute")
    async def cute(self, ctx):
        """ Are you feeling cute? """
        name = "cute"
        emoji = "🥺"

        embed = nextcord.Embed(
            description=f"{emoji}**{ctx.author.name}** is feeling {name}", color=color)
        embed.set_image(url=kawaii(name))
        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Roleplay(bot))
