import os
import traceback
import discord
from discord.ext import commands

#環境変数読み込み
token = os.environ['BOT_TOKEN'] #自分のBotトークンに書き換え

INITIAL_EXTENSIONS = [
    "cogs.control"
]

class MyBot(commands.Bot):

    def __init__(self, command_prefix,intents=discord.Intents.all()):
        super().__init__(command_prefix=command_prefix,intents=intents)

        for cog in INITIAL_EXTENSIONS:
            try:
                self.load_extension(cog)
            except Exception:
                traceback.print_exc()

    async def on_ready(self):
        print("Logged in as " + client.user.name)
        print("-----")

if __name__ == '__main__':
    client = MyBot(command_prefix="/")
    client.run(token)