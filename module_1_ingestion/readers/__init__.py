"""
Readers - Leitores de diferentes tipos de arquivo
"""

from .base_reader import BaseReader, Document
from .text_reader import TextReader

__all__ = [
    "BaseReader",
    "Document",
    "TextReader",
]

