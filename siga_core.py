import asyncio
import aiohttp
from SharedLibrary import pdf_utils
from SharedLibrary import siga_utils

portal_uri = "https://gnosys.ufrj.br"


async def access_siga(username, password):
    """ Access the siga main page throught the intranet

    Args:
        username (str): login (usually the cpf)
        password (str): password to access the siga

    Returns:
        cookie_jar: the request cookies
    """
    async with aiohttp.ClientSession(cookie_jar=aiohttp.CookieJar()) as session:
        # Access CAS website
        cas_url = 'https://intranetauxiliar.ufrj.br/LoginUfrj/redireciona/?url_redir=https%3A%2F%2Fsiga.ufrj.br%2Fsira%2Fintranet%2FLoginIntranet.jsp%3FidentificacaoUFRJ%3D%3Aidentificacao_ufrj%3A%26idSessao%3D%3Aid_sessao%3A'
        login_page = await session.get(cas_url)
        login_page_content = await login_page.read()
        login = await session.post(login_page.url, data=siga_utils.get_login_post_data(
            username, password, login_page_content.decode("utf-8")))

        siga_response = await session.get(portal_uri + "/Portal/auth.seam")
        return session.cookie_jar


async def access_documents_page(cookies):
    """ Access the siga documents page

    Args:
        cookies (cookie_jar): the request cookies

    Returns:
        str: decoded html content
    """
    async with aiohttp.ClientSession(cookie_jar=cookies) as session:
        await session.get(portal_uri + "/Documentos")
        resp = await session.get(portal_uri + "/Documentos/auth.seam")

        resp_content = await resp.read()
        return resp_content.decode("utf-8")


async def download_documents(cookies, doc_type, pdf_folder_path):
    """ Download the wanted document by making a post

    Args:
        cookies (cookie_jar): the request cookies
        doc_type (str): document to be downloaded in the page
        pdf_folder_path (str): path where the pdf will be saved
    """
    async with aiohttp.ClientSession(cookie_jar=cookies) as session:
        document = await session.post(portal_uri + "/Documentos/certidoes/emitir",
                                      data=siga_utils.siga_document_post_data(
                                          doc_type))
        content = await document.read()
        pdf_path = pdf_folder_path + "/" + doc_type + ".pdf"
        pdf_utils.save_document(content, pdf_path)


async def get_document_from_siga(login, password, username, doc_type):
    """ A wrapper that acces every pages, download the pdf and returns the path where it's located

    Args:
        login (str): login (usually the cpf)
        password (str): password to access the siga
        username (str): discord person username
        doc_type (str): document to be downloaded in the page

    Returns:
        str: path where the pdf is located
    """
    directory_name = "Documents/" + username

    pdf_utils.create_directory(directory_name)

    cookies = await access_siga(login, password)
    await access_documents_page(cookies)
    await download_documents(cookies, doc_type, directory_name)

    return directory_name + "/" + doc_type + '.pdf'

