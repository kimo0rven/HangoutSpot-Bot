import nextcord
import logging
import json
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from pathlib import Path
from nextcord.ext import commands

cred = credentials.Certificate('./HS.py/bot_config/database_credentials.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n-----")
secret_file = json.load(open(cwd + '/bot_config/secrets.json'))


def main():
    intents = nextcord.Intents.default()
    intents.members = True
    intents.guilds = True
    intents.messages = True
    intents.presences = True
    bot = commands.Bot(command_prefix=commands.when_mentioned_or('!'),
                       description="Official Bot", case_insensitive=True,
                       help_command=None, intents=intents, owner_id=575577106239717407)
    bot.config_token = secret_file['token']
    bot.remove_command("help")
    bot.color = 15799643
    logging.basicConfig(level=logging.INFO)

    for file in os.listdir(cwd + "/cogs"):
        if file.endswith(".py") and not file.startswith("_"):
            bot.load_extension(f"cogs.{file[:-3]}")

    bot.run(bot.config_token)


if __name__ == "__main__":
    main()
