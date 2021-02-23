from datetime import datetime

import discord
from discord.ext import commands
from SharedLibrary import *

import siga_core


class SigaHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.dm_only()
    @commands.command(name='document', aliases=['documento'])
    async def document(self, ctx, login, password, doc_type):
        print("[Debug] " + str(ctx.author) +
              " acabou de chamar o comando document.")
        login = siga_utils.treat_login(login)
        if(login == ""):
            print("[Error] O usuário: {0} digitou o cpf incorreto {1}.".format(
                str(ctx.author), str(login)))
            raise commands.MissingRequiredArgument

        print("[Debug] O CPF inserido pelo " +
              str(ctx.author) + " é válido.")

        if not discord_utils.is_valid_document(doc_type):
            print("[Error] O usuário: {0} digitou {1} como doctype porém este não se encontra na lista.".format(
                str(ctx.author), str(doc_type)))
            raise commands.UserInputError

        print("[Debug] O doc_type: " + doc_type + ", inserido pelo " +
              str(ctx.author) + " é válido.")

        msg = await ctx.send("Aguarde! Estou baixando seu documento.")
        print("[Debug] O " + doc_type + " do " +
              str(ctx.author) + " acabou de ser baixado.")
        file_path = await siga_core.get_document_from_siga(
            login, password, str(ctx.author), doc_type.lower())

        if not pdf_utils.is_valid_file_path(file_path):
            print("[Error] O usuário: {0} tentou baixar o seguinte doc_type {1} mas não conseguiu. Algum erro aconteceu na requisição.".format(
                str(ctx.author), str(doc_type)))
            raise commands.CheckFailure

        print("[Debug] O " + str(doc_type) +
              " foi baixado do SIGA com sucesso.")

        await ctx.send(file=discord.File(file_path))
        print("[Debug] O " + doc_type + " do " +
              str(ctx.author) + " acabou de ser enviado.")

        pdf_utils.delete_document(file_path)

    @document.error
    async def document_handler(self, ctx, error):
        if(isinstance(error, commands.MissingRequiredArgument)):
            embed = discord.Embed(title="Comando !document:", colour=discord.Colour(0xff0000),
                                  description="Você baixa o documento de interesse.\n \n**Como"
                                  " usar: !document <Login> <Senha> <Tipo do Documento>**\n \n**"
                                  "Só funciona no privado**")

            embed.set_author(
                name="Opa! Um erro aconteceu. Verifique seu Login, Senha ou Tipo de documento estão corretos.")
            embed.set_footer(icon_url=discord_utils.bot_icon,
                             text="Usado às {} Horário de Brasília | © {} {} .".format(datetime.now().strftime("%H:%M"),
                                                                                       self.bot.user.name,
                                                                                       datetime.now().strftime("%Y")))

            embed.add_field(name="📖**Exemplos:**", value="!document 37584937063 batata234 crid\n!documento 81709558075 gshBgjds123 boletim",
                            inline=False)
            embed.add_field(name="📜**Lista de documentos:**", value="historico, boletim, boa, crid, bolsista, cotista, regularmente_matriculado, declaracao_passe_livre.",
                            inline=False)
            embed.add_field(name="🔀**Outros Comandos**",
                            value="``!documento``", inline=False)

            msg = await ctx.send(embed=embed)
            await msg.add_reaction("❓")
            return

        if isinstance(error, commands.PrivateMessageOnly):
            embed = discord.Embed(title="Comando !document:", colour=discord.Colour(0xff0000),
                                  description="Você baixa o documento de interesse.\n \n**Como"
                                  " usar: !document <Login> <Senha> <Tipo do Documento>**\n \n**"
                                  "Só funciona no privado**")

            embed.set_author(
                name="Opa! Um erro aconteceu. Você só pode enviar esse comando no privado.")
            embed.set_footer(icon_url=discord_utils.bot_icon,
                             text="Usado às {} Horário de Brasília | © {} {} .".format(datetime.now().strftime("%H:%M"),
                                                                                       self.bot.user.name,
                                                                                       datetime.now().strftime("%Y")))

            embed.add_field(name="📖**Exemplos:**", value="!document 37584937063 batata234 crid\n!documento 81709558075 gshBgjds123 boletim",
                            inline=False)
            embed.add_field(name="📜**Lista de documentos:**", value="historico, boletim, boa, crid, bolsista, cotista, regularmente_matriculado, declaracao_passe_livre.",
                            inline=False)
            embed.add_field(name="🔀**Outros Comandos**",
                            value="``!documento``", inline=False)

            msg = await ctx.send(embed=embed)
            await msg.add_reaction("❓")
            return

        if isinstance(error, commands.UserInputError):
            embed = discord.Embed(title="Comando !document:", colour=discord.Colour(0xff0000),
                                  description="Você baixa o documento de interesse.\n \n**Como"
                                  " usar: !document <Login> <Senha> <Tipo do Documento>**\n \n**"
                                  "Só funciona no privado**")

            embed.set_author(
                name="Opa! Um erro aconteceu. Você colocou um tipo de documento inválido.")
            embed.set_footer(icon_url=discord_utils.bot_icon,
                             text="Usado às {} Horário de Brasília | © {} {} .".format(datetime.now().strftime("%H:%M"),
                                                                                       self.bot.user.name,
                                                                                       datetime.now().strftime("%Y")))

            embed.add_field(name="📖**Exemplos:**", value="!document 37584937063 batata234 crid\n!documento 81709558075 gshBgjds123 boletim",
                            inline=False)
            embed.add_field(name="📜**Lista de documentos:**", value="historico, boletim, boa, crid, bolsista, cotista, regularmente_matriculado, declaracao_passe_livre.",
                            inline=False)
            embed.add_field(name="🔀**Outros Comandos**",
                            value="``!documento``", inline=False)

            msg = await ctx.send(embed=embed)
            await msg.add_reaction("❓")
            return

        if isinstance(error, commands.CheckFailure):
            embed = discord.Embed(title="Comando !document:", colour=discord.Colour(0xff0000),
                                  description="Você baixa o documento de interesse.\n \n**Como"
                                  " usar: !document <Login> <Senha> <Tipo do Documento>**\n \n**"
                                  "Só funciona no privado**")
            embed.set_author(
                name="Opa! Um erro aconteceu. Possívelmente você não tem foto, este documento ou o SIGA está fora do ar.")
            embed.set_footer(icon_url=discord_utils.bot_icon,
                             text="Usado às {} Horário de Brasília | © {} {} .".format(datetime.now().strftime("%H:%M"),
                                                                                       self.bot.user.name,
                                                                                       datetime.now().strftime("%Y")))
            embed.add_field(name="📖**Exemplos:**", value="!document 37584937063 batata234 crid\n!documento 81709558075 gshBgjds123 boletim",
                            inline=False)
            embed.add_field(name="📜**Lista de documentos:**", value="historico, boletim, boa, crid, bolsista, cotista, regularmente_matriculado, declaracao_passe_livre.",
                            inline=False)
            embed.add_field(name="🔀**Outros Comandos**",
                            value="``!documento``", inline=False)

            msg = await ctx.send(embed=embed)
            await msg.add_reaction("❓")


def setup(bot):
    bot.add_cog(SigaHandler(bot))
