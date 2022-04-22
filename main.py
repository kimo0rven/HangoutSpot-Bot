import nextcord
import logging, json, os
import firebase_admin

import bot_config.config

from firebase_admin import credentials, firestore
from pathlib import Path
from nextcord.ext import commands

cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n-----")
cred = credentials.Certificate(cwd + '/bot_config/database_credentials.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

secret_file = json.load(open(cwd + '/bot_config/secrets.json'))
prefix = bot_config.config.prefix

def main():
    intents = nextcord.Intents.default()
    intents.members = True
    intents.guilds = True
    intents.messages = True
    intents.presences = True
    bot = commands.Bot(command_prefix=commands.when_mentioned_or(prefix),
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
