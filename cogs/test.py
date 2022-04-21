import nextcord
import random
import asyncio

from nextcord.ext import commands
from util import checkBalance, unbAPI

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('./bot_config/database_credentials.json')
firebase_admin.get_app()
db = firestore.client()

currency = "**⌬**"
color = 15799643

game_items = [
    {"Item": {"chance": [1, 100], "emoji": "emoji", "name": "item",
              "description": "a description", "price": 0, "rarity": "rare", "type": "craft"}},
    {"Item": {"chance": [1, 100], "emoji": "emoji", "name": "item",
              "description": "a description", "price": 0, "rarity": "rare", "type": "craft"}}

]

shop = [
    {"Emoji": "⛏", "Name": "Pickaxe", "Price": 50,
        "ID": "pickaxe", "Description": "Used to dig"},
    {"Emoji": "🪓", "Name": "Axe", "Price": 50,
        "ID": "axe", "Description": "Used to cut woods"},
    {"Emoji": "🎣", "Name": "Fishing Rod", "Price": 50,
        "ID": "fishingrod", "Description": "Used to catch fish"},
    {"Emoji": "⚔", "Name": "Swords", "Price": 50,
        "ID": "swords", "Description": "Used to fight monsters"},
    {"Emoji": "🔫", "Name": "Gun", "Price": 50,
        "ID": "gun", "Description": "Used to hunt animals"}
]


async def open_account(user):
    game = db.collection(u'Game').document(f'{str(user)}')
    get = game.get()
    if not get.exists:
        game.set({
            u'balance': 0,
            u'level': 0,
            u'inventory': {"axe": {'amount': 1, 'emoji': '🪓', 'name': 'axe'},
                           "pickaxe": {'amount': 1, 'emoji': '⛏', 'name': 'Pickaxe'},
                           "fishing rod": {'amount': 1, 'emoji': '🎣', 'name': 'Fishing Rod'},
                           "swords": {'amount': 1, 'emoji': '⚔', 'name': 'Swords'},
                           "gun": {'amount': 1, 'emoji': '🔫', 'name': 'Gun'}
                           }
        }, merge=True)


async def update_balance(user, amount=0):
    game = db.collection(u'Game').document(f'{str(user)}')
    get = game.get()
    balance = get.to_dict().get("balance")
    balance = balance + amount
    game.update({
        u'balance': balance
    })


class HangoutSpotGame(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="Start")
    async def start(self, ctx):
        doc_ref = db.collection('Game').document(str(ctx.author.id))
        doc = doc_ref.get()
        if doc.exists:
            await ctx.send(f"You already have created an account!")
        else:
            await open_account(ctx.author.id)
            await ctx.send(f"Account Created!")

    @commands.Cog.listener()
    async def on_message(self, message):
        chance = random.randint(1, 100)
        amount = random.randint(1, 5)
        user_id = message.author.id
        if message.author == self.bot.user:
            return
        if message.channel.id == 887626373991120946:
            if chance == 1:
                embed = nextcord.Embed(
                    description=f"Someone dropped {currency}{amount}. Quick! type `!grab` before someone gets it!",
                    color=nextcord.Color.green()
                )
                message = await message.channel.send(embed=embed)
                def check(m): return m.content == "!grab"
                try:
                    confirm = await self.bot.wait_for(event='message', check=check, timeout=30)
                except asyncio.TimeoutError:
                    embed = nextcord.Embed(
                        description=f"No one grabbed the drop.",
                        color=nextcord.Color.red()
                    )
                    await message.edit(embed=embed, delete_after=300)
                    return
                if "!grab" in confirm.content:
                    embed = nextcord.Embed(
                        description=f"<@{user_id}> was quick enough to grab {currency}{amount}!",
                        color=color
                    )
                    await message.edit(embed=embed)
                    game = db.collection(u'Game').document(f'{user_id}')
                    get = game.get()
                    if not get.exists:
                        await message.channel.send(f"Type `!start` to register!")
                    else:
                        balance = get.to_dict().get("balance")
                        print(balance)
                        balance = balance + amount
                        game.update({
                            u'balance': balance
                        })
                    return
        await asyncio.sleep(60)

    @commands.command(name="Bag", aliases=["Inventory", "inv", "i"])
    async def storage(self, ctx):
        game = db.collection(u'Game').document(str(ctx.author.id))
        bag = game.get()
        x = bag.to_dict().get(u'inventory')
        balance = bag.to_dict().get("balance")
        embed_from_dict = {
            'title': 'Player Inventory',
            'description': f"Money: {currency} {'`{:,}`'.format(balance)}\n\nItems:\n",
            'color': 15799643,
            'author': {'name': f'{ctx.author}', 'icon_url': ctx.author.avatar.url}
        }
        for y, z in x.items():
            if isinstance(z, dict):
                embed_from_dict['description'] += f"{z['emoji']} {z['name']} - {z['amount']}\n"

        await ctx.send(embed=nextcord.Embed.from_dict(embed_from_dict))

    @commands.command(name="Shop")
    async def shop(self, ctx):
        embed = nextcord.Embed(title="Shop", color=color)
        for item in shop:
            emoji = item["Emoji"]
            name = item["Name"]
            price = item["Price"]
            desc = item["Description"]
            item_id = item["ID"]
            embed.add_field(
                name=f"{emoji} {name} - {currency} {price}", value=f"ID:`{item_id}`\n```{desc}```")
        await ctx.send(embed=embed)

    @commands.command(name="Buy", aliases=["b"])
    async def buy(self, ctx, item, amount=1):
        doc_ref = db.collection(u'Game').document(str(ctx.author.id))
        doc_fetched = doc_ref.get()
        item = item.lower()
        item_id = item_price = item_name = item_emoji = oldAmount = None
        shop_item = []
        inventory = doc_fetched.to_dict().get(u'inventory')
        balance = doc_fetched.to_dict().get(u'balance')
        for s in shop:
            if s.get('ID') == item:
                item_id = str(s["ID"])
                item_name = s["Name"]
                item_price = s["Price"]
                item_emoji = s["Emoji"]
                shop_item.append(item_id)

        if item is None or item not in shop_item:
            await ctx.send(f"**{item}** doesn't exist or is not an item")
        elif item_id in shop_item:
            cost = item_price * amount
            for z, x in inventory.items():
                if z == item:
                    oldAmount = x['amount']
            if balance < cost:
                await ctx.send(f"You don't have enough money to buy {amount} {item}.")
            else:
                await update_balance(ctx.author.id, -cost)
                newAmount = oldAmount + amount
                doc_ref.set({u'inventory': {f'{item_id}': {
                    u'name': item_name,
                    u'emoji': item_emoji,
                    u'amount': newAmount}}}, merge=True)
                await ctx.send(f"You bought `{amount}` {item} for {currency} `{cost}`")


def setup(bot):
    bot.add_cog(HangoutSpotGame(bot))
