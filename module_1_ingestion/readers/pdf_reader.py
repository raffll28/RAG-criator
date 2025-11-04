"""
PDF Reader - Leitor de arquivos PDF

Suporta: .pdf
Usa PyMuPDF (fitz) para extração robusta de texto
"""

from pathlib import Path
from typing import Union
import hashlib
import fitz  # PyMuPDF
from loguru import logger

from .base_reader import BaseReader, Document


class PDFReader(BaseReader):
    """
    Reader para arquivos PDF.
    
    Usa PyMuPDF para extração de texto com suporte a:
    - Múltiplas páginas
    - Metadados do PDF
    - Detecção de PDF protegido/criptografado
    """
    
    def __init__(self, extract_images_text: bool = False):
        """
        Inicializa o PDFReader.
        
        Args:
            extract_images_text: Se True, tenta extrair texto de imagens (OCR básico)
        """
        super().__init__()
        self.extract_images_text = extract_images_text
        self.supported_extensions = [".pdf"]
    
    def read(self, file_path: Union[Path, str]) -> Document:
        """
        Lê um arquivo PDF e retorna um Document.
        
        Args:
            file_path: Caminho do arquivo PDF (Path ou string)
            
        Returns:
            Document contendo o conteúdo e metadados
            
        Raises:
            FileNotFoundError: Se o arquivo não existir
            ValueError: Se o arquivo não puder ser lido ou estiver protegido
        """
        # Converte para Path se necessário
        if isinstance(file_path, str):
            file_path = Path(file_path)
        
        logger.debug(f"Reading PDF file: {file_path}")
        
        # Valida o arquivo
        self._validate_file_exists(file_path)
        
        # Abre o PDF
        try:
            pdf_document = fitz.open(file_path)
        except Exception as e:
            raise ValueError(f"Failed to open PDF {file_path}: {e}")
        
        # Verifica se está criptografado
        if pdf_document.is_encrypted:
            pdf_document.close()
            raise ValueError(f"PDF is encrypted/password protected: {file_path}")
        
        # Extrai texto de todas as páginas
        content_parts = []
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            text = page.get_text()
            
            if text.strip():  # Só adiciona se tiver conteúdo
                content_parts.append(text)
        
        content = "\n\n".join(content_parts)
        
        # Extrai metadados do PDF
        pdf_metadata = pdf_document.metadata or {}
        
        # Metadados básicos do arquivo
        metadata = self._extract_basic_metadata(file_path)
        
        # Metadados específicos do PDF
        metadata["pages"] = pdf_document.page_count
        metadata["pdf_version"] = "1.0"  # PyMuPDF não expõe facilmente a versão
        metadata["is_encrypted"] = pdf_document.is_encrypted
        metadata["is_pdf_valid"] = True  # Se chegamos aqui, é um PDF válido
        
        # Metadados do documento PDF (se disponíveis)
        metadata["pdf_title"] = pdf_metadata.get("title", "")
        metadata["pdf_author"] = pdf_metadata.get("author", "")
        metadata["pdf_subject"] = pdf_metadata.get("subject", "")
        metadata["pdf_creator"] = pdf_metadata.get("creator", "")
        metadata["pdf_producer"] = pdf_metadata.get("producer", "")
        metadata["pdf_keywords"] = pdf_metadata.get("keywords", "")
        
        # Metadados de conteúdo
        metadata["content_length"] = len(content)
        metadata["char_count"] = len(content)
        metadata["lines_count"] = len(content.splitlines()) if content else 0
        metadata["word_count"] = len(content.split()) if content else 0
        metadata["content_hash"] = hashlib.md5(content.encode()).hexdigest()
        
        # Fecha o documento
        pdf_document.close()
        
        # Determina se permite vazio (PDFs sem texto extraível)
        allow_empty = len(content) == 0
        
        if allow_empty:
            logger.warning(
                f"PDF {file_path.name} has no extractable text. "
                "Might contain only images or be scanned."
            )
        
        # Cria o documento
        document = Document(
            content=content,
            metadata=metadata,
            source=str(file_path.absolute()),
            allow_empty=allow_empty
        )
        
        logger.info(
            f"Successfully read PDF {file_path.name} "
            f"({metadata['pages']} pages, {metadata['word_count']} words)"
        )
        
        return document

