from difflib import SequenceMatcher

list_of_documents = ['historico', 'boletim', 'boa', 'crid',
                     'regularmente_matriculado', 'bolsista', 'cotista', 'declaracao_passe_livre']

bot_icon = "https://cdn.discordapp.com/attachments/539836343094870016/813096168799207454/minerva.png"


def is_dm(ctx, dm_channel):
    """ Checks if the user is sending a message on dm

    Args:
        ctx (object): object related to the user
        dm_channel (object): object that refers to dm

    Returns:
        bool: true if the user send message on dm
    """
    if isinstance(ctx.channel, dm_channel):
        return True

    return False


def is_valid_document(doc_type):
    """ Checks if the doc_type parameter is valid

    Args:
        doc_type (str): document type to be downloaded

    Returns:
        bool: True if it's valid
    """
    if doc_type.lower() not in list_of_documents:
        return False
    return True


def similar(a, b):
    """ Checks how similar is a str from another

    Args:
        a (str): first string to be compared
        b (str): second string to be compared

    Returns:
        float: ratio in how similar are the strings
    """
    return SequenceMatcher(None, a, b).ratio()
