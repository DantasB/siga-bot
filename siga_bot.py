import os
import pathlib
import time
from datetime import datetime

import discord
from discord.ext import commands

from Cogs import *
from SharedLibrary.discord_utils import BOT_ICON

INTENTS = discord.Intents.default()
INTENTS.members = True

BOT = commands.Bot(command_prefix=os.getenv('PREFIX'),
                   help_command=None, intents=INTENTS)
REQUIREMENTS = ["error_handler", "siga_handler"]


@ BOT.event
async def on_ready() -> None:
    """ Prints information when the bot is ready
    """
    print('--------------BD--------------')
    print('BOT ONLINE')
    print('Nome do Bot: ' + BOT.user.name)
    print('ID do Bot: ' + str(BOT.user.id))
    print('Versao do Discord: ' + discord.__version__)
    print('--------------BD--------------')
    game = discord.Game(f"!help | Atualmente em {str(len(BOT.guilds))} serve"
                        f"rs com {str(len(set(BOT.get_all_members())))} usuários!")
    await BOT.change_presence(status=discord.Status.online, activity=game)


@ BOT.command(name='help', aliases=['h', 'ajuda'])
async def help(ctx: commands.Context) -> None:
    """ Overrides the discord help method

    Args:
        ctx (object): main discord parameter, relates to the author and message
    """

    print("[Debug] " + str(ctx.author) + " acabou de chamar o comando help")

    embed = discord.Embed(title="Olá, Posso ajudar?", colour=discord.Colour(0xff0000),
                          description="Meu nome é SigaBot. Fui criado para facilitar a vida dos alunos com o acesso ao SIGA - UFRJ")

    embed.set_footer(icon_url=BOT_ICON,
                     text="Usado às {} Horário de Brasília | © {} {} .".format(datetime.now().strftime("%H:%M"),
                                                                               BOT.user.name,
                                                                               datetime.now().strftime("%Y")))

    embed.add_field(name="📜 **document<Login> <Senha> <Tipo do Documento>**", value="Acessa o siga para você e envia no privado o seu documento.",
                    inline=False)

    await ctx.send(embed=embed)


if __name__ == '__main__':
    for cog_file in REQUIREMENTS:
        try:
            print(
                "[Debug] A extensão Cogs.{0} acabou de ser carregada.".format(cog_file))
            BOT.load_extension("Cogs." + cog_file)
        except commands.ExtensionFailed as ex:
            exception = '{}: {}'.format(type(ex).__name__, ex)
            print('Falha ao carregar a extensão {}\n{}'.format(cog_file, exception))


BOT.run(os.getenv('TOKEN'))
