from difflib import SequenceMatcher

list_of_documents = ['historico', 'boletim', 'boa', 'crid',
                     'regularmente_matriculado', 'bolsista', 'cotista', 'declaracao_passe_livre']

bot_icon = "https://cdn.discordapp.com/attachments/539836343094870016/813096168799207454/minerva.png"


def is_dm(ctx, dm_channel):
    if isinstance(ctx.channel, dm_channel):
        return True

    return False


def is_valid_document(doc_type):
    if doc_type.lower() not in list_of_documents:
        return False
    return True


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()
