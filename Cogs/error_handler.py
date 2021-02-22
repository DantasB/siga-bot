import discord
import traceback
import math

from discord.ext import commands
from importlib.machinery import SourceFileLoader
discord_utils = SourceFileLoader(
    "discord_utils", "Utils/discord_utils.py").load_module()


class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        ignored = (commands.CommandNotFound)
        error = getattr(error, 'original', error)

        if isinstance(error, ignored):
            comandos = [x for x in self.bot.all_commands]
            possiveis = []
            possivel = str(error).split(' ')[1]
            for comando in comandos:
                if discord_utils.similar(possivel, comando) > 0.4:
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

        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.message.add_reaction("❌")
            return await ctx.send('**Por favor insira os argumentos adequados.**')

        elif isinstance(error, commands.TooManyArguments):
            await ctx.message.add_reaction("❌")
            return await ctx.send("**Você colocou argumentos demais nessa função.**")


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
