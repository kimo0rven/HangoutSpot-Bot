import nextcord
from nextcord.ext import commands, activities


class makeLinkBTN(nextcord.ui.View):
    def __init__(self, link: str):
        super().__init__()
        self.add_item(nextcord.ui.Button(label="Join Game!", url=f"{link}"))


class miniGames(commands.Cog, name="Mini Games"):
    """ Discord Mini Games
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    COG_EMOJI = "😃"

    @commands.group(invoke_without_command=True)
    async def play(self, ctx):
        return

    @play.command(name="Sketch")
    async def _sketch(self, ctx, channel: nextcord.VoiceChannel = None):
        """
        Players sketch pictures of a word prompt to get others to guess the prompt correctly.

        Sketch Heads has two game modes: Classic and Blitz. Classic mode is a competitive battle
        against your friends where you take turns choosing a secret word to draw while everyone else competes
        to guess it as fast as possible! Blitz mode is a chaotic, cooperative race against the clock where
        you split into two teams, Drawers and Guessers. Drawers share a canvas and rapidly draw words while
        the Guessers guess as many as possible before the time runs out.
        """
        if channel is None:
            return await ctx.send("Please specify a channel to join!")

        try:
            invite_link = await channel.create_activity_invite(activities.Activity.sketch)

        except nextcord.HTTPException:
            return await ctx.send("Please mention a voice channel to join and create a game!")
        em = nextcord.Embed(
            title="Sketch", description=f"{ctx.author.mention} has created a game in {channel.mention}")
        em.add_field(name="How to play?",
                     value="It's like Skribble.io but in a vc.")

        await ctx.send(embed=em, view=makeLinkBTN(invite_link))

    @play.command()
    async def poker(self, ctx, channel: nextcord.VoiceChannel = None):
        """
        A Texas hold 'em style game we developed here at Discord. You can play with up to 8 players total per game (you + 7 others), and have up to 17 additional spectators max.
        """
        if channel is None:
            return await ctx.send("Please specify a channel to join!")

        try:
            invite_link = await channel.create_activity_invite(activities.Activity.poker)

        except nextcord.HTTPException:
            return await ctx.send("Please mention a voice channel to join and create a game!")
        em = nextcord.Embed(
            title="Poker", description=f"{ctx.author.mention} has created a game in {channel.mention}")
        em.add_field(name="How to play?", value="Poker but in a VC!")

        await ctx.send(embed=em, view=makeLinkBTN(invite_link))

    @play.command()
    async def betrayal(self, ctx, channel: nextcord.VoiceChannel = None):
        if channel is None:
            return await ctx.send("Please specify a channel to join!")

        try:
            invite_link = await channel.create_activity_invite(activities.Activity.betrayal)

        except nextcord.HTTPException:
            return await ctx.send("Please mention a voice channel to join and create a game!")
        em = nextcord.Embed(title="Betrayal",
                            description=f"{ctx.author.mention} has created a game in {channel.mention}")
        em.add_field(name="How to play?", value="Betrayal but in a VC!")

        await ctx.send(embed=em, view=makeLinkBTN(invite_link))

    @play.command()
    async def awkword(self, ctx, channel: nextcord.VoiceChannel = None):
        if channel is None:
            return await ctx.send("Please specify a channel to join!")

        try:
            invite_link = await channel.create_activity_invite(activities.Activity.awkword)

        except nextcord.HTTPException:
            return await ctx.send("Please mention a voice channel to join and create a game!")
        em = nextcord.Embed(title="Awkword",
                            description=f"{ctx.author.mention} has created a game in {channel.mention}")
        em.add_field(name="How to play?", value="Awkword but in a VC!")

        await ctx.send(embed=em, view=makeLinkBTN(invite_link))

    @play.command(name="Checker")
    async def checker(self, ctx, channel: nextcord.VoiceChannel = None):
        """
        An Activity that we've developed here at Discord for playing checkers with your friends!
        """
        if channel is None:
            return await ctx.send("Please specify a channel to join!")

        try:
            invite_link = await channel.create_activity_invite(activities.Activity.checker)

        except nextcord.HTTPException:
            return await ctx.send("Please mention a voice channel to join and create a game!")
        em = nextcord.Embed(title="Checker",
                            description=f"{ctx.author.mention} has created a game in {channel.mention}")
        em.add_field(name="How to play?", value="Checker but in a VC!")

        await ctx.send(embed=em, view=makeLinkBTN(invite_link))

    @play.command(name="Chess")
    async def chess(self, ctx, channel: nextcord.VoiceChannel = None):
        """
        An Activity that we've developed here at Discord for playing chess with your friends!
        """
        if channel is None:
            return await ctx.send("Please specify a channel to join!")

        try:
            invite_link = await channel.create_activity_invite(activities.Activity.chess)

        except nextcord.HTTPException:
            return await ctx.send("Please mention a voice channel to join and create a game!")
        em = nextcord.Embed(title="Chess",
                            description=f"{ctx.author.mention} has created a game in {channel.mention}")
        em.add_field(name="How to play?", value="Chess but in a VC!")

        await ctx.send(embed=em, view=makeLinkBTN(invite_link))

    @play.command()
    async def fishington(self, ctx, channel: nextcord.VoiceChannel = None):
        """
        An online fishing game where you can relax, chat and fish with up to 24 players!
        """
        name = "Fishington"
        if channel is None:
            return await ctx.send("Please specify a channel to join!")

        try:
            invite_link = await channel.create_activity_invite(activities.Activity.fishington)

        except nextcord.HTTPException:
            return await ctx.send("Please mention a voice channel to join and create a game!")
        em = nextcord.Embed(title=f"{name}",
                            description=f"{ctx.author.mention} has created a game in {channel.mention}")
        em.add_field(name="How to play?", value=f"{name} but in a VC!")

        await ctx.send(embed=em, view=makeLinkBTN(invite_link))

    @play.command()
    async def letter_league(self, ctx, channel: nextcord.VoiceChannel = None):
        """
        A game where you and your friends take turns placing letters on a shared game board to create words in a crossword-style. Spelling words with high earning letters and placing letters on special spaces earn players more points, so get your dictionaries and thesauri ready!
        """
        name = "Letter League"
        if channel is None:
            return await ctx.send("Please specify a channel to join!")

        try:
            invite_link = await channel.create_activity_invite(activities.Activity.letter_league)

        except nextcord.HTTPException:
            return await ctx.send("Please mention a voice channel to join and create a game!")
        em = nextcord.Embed(title=f"{name}",
                            description=f"{ctx.author.mention} has created a game in {channel.mention}")
        em.add_field(name="How to play?", value=f"{name} but in a VC!")

        await ctx.send(embed=em, view=makeLinkBTN(invite_link))

    @play.command()
    async def letter_tile(self, ctx, channel: nextcord.VoiceChannel = None):
        name = "Letter Tile"
        if channel is None:
            return await ctx.send("Please specify a channel to join!")

        try:
            invite_link = await channel.create_activity_invite(activities.Activity.letter_tile)

        except nextcord.HTTPException:
            return await ctx.send("Please mention a voice channel to join and create a game!")
        em = nextcord.Embed(title=f"{name}",
                            description=f"{ctx.author.mention} has created a game in {channel.mention}")
        em.add_field(name="How to play?", value=f"{name} but in a VC!")

        await ctx.send(embed=em, view=makeLinkBTN(invite_link))

    @play.command()
    async def ocho(self, ctx, channel: nextcord.VoiceChannel = None):
        name = "Ocho"
        if channel is None:
            return await ctx.send("Please specify a channel to join!")

        try:
            invite_link = await channel.create_activity_invite(activities.Activity.ocho)

        except nextcord.HTTPException:
            return await ctx.send("Please mention a voice channel to join and create a game!")
        em = nextcord.Embed(title=f"{name}",
                            description=f"{ctx.author.mention} has created a game in {channel.mention}")
        em.add_field(name="How to play?", value=f"{name} but in a VC!")

        await ctx.send(embed=em, view=makeLinkBTN(invite_link))

    @play.command()
    async def spellcast(self, ctx, channel: nextcord.VoiceChannel = None):
        name = "Spell Cast"
        if channel is None:
            return await ctx.send("Please specify a channel to join!")

        try:
            invite_link = await channel.create_activity_invite(activities.Activity.spellcast)

        except nextcord.HTTPException:
            return await ctx.send("Please mention a voice channel to join and create a game!")
        em = nextcord.Embed(title=f"{name}",
                            description=f"{ctx.author.mention} has created a game in {channel.mention}")
        em.add_field(name="How to play?", value=f"{name} but in a VC!")

        await ctx.send(embed=em, view=makeLinkBTN(invite_link))

    @play.command()
    async def word_snacks(self, ctx, channel: nextcord.VoiceChannel = None):
        name = "Word Snacks"
        if channel is None:
            return await ctx.send("Please specify a channel to join!")

        try:
            invite_link = await channel.create_activity_invite(activities.Activity.word_snacks)

        except nextcord.HTTPException:
            return await ctx.send("Please mention a voice channel to join and create a game!")
        em = nextcord.Embed(title=f"{name}",
                            description=f"{ctx.author.mention} has created a game in {channel.mention}")
        em.add_field(name="How to play?", value=f"{name} but in a VC!")

        await ctx.send(embed=em, view=makeLinkBTN(invite_link))

    @play.command()
    async def youtube(self, ctx, channel: nextcord.VoiceChannel = None):
        """
        Watch together Youtube with friends!
        """
        name = "Youtube"
        if channel is None:
            return await ctx.send("Please specify a channel to join!")

        try:
            invite_link = await channel.create_activity_invite(activities.Activity.youtube)

        except nextcord.HTTPException:
            return await ctx.send("Please mention a voice channel to join and create a game!")
        em = nextcord.Embed(title=f"{name}",
                            description=f"{ctx.author.mention} has created a game in {channel.mention}")
        em.add_field(name="How to play?", value=f"{name} but in a VC!")

        await ctx.send(embed=em, view=makeLinkBTN(invite_link))


def setup(bot):
    bot.add_cog(miniGames(bot))
