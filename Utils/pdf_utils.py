import os
import PyPDF2


def create_directory(directory_name):
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)


def is_valid_file_path(file_path):
    if(file_path == ""):
        return False

    if is_not_pdf(file_path):
        return False

    return True


def is_not_pdf(path):
    try:
        with open(path, "rb") as pdf:
            PyPDF2.PdfFileReader(pdf)
        return False
    except PyPDF2.utils.PdfReadError:
        return True


def save_document(html_content, path):
    with open(path, "wb") as f:
        f.write(html_content)


def delete_document(file_path):
    os.remove(file_path)
