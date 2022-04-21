import nextcord
import random
import datetime
import re
import asyncio

from nextcord.ext import commands
from json import load
from pathlib import Path

from words.hunt import animalsToHunt
from words.fish import fishesToCast
from words.beg import begMessages
from util import checkBalance, unbAPI

from cogs.buttons.scout import Scout
import bot_config.config

with Path("./HS.py/bot_config/unb_token.json").open() as f:
    config = load(f)

currency = bot_config.config.currency
boostChannel = 887626373991120946
allowed_channel = [887626373991120946, 846425542165004338]
am = nextcord.AllowedMentions(replied_user=False)


def guessChecker(Guess, bet, choice, ctx, color):
    bet = int(bet)
    Guess = int(Guess)
    if checkBalance(ctx.author.id) < 1:
        embed = nextcord.Embed(
            description=f"You must choose at least {currency}1 for your bet.",
            color=color
        )
        embed.set_author(name=ctx.author,
                         icon_url=ctx.author.avatar.url)
        embed.timestamp = datetime.datetime.utcnow()
        ctx.command.reset_cooldown(ctx)
        return ctx.reply(embed=embed, allowed_mentions=am)

    if bet > 50000:
        moreThan50k = nextcord.Embed(
            description=f"You can't bet more than {currency}50,0000",
            color=color
        )
        moreThan50k.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url)
        moreThan50k.timestamp = datetime.datetime.utcnow()
        ctx.command.reset_cooldown(ctx)
        return ctx.reply(embed=moreThan50k, allowed_mentions=am)

    if Guess >= 51:
        guessMoreThan51 = nextcord.Embed(
            description=f"You can only guess from `0 - 100`",
            color=color
        )
        guessMoreThan51.set_author(name=ctx.author,
                                   icon_url=ctx.author.avatar.url)
        guessMoreThan51.timestamp = datetime.datetime.utcnow()
        ctx.command.reset_cooldown(ctx)
        return ctx.reply(embed=guessMoreThan51, allowed_mentions=am)

    if Guess == choice:
        betDoubled = 5 * bet
        reason = 'Guessed the number'
        unbAPI(betDoubled, reason, ctx.author.id)
        rightGuess = nextcord.Embed(
            description=f"You guessed the correct number and won {currency}{'{:,}'.format(betDoubled)}",
            color=color
        )
        rightGuess.set_author(name=ctx.author,
                              icon_url=ctx.author.avatar.url)
        rightGuess.timestamp = datetime.datetime.utcnow()
        return ctx.reply(embed=rightGuess, allowed_mentions=am)

    elif Guess in range(choice, (choice + 15)) or Guess in range((choice - 15), choice):
        betAlmostGuessed = (2 * bet)
        reason = 'Almost Guessed the number'
        unbAPI(betAlmostGuessed, reason, ctx.author.id)
        first = nextcord.Embed(
            description=f"You didn't guess `{choice}`, but because your guess `{Guess}` "
                        f"was within `{abs(int(Guess) - choice)}` digits "
                        f"away {currency}{'{:,}'.format(betAlmostGuessed)}",
            color=color)
        first.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
        first.timestamp = datetime.datetime.utcnow()
        return ctx.reply(embed=first, allowed_mentions=am)

    elif Guess in range(choice, choice + 10) or Guess in range(choice - 10, choice):
        betAlmostGuessed = (2 * bet) + bet
        reason = 'Almost Guessed the number'
        unbAPI(betAlmostGuessed, reason, ctx.author.id)
        first = nextcord.Embed(
            description=f"You didn't guess `{choice}`, but because your guess `{Guess}` "
                        f"was within `{abs(int(Guess) - choice)}` digits "
                        f"away {currency}{'{:,}'.format(betAlmostGuessed)}",
            color=color)
        first.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
        first.timestamp = datetime.datetime.utcnow()
        return ctx.reply(embed=first, allowed_mentions=am)

    else:
        reason = "Didn't Guessed the number"
        unbAPI(-abs(bet), reason, ctx.author.id)
        third = nextcord.Embed(
            description=f"Uh oh! The number I was thinking of was `{choice}` and lost "f"{currency}{'{:,}'.format(-abs(bet))} ", color=color)
        third.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
        third.timestamp = datetime.datetime.utcnow()
        return ctx.reply(embed=third, allowed_mentions=am)


