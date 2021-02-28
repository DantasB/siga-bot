from bs4 import BeautifulSoup
from validate_docbr import CPF

list_of_documents = {'historico': {'botaoHistorico': 'botaoHistorico'},
                     'boletim': {'botaoBoletim': 'botaoBoletim'},
                     'boa': {'j_id123': 'j_id123'}, 'crid': {'j_id127': 'j_id127'},
                     'regularmente_matriculado': {'j_id103:0:j_id104': 'j_id103:0:j_id104'},
                     'bolsista': {'j_id103:2:j_id104': 'j_id103:2:j_id104'},
                     'cotista': {'j_id103:3:j_id104': 'j_id103:3:j_id104'},
                     'declaracao_passe_livre': {'j_id103:4:j_id104': 'j_id103:4:j_id104'}}


def get_enrolled_page_token(html_content):
    """ Get the page token

    Args:
        html_content (str): the page html

    Returns:
        str: page token
    """
    soup = BeautifulSoup(html_content, "html.parser")
    # We need a token to get the raw json enrollment data
    return soup.find("span", {"id": "token"}).text


def get_login_post_data(username, password, html_content):
    """ Generate the post data to be used on login

    Args:
        username (str): login (usually the cpf)
        password (str): password to access the siga
        html_content (str): the page html
    Returns:
        dictionary: post data
    """
    postData = {'authenticity_token': get_authenticity_token_parameter(html_content),
                'lt': get_lt_parameter(html_content),
                'username': username,
                'password': password}

    return postData


def get_authenticity_token_parameter(html_content):
    """ Get the authenticity token

    Args:
        html_content (str): the page html

    Returns:
        str: authenticity token
    """
    soup = BeautifulSoup(html_content, "html.parser")
    return soup.find("input", {"name": "authenticity_token"})["value"]


def get_lt_parameter(html_content):
    """ Get the lt parameter

    Args:
        html_content (str): the page html

    Returns:
        str: lt parameter
    """
    soup = BeautifulSoup(html_content, "html.parser")
    return soup.find("input", {"id": "lt"})["value"]


def siga_document_post_data(doc_type):
    """ Generate the post data to be used on pdf download

    Args:
        doc_type (str): document to be downloaded in the page
    Returns:
        dictionary: post data
    """
    return {
        "gnosys-decor-vis-seletor-matricula-aluno": "0",
        "gnosys-decor-vis-seletor-matricula-form": "gnosys-decor-vis-seletor-matricula-form",
        "autoScroll": "",
        "javax.faces.ViewState": "j_id1"
    } | list_of_documents[doc_type]


def treat_login(login):
    """ Checks if the login is a valid cpf

    Args:
        login (str): siga login

    Returns:
        str: cpf digits
    """
    if(not CPF().validate(login)):
        return ""
    return login.replace(".", "").replace("-", "")
