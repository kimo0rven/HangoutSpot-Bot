from nextcord.ext import commands
import nextcord
import nextcord.ext.commands

import bot_config.config
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('./bot_config/database_credentials.json')
firebase_admin.get_app()
db = firestore.client()
confessionChannel = bot_config.config.confessionChannel


class Confession(commands.Cog):
    """ Shows the Confession command
    """

    def __init__(self, bot):
        self.bot = bot

    COG_EMOJI = "🌸"

    @commands.command(name="confess")
    async def dm_command(self, ctx: commands.Context, *, confession: str):
        """ DM the bot to send your confession """
        guild = self.bot.get_guild(748105410162065409)
        guild_icon = guild.icon
        doc_ref = db.collection(u'Confession').document(u'Number')
        doc = doc_ref.get()
        set1 = doc.to_dict()
        number = set1.get("confess_number")
        color = nextcord.Colour.random()

        if isinstance(ctx.channel, nextcord.channel.DMChannel):
            if len(confession) < 151:
                embed = nextcord.Embed(
                    description=f"Your confession must be at least 150 characters.",
                    color=nextcord.Colour.random()
                )
                await ctx.author.send(embed=embed, delete_after=5)
                self.dm_command.reset_cooldown(ctx)
                return
            channel = self.bot.get_channel(confessionChannel)
            embed = nextcord.Embed(description=confession,
                                   color=color)

            embed.set_author(
                name=f"Anonymous Confession #{number}",
                icon_url=guild_icon
            )

            embed.set_footer(
                text='DM me "!confess (description)" to send a confession ')
            embed.timestamp = nextcord.utils.utcnow()
            await channel.send(embed=embed)
            number = number + 1
            data = {
                u'confess_number': number
            }
            db.collection(u'Confession').document(u'Number').set(data)

            embed = nextcord.Embed(
                description=f"{ctx.author.mention}, your anonymous confession was successfully posted to **{guild.name}**!",
                color=color)
            embed.set_author(name=f"Confessions » {guild.name}", url="https://discord.gg/GmPdy6qaSw",
                             icon_url=ctx.author.avatar.url
                             )
            embed.add_field(name="Confession: ", value=f"||{confession}||", inline=True)
            embed.add_field(name="Channel:", value=f"<#{confessionChannel}>", inline=True)
            embed.set_footer(text=" ")
            embed.timestamp = nextcord.utils.utcnow()
            await ctx.author.send(embed=embed)


def setup(bot):
    bot.add_cog(Confession(bot))
