"""
Readers - Leitores de diferentes tipos de arquivo

Usage:
    # Forma simples (recomendada)
    from module_1_ingestion.readers import read_file
    doc = read_file("data/sample.txt")
    
    # Usando factory explicitamente
    from module_1_ingestion.readers import ReaderFactory
    factory = ReaderFactory()
    doc = factory.read("data/sample.txt")
    
    # Usando reader específico
    from module_1_ingestion.readers import TextReader
    reader = TextReader()
    doc = reader.read("data/sample.txt")
"""

from .base_reader import BaseReader, Document
from .text_reader import TextReader
from .reader_factory import ReaderFactory, get_factory, read_file

__all__ = [
    "BaseReader",
    "Document",
    "TextReader",
    "ReaderFactory",
    "get_factory",
    "read_file",
]

