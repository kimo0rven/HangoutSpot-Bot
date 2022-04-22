import asyncio
import nextcord
import random

from nextcord.ext import commands


am = nextcord.AllowedMentions(replied_user=False)

def text_to_owo(text):
    """ Converts your text to OwO """
    smileys = [';;w;;', '^w^', '>w<', 'UwU', '(・`ω\´・)', '(´・ω・\`)']

    text = text.replace('L', 'W').replace('l', 'w')
    text = text.replace('R', 'W').replace('r', 'w')

    text = last_replace(text, '!', '! {}'.format(random.choice(smileys)))
    text = last_replace(text, '?', '? owo')
    text = last_replace(text, '.', '. {}'.format(random.choice(smileys)))

    vowels = ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U']

    for v in vowels:
        if 'n{}'.format(v) in text:
            text = text.replace('n{}'.format(v), 'ny{}'.format(v))
        if 'N{}'.format(v) in text:
            text = text.replace('N{}'.format(v), 'N{}{}'.format(
                'Y' if v.isupper() else 'y', v))

    return text
 

def last_replace(s, old, new):
    li = s.rsplit(old, 1)
    return new.join(li)


class Fun(commands.Cog):
    """
    Shows the list of Fun commands
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    COG_EMOJI = "😃"

    @commands.command(name="Say", aliases=["Echo"])
    async def echo(self, ctx, *, message=None):
        """ Make the bot say whatever you want! """
        message = message or "Please provide a message."

        await ctx.message.delete()
        await ctx.send(message)

    @commands.command(name="8ball", aliases=["ask", "eightball"])
    async def _8ball(self, ctx):
        """ Ask the the magic 8ball about your future """
        allowed_channel = [887626373991120946, 848771072933363732, 880375753538170880, 806553902425309244, 922948197498888202]
        if ctx.channel.id not in allowed_channel:
            return
        responses = ["It is certain", " It is decidedly so", "Without a doubt", "Yes definitely",
                    "You may rely on it", "As I see it, yes", "Most likely", "Outlook good",
                    "Yes", "Signs point to yes", "Reply hazy, try again", "Ask again later",
                    "Better not tell you now", "Cannot predict now", "Concentrate and ask again",
                    "Don't count on it", "My reply is no", "My sources say no", "Outlook not so good",
                    "Very doubtful"]    
        randomized_responses = random.choice(responses)
        await ctx.send("🎱 | " + randomized_responses + ", **" + str(ctx.author.name + "**"))

    @commands.command(name='Choose', description='For when you wanna settle the score some other way')
    async def _choose(self, ctx, *choices: str):
        """Chooses between multiple choices."""
        allowed_channel = [887626373991120946, 848771072933363732, 880375753538170880, 806553902425309244, 922948197498888202]
        if ctx.channel.id not in allowed_channel:
            return
        await ctx.send(f'**{ctx.author.name}**, I choose ```{random.choice(choices)}```')

    @commands.command(name='Dice')
    async def _dice(self, ctx, dice: str):
        """ Rolls a dice in NdN format. """
        allowed_channel = [887626373991120946, 848771072933363732, 880375753538170880, 806553902425309244, 922948197498888202]
        if ctx.channel.id not in allowed_channel:
            return
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await ctx.send('Format has to be in NdN!')
            return

        result = ', '.join(str(random.randint(1, limit)) for _ in range(rolls))
        await ctx.send(result)

    @commands.command(name='Owo', brief="Any message to owo")
    async def owo(self, ctx):
        """ Convert any sentence into an OwO """
        await ctx.message.delete()
        await ctx.send(text_to_owo(ctx.message.content[5:]))

    @commands.command(name="Coffee", aliases=['cafe', 'kopi'])
    async def coffee(self, ctx, member: nextcord.Member = None):
        """ Enjoy coffee with someone """
        if member.bot: 
            return
        if member == ctx.author or not member:
            await ctx.send(embed=nextcord.Embed(
                description=f"☕ | {ctx.author.name} is enjoying Coffee alone :smirk: ",
                color=3092790)
            )
        elif member == self.bot.user:
            await ctx.send(embed=nextcord.Embed(
                description="☕ | Don't worry I will drink coffee with you *sips*",
                color=3092790)
            )
            return

        coffee_msg = await ctx.send(embed=nextcord.Embed(
            description=f"☕ | {member.mention}, you got a coffee offer from {ctx.author.name}",
            color=3092790)
        )
        await coffee_msg.add_reaction('☕')

        def check(reaction, user):
            return user == member and str(reaction.emoji) == '☕'

        try:
            await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send(
                embed=nextcord.Embed(
                    description=f"Looks like {member.name} is busy", color=3092790)
            )
        else:
            await coffee_msg.delete()
            await ctx.send(embed=nextcord.Embed(
                description=f"☕ | Yay! {ctx.author.name} and {member.name} are enjoying coffee together!",
                color=3092790))

    @commands.command(name="Beer", aliases=['Drink', 'Shat'])
    async def beer(self, ctx, member: nextcord.Member = None):
        """ Drink beer with someone """
        if member.bot:
            return
        if member == ctx.author or not member:
            await ctx.send(embed=nextcord.Embed(description=f"🍺 | {ctx.author.name} Party Time !! , *Enjoying Beer*",
                                                color=3092790))
            return
        elif member == self.bot.user:
            await ctx.send(embed=nextcord.Embed(description="🍺 | Don't worry I will Enjoy beer with you  *brr*",
                                                color=3092790))
            return

        coffee_msg = await ctx.send(embed=nextcord.Embed(
            description=f"🍺 | {member.mention}, you got Beer Party offer from {ctx.author.name}",
            color=3092790)
        )
        await coffee_msg.add_reaction('🍺')

        def check(reaction, user):
            return user == member and str(reaction.emoji) == '🍺'

        try:
            await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send(embed=nextcord.Embed(
                description=f"Looks like {member.name} is busy",
                color=3092790)
            )
        else:
            await coffee_msg.delete()
            await ctx.send(embed=nextcord.Embed(
                description=f"🍺 | Yay! {ctx.author.name} and {member.name} are enjoying Beer Party!", color=3092790))

    @commands.command(name="Roll")
    async def roll(self, ctx):
        """ Receive a number from 1-100 """
        roll = random.randint(1, 100)
        embed = nextcord.Embed(
            description=f"🎲 You rolled **{roll}**",
            color=3092790
        )
        await ctx.reply(embed=embed, allowed_mentions=am)

    @commands.command(name="Hello")
    async def hello(self, ctx):
        """ Say hello to the bot """
        await ctx.reply('Hello!')


def setup(bot):
    bot.add_cog(Fun(bot))
