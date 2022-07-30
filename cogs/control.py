from discord.ext import commands
from cogs.werewolf import *
from cogs import createEmbed
from discord.commands import SlashCommandGroup
import os

guildId=int(os.environ['GUILD_ID']) #Botを使用するサーバーIDに書き換え

class Werewolf(commands.Cog,name="Werewolf"):
    def __init__(self,bot):
        self.bot = bot

    wwg = SlashCommandGroup("wwg", "人狼ゲームに関連するコマンド",guild_id=[guildId])

    @wwg.command(name="start",description="人狼ゲームを開始します",guild_id=[guildId])
    async def start(self,ctx):
        game = WerewolfGame()
        embed,view = await createEmbed.mainEmbed(game)
        await ctx.respond(embed=embed,view=view)

def setup(bot):
    bot.add_cog(Werewolf(bot))
