import math
import traceback

import discord
from discord.ext import commands
from SharedLibrary.discord_utils import similar


class ErrorHandler(commands.Cog):
    """Cog related to the error handler
        Args:
            bot (commands.Bot): the discord bot that will load the Cog
    """

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: discord.DiscordException) -> None:
        """ Every time that an error occur, this function will be called

            Args:
                ctx (commands.Context): main discord parameter, relates to the author and message
                error (discord.DiscordException): error that ocurred 

        """
        error = getattr(error, 'original', error)

        print("[Error] Um erro acabou de acontecer para o usuário {0}.".format(
            str(ctx.author)))

        if isinstance(error, commands.CommandNotFound):
            comandos = [x for x in self.bot.all_commands]
            possiveis = []
            possivel = str(error).split(' ')[1]
            for comando in comandos:
                if similar(possivel, comando) > 0.4:
                    possiveis.append(comando)
            if not possiveis:
                await ctx.message.add_reaction("❌")
                return await ctx.send(f'```Olá usuário, não encontrei o comando {possivel}.'
                                      f'\nTambém não encontrei nenhum possível comando com esse nome.'
                                      f'\nUse o !help para obter ajuda sobre meus comandos.```')
            else:
                valor = '\n-> !'.join([x for x in possiveis])
                return await ctx.send(f'```Olá usuário, não encontrei o comando {possivel}.'
                                      f'\nVocê quis dizer:\n'f'-> !{valor}```')
            return

        elif isinstance(error, commands.BadArgument):
            await ctx.message.add_reaction("❌")
            message = f"**Por favor, coloque um argumento válido!**\n **{error}**"
            return await ctx.send(message)

        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.message.add_reaction("❌")
            missing = [perm.replace('_', ' ').replace(
                'guild', 'server').title() for perm in error.missing_perms]

            if len(missing) > 2:
                fmt = '{}, e {}'.format(
                    "**, **".join(missing[:-1]), missing[-1])
            else:
                fmt = ' e '.join(missing)

            message = "**Eu preciso dessas permissões" \
                " para executar esse comando:** ``{}``".format(fmt)

            return await ctx.send(message)

        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.message.add_reaction("⌛")
            message = f"**Vamos com calma, " \
                f"apressadinho. Tente novamente em** ``{math.ceil(error.retry_after)}`` **segundos.**"
            return await ctx.send(message)

        elif isinstance(error, commands.TooManyArguments):
            await ctx.message.add_reaction("❌")
            return await ctx.send("**Você colocou argumentos demais nessa função.**")


def setup(bot: commands.Bot) -> None:
    bot.add_cog(ErrorHandler(bot))
