from .common import process_file
from langchain.document_loaders import PyPDFLoader
from sqlite3 import Connection


def process_pdf(file, stats_db):
    return process_file(file, PyPDFLoader, ".pdf", stats_db=stats_db)
