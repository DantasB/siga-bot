import os

import PyPDF2


def create_directory(directory_name):
    """ Creates a directory with the name

    Args:
        directory_name (str): directory to be created
    """
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)


def is_valid_file_path(file_path):
    """ Check if the pdf path is valid

    Args:
        file_path (str): path where the pdf is located

    Returns:
        bool: returns true if the path is valid
    """
    if(file_path == ""):
        return False

    if is_not_pdf(file_path):
        return False

    return True


def is_not_pdf(path):
    """ Tries to open the pdf and check if it's valid or not

    Args:
        path (str): path where the pdf is located

    Returns:
        bool: returns True if the document is not a valid pdf
    """
    try:
        with open(path, "rb") as pdf:
            PyPDF2.PdfFileReader(pdf)
        return False
    except PyPDF2.utils.PdfReadError:
        return True


def save_document(html_content, path):
    """ writes the document bytes in the path

    Args:
        html_content (bytes): bytes of the pdf 
        path (str): path to save the pdf
    """
    with open(path, "wb") as f:
        f.write(html_content)


def delete_document(file_path):
    """ Deletes the document from the file_path

    Args:
        file_path (str): path where the pdf is located
    """
    os.remove(file_path)
