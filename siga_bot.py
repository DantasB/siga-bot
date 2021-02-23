import os
import pathlib
import time
from datetime import datetime

import discord
from discord.ext import commands

from Cogs import *
from SharedLibrary import *

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix=os.getenv('PREFIX'),
                   help_command=None, intents=intents)
requirements = ["error_handler", "siga_handler"]


@bot.event
async def on_ready():

    print('--------------BD--------------')
    print('BOT ONLINE')
    print('Nome do Bot: ' + bot.user.name)
    print('ID do Bot: ' + str(bot.user.id))
    print('Versao do Discord: ' + discord.__version__)
    print('--------------BD--------------')
    game = discord.Game(f"!help | Atualmente em {str(len(bot.guilds))} serve"
                        f"rs com {str(len(set(bot.get_all_members())))} usuários!")
    await bot.change_presence(status=discord.Status.online, activity=game)


@bot.command(name='help', aliases=['h', 'ajuda'])
async def help(ctx):

    print("[Debug] " + str(ctx.author) + " acabou de chamar o comando help")

    embed = discord.Embed(title="Olá, Posso ajudar?", colour=discord.Colour(0xff0000),
                          description="Meu nome é SigaBot. Fui criado para facilitar a vida dos alunos com o acesso ao SIGA - UFRJ")

    embed.set_footer(icon_url=discord_utils.bot_icon,
                     text="Usado às {} Horário de Brasília | © {} {} .".format(datetime.now().strftime("%H:%M"),
                                                                               bot.user.name,
                                                                               datetime.now().strftime("%Y")))

    embed.add_field(name="📜 **document<Login> <Senha> <Tipo do Documento>**", value="Acessa o siga para você e envia no privado o seu documento.",
                    inline=False)

    await ctx.send(embed=embed)


if __name__ == '__main__':
    for cog_file in requirements:
        try:
            bot.load_extension("Cogs." + cog_file)
            print(
                "[Debug] A extensão Cogs.{0} acabou de ser carregada.".format(cog_file))
        except Exception as ex:
            exception = '{}: {}'.format(type(ex).__name__, ex)
            print('Falha ao carregar a extensão {}\n{}'.format(cog_file, exception))


bot.run(os.getenv('TOKEN'))