class Economy(commands.Cog, name="Economy"):
    """ Shows the list of Economy commands
    """

    def __init__(self, bot):
        self.bot = bot

    COG_EMOJI = f"{currency}"

    @commands.cooldown(1, 3600, commands.BucketType.user)
    @commands.command(name="Hourly")
    async def _hourly(self, ctx):
        """ Get your hourly coins """
        hourly_amount = random.randrange(5000, 15000)
        reason = 'Hourly'
        unbAPI(hourly_amount, reason, ctx.author.id)
        embed = nextcord.Embed(
            description=f"Hourly income successfully collected! {currency}{'{:,}'.format(hourly_amount)}",
            color=self.bot.color
        )
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.reply(embed=embed, allowed_mentions=am)

    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.command(name="Beg", aliases=['begging'])
    async def _beg(self, ctx):
        """ This command is used to beg for a random amount of coins """
        if ctx.channel.id not in allowed_channel:
            return
        chance = random.randint(1, 5)
        if chance == 5:
            await ctx.reply(f"You received nothing. Sucks to be you!", allowed_mentions=am)

        else:
            beg_amount = random.randrange(1000, 1500)
            reason = 'Begging'
            unbAPI(beg_amount, reason, ctx.author.id)

            embed = nextcord.Embed(description=f"{random.choice(begMessages)} {currency}{'{:,}'.format(beg_amount)}",
                                   color=self.bot.color)
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.reply(embed=embed, allowed_mentions=am)

    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.command(name="Fish", aliases=['fishing', 'cast'])
    async def _fish(self, ctx):
        """ This command is used to fish for a random amount of coins """
        if ctx.channel.id not in allowed_channel:
            return
        chance = random.randint(1, 5)
        if chance == 5:
            await ctx.reply(f"HAHA! You caught nothing!", allowed_mentions=am)
        else:
            counter = -1
            for _ in fishesToCast:
                counter = counter + 1
            caught = random.randint(0, counter)

            caughtFish = fishesToCast[caught][0]
            lower = fishesToCast[caught][1]
            upper = fishesToCast[caught][2]
            caughtValue = random.randint(lower, upper)

            reason = 'Fishing'
            unbAPI(caughtValue, reason, ctx.author.id)
            embed = nextcord.Embed(description=f"You cast out your line, brought back a {caughtFish} and sold it for "
                                               f"{currency}{'{:,}'.format(caughtValue)}", color=self.bot.color)
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.reply(embed=embed, allowed_mentions=am)

    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.command(name="Hunt", aliases=['hunting'])
    async def _hunt(self, ctx):
        """ This command is used to hunt for a random amount of coins """
        if ctx.channel.id not in allowed_channel:
            return
        chance = random.randint(1, 5)
        if chance == 5:
            await ctx.reply(f"HAHA! You caught nothing.", allowed_mentions=am)
        else:
            counter = -1
            for _ in animalsToHunt:
                counter = counter + 1
            caught = random.randint(0, counter)

            hunted = animalsToHunt[caught][0]
            lower = animalsToHunt[caught][1]
            upper = animalsToHunt[caught][2]
            huntValue = random.randint(lower, upper)

            reason = 'Hunting'
            unbAPI(huntValue, reason, ctx.author.id)
            embed = nextcord.Embed(
                description=f"You caught a {hunted} and sold it for {currency}{'{:,}'.format(huntValue)}",
                color=self.bot.color)
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.reply(embed=embed, allowed_mentions=am)

    @commands.command(name="GuessTheNumber", aliases=["guess", "ntg", "gtn"])
    @commands.cooldown(1, 120, commands.BucketType.user)
    async def GuessTheNumber(self, ctx: commands.Context, Guess, *, bet=None):
        """ Guess the number and win more coins """
        if ctx.channel.id not in allowed_channel:
            return
        await ctx.channel.trigger_typing()
        Guess = int(Guess)
        choice = random.randint(10, 90)
        if re.findall(r"^\d\Be\d$", bet):
            letters = []
            for _ in bet:
                letters.append(_)
            bet = int(letters[0]) * (10 ** int(letters[2]))
            guessChecker(Guess, bet, choice, ctx, self.bot.color)
            return
        if bet == "all":
            if checkBalance(ctx.author.id) < 1:
                embed = nextcord.Embed(
                    description=f"You must choose at least {currency}1 for your bet.",
                    color=self.bot.color
                )
                embed.set_author(name=ctx.author,
                                 icon_url=ctx.author.avatar.url)
                embed.timestamp = datetime.datetime.utcnow()
                await ctx.reply(embed=embed, allowed_mentions=am)
            else:
                bet = checkBalance(ctx.author.id)
                return guessChecker(Guess, bet, choice, ctx, self.bot.color)
        await guessChecker(Guess, bet, choice, ctx, self.bot.color)

    @GuessTheNumber.error
    async def info_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            embed = nextcord.Embed(
                description=f"Too few arguments given.\n\nUsage:\n`guess <guess> <bet>`",
                color=self.bot.color
            )
            ctx.command.reset_cooldown(ctx)
            await ctx.send(embed=embed)

    @commands.command(name="Reward", aliases=['gym'])
    @commands.has_permissions(manage_roles=True)
    async def _reward(self, ctx, amount: int, member: commands.Greedy[nextcord.User]):
        """ This command is used reward participants """
        users = []
        for person in member:
            users.append(person.mention)
            reason = "Reward"
            await asyncio.sleep(3)
            unbAPI(amount, reason, person.id)
        users2 = " and ".join(
            [", ".join(users[:-1]), users[-1]] if len(users) > 2 else users)
        embed = nextcord.Embed(
            description=f"\✅ Added {currency}{'{:,}'.format(amount)} to {users2}"
                        f"'s bank for participating.",
            color=self.bot.color
        )
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.reply(embed=embed, allowed_mentions=am)

    @commands.command(name="Scout", aliases=['search', 'go'])
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def _scout(self, ctx: commands.Context):
        """ Search in areas and earn coins """
        if ctx.channel.id not in allowed_channel:
            return
        view = Scout()
        embed = nextcord.Embed(
            description=f"Where do you want to go?", color=self.bot.color)
        await ctx.reply(embed=embed, view=view, allowed_mentions=am)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if (message.attachments and message.channel.id == 887626373991120946) or (
                message.attachments and message.channel.id == 748943016659648512):
            emoji_reactions = [":meme_sad_cat_thumbsup:764124436353646683",
                               "a:peepoLoving:779332967142785035",
                               "a:peepoGiggle:779333423440986152",
                               ":wowowow:770164675102638090",
                               "a:peepocry:782539657296609310",
                               ":pepetriggered:759382578330730506"
                               ]
            user_id = message.author.id
            memeReward = random.randrange(1000, 5000)
            reason = "Sending Memes"
            await message.add_reaction("💸")
            for i in range(len(emoji_reactions)):
                await message.add_reaction(emoji_reactions[i])
            unbAPI(memeReward, reason, str(user_id))
            await message.clear_reaction("💸")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.bot:
            return
        if before.channel is None and after.channel is not None:
            voice_amount = -1000
            reason = "Joining VC"
            unbAPI(voice_amount, reason, str(member.id))


def setup(bot):
    bot.add_cog(Economy(bot))
