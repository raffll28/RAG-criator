"""
CSV Reader - Leitor de arquivos CSV

Suporta: .csv, .tsv
Usa pandas para leitura estruturada e conversão para texto
"""

from pathlib import Path
from typing import Union, Optional
import hashlib
import csv
from loguru import logger

from .base_reader import BaseReader, Document


class CSVReader(BaseReader):
    """
    Reader para arquivos CSV/TSV.
    
    Oferece opções de formatação e conversão para texto legível.
    """
    
    def __init__(
        self, 
        delimiter: str = ",",
        encoding: str = "utf-8",
        auto_detect_delimiter: bool = True,
        max_preview_rows: int = 1000
    ):
        """
        Inicializa o CSVReader.
        
        Args:
            delimiter: Delimitador padrão (vírgula, tab, etc.)
            encoding: Encoding padrão
            auto_detect_delimiter: Se True, tenta detectar delimitador automaticamente
            max_preview_rows: Máximo de linhas para preview (evita arquivos muito grandes)
        """
        super().__init__(encoding)
        self.delimiter = delimiter
        self.auto_detect_delimiter = auto_detect_delimiter
        self.max_preview_rows = max_preview_rows
        self.supported_extensions = [".csv", ".tsv"]
    
    def read(self, file_path: Union[Path, str]) -> Document:
        """
        Lê um arquivo CSV e retorna um Document.
        
        Args:
            file_path: Caminho do arquivo CSV (Path ou string)
            
        Returns:
            Document contendo o conteúdo e metadados
            
        Raises:
            FileNotFoundError: Se o arquivo não existir
            ValueError: Se o arquivo não puder ser lido
        """
        # Converte para Path se necessário
        if isinstance(file_path, str):
            file_path = Path(file_path)
        
        logger.debug(f"Reading CSV file: {file_path}")
        
        # Valida o arquivo
        self._validate_file_exists(file_path)
        
        # Detecta delimitador se necessário
        delimiter = self._detect_delimiter(file_path) if self.auto_detect_delimiter else self.delimiter
        
        # Lê o CSV
        try:
            rows = self._read_csv_rows(file_path, delimiter)
        except Exception as e:
            raise ValueError(f"Failed to read CSV {file_path}: {e}")
        
        if not rows:
            content = ""
            row_count = 0
            column_count = 0
            headers = []
        else:
            # Primeira linha são os headers (se tiver)
            headers = rows[0] if rows else []
            row_count = len(rows)
            column_count = len(headers) if headers else 0
            
            # Formata o conteúdo como texto legível
            content = self._format_csv_as_text(rows, headers)
        
        # Metadados básicos do arquivo
        metadata = self._extract_basic_metadata(file_path)
        
        # Metadados específicos do CSV
        metadata["delimiter"] = delimiter
        metadata["encoding"] = self.encoding
        metadata["rows_count"] = row_count
        metadata["columns_count"] = column_count
        metadata["headers"] = headers
        metadata["is_tsv"] = file_path.suffix.lower() == ".tsv"
        
        # Metadados de conteúdo
        metadata["content_length"] = len(content)
        metadata["char_count"] = len(content)
        metadata["lines_count"] = len(content.splitlines()) if content else 0
        metadata["word_count"] = len(content.split()) if content else 0
        metadata["content_hash"] = hashlib.md5(content.encode()).hexdigest()
        
        # Determina se permite vazio
        allow_empty = len(content) == 0
        
        # Cria o documento
        document = Document(
            content=content,
            metadata=metadata,
            source=str(file_path.absolute()),
            allow_empty=allow_empty
        )
        
        logger.info(
            f"Successfully read CSV {file_path.name} "
            f"({row_count} rows, {column_count} columns)"
        )
        
        return document
    
    def _detect_delimiter(self, file_path: Path) -> str:
        """
        Detecta o delimitador do CSV automaticamente.
        
        Args:
            file_path: Caminho do arquivo
            
        Returns:
            Delimitador detectado
        """
        # Lê primeiras linhas para detecção
        try:
            with open(file_path, 'r', encoding=self.encoding, errors='replace') as f:
                sample = f.read(4096)  # Amostra de 4KB
            
            sniffer = csv.Sniffer()
            detected_delimiter = sniffer.sniff(sample).delimiter
            
            logger.debug(f"Detected CSV delimiter: '{detected_delimiter}'")
            return detected_delimiter
            
        except Exception as e:
            logger.warning(f"Could not detect delimiter: {e}. Using default: '{self.delimiter}'")
            return self.delimiter
    
    def _read_csv_rows(self, file_path: Path, delimiter: str) -> list:
        """
        Lê as linhas do CSV.
        
        Args:
            file_path: Caminho do arquivo
            delimiter: Delimitador a usar
            
        Returns:
            Lista de linhas (cada linha é uma lista de valores)
        """
        rows = []
        
        with open(file_path, 'r', encoding=self.encoding, errors='replace', newline='') as f:
            csv_reader = csv.reader(f, delimiter=delimiter)
            
            for i, row in enumerate(csv_reader):
                if i >= self.max_preview_rows:
                    logger.warning(f"Reached max preview rows ({self.max_preview_rows}). Truncating.")
                    break
                rows.append(row)
        
        return rows
    
    def _format_csv_as_text(self, rows: list, headers: list) -> str:
        """
        Formata CSV como texto legível.
        
        Args:
            rows: Linhas do CSV
            headers: Cabeçalhos
            
        Returns:
            Texto formatado
        """
        if not rows:
            return ""
        
        content_parts = []
        
        # Adiciona headers
        if headers:
            content_parts.append("# Headers")
            content_parts.append(", ".join(headers))
            content_parts.append("")
        
        # Adiciona dados (pulando header)
        content_parts.append("# Data")
        for i, row in enumerate(rows[1:] if headers else rows, 1):
            # Formata cada linha como "campo1: valor1 | campo2: valor2"
            if headers and len(row) == len(headers):
                formatted_row = " | ".join(f"{h}: {v}" for h, v in zip(headers, row))
            else:
                formatted_row = ", ".join(row)
            
            content_parts.append(f"Row {i}: {formatted_row}")
        
        return "\n".join(content_parts)

