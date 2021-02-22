import requests

from SharedLibrary import pdf_utils
from SharedLibrary import siga_utils

portal_uri = "https://gnosys.ufrj.br"


def access_siga(username, password):
    with requests.Session() as session:
        # Access CAS website
        cas_url = 'https://intranetauxiliar.ufrj.br/LoginUfrj/redireciona/?url_redir=https%3A%2F%2Fsiga.ufrj.br%2Fsira%2Fintranet%2FLoginIntranet.jsp%3FidentificacaoUFRJ%3D%3Aidentificacao_ufrj%3A%26idSessao%3D%3Aid_sessao%3A'
        login_page = session.get(cas_url)

        login = session.post(login_page.url, data=siga_utils.get_login_post_data(
            username, password, login_page))

        if(login.status_code == 500):
            print("foi")
            return None

        siga_response = session.get(portal_uri + "/Portal/auth.seam")

        return siga_response.cookies


def access_documents_page(cookies):
    with requests.Session() as session:
        # Set session cookies with the ones obtained in `login_to_siga`
        session.cookies = cookies
        # Go to the page just to wait for the redirect request
        session.get(portal_uri + "/Documentos")
        # Going here with the appropriate cookies return the desired page
        resp = session.get(portal_uri + "/Documentos/auth.seam")

        # We return the raw HTML of the page containing all the pdfs
        # Reverse engineering is needed to select specific pdfs (it uses js to lazy load)
        return resp.content.decode("utf-8")


def download_documents(cookies, doc_type, pdf_folder_path):
    with requests.Session() as session:
        # Set session cookies with the ones obtained in `login_to_siga`
        session.cookies = cookies

        document = session.post(portal_uri + "/Documentos/certidoes/emitir",
                                data=siga_utils.siga_document_post_data(
                                    session, doc_type),
                                allow_redirects=False)

        pdf_path = pdf_folder_path + doc_type + ".pdf"
        pdf_utils.save_document(session.get(
            document._next.url).content, pdf_path)


def get_document_from_siga(login, password, username, doc_type):

    directory_name = "Documents/" + username + "/"

    pdf_utils.create_directory(directory_name)

    cookies = access_siga(login, password)
    if(cookies is None):
        return ""

    access_documents_page(cookies)
    download_documents(cookies, doc_type, directory_name)

    return directory_name + '/' + doc_type + '.pdf'


get_document_from_siga("13429384702", "8778Bruno", "Bruno Dantas", "crid")
