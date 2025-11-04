"""
Text Reader - Leitor de arquivos de texto simples

Suporta: .txt, .md (markdown), .log, .csv
"""

from pathlib import Path
from typing import Optional
import chardet

from .base_reader import BaseReader, Document


class TextReader(BaseReader):
    """
    Reader para arquivos de texto simples.
    
    Suporta detecção automática de encoding e múltiplos formatos de texto.
    """
    
    def __init__(self, encoding: str = "utf-8", auto_detect_encoding: bool = True):
        """
        Inicializa o TextReader.
        
        Args:
            encoding: Codificação padrão (usado se auto_detect_encoding=False)
            auto_detect_encoding: Se True, tenta detectar encoding automaticamente
        """
        super().__init__(encoding)
        self.auto_detect_encoding = auto_detect_encoding
        self.supported_extensions = [".txt", ".md", ".log", ".csv", ".text"]
    
    def read(self, file_path: Path) -> Document:
        """
        Lê um arquivo de texto e retorna um Document.
        
        Args:
            file_path: Caminho do arquivo de texto
            
        Returns:
            Document contendo o conteúdo e metadados
            
        Raises:
            FileNotFoundError: Se o arquivo não existir
            ValueError: Se o arquivo não puder ser lido
        """
        # Converte para Path se necessário
        if isinstance(file_path, str):
            file_path = Path(file_path)
        
        # Valida o arquivo
        self._validate_file_exists(file_path)
        
        # Detecta encoding se necessário
        encoding = self._detect_encoding(file_path) if self.auto_detect_encoding else self.encoding
        
        # Lê o conteúdo
        try:
            content = self._read_content(file_path, encoding)
        except UnicodeDecodeError as e:
            # Tenta com encoding alternativo se falhar
            encoding = "latin-1"
            try:
                content = self._read_content(file_path, encoding)
            except Exception as fallback_error:
                raise ValueError(
                    f"Failed to read file {file_path} with encoding {encoding}: {fallback_error}"
                ) from e
        
        # Extrai metadados
        metadata = self._extract_basic_metadata(file_path)
        metadata["encoding"] = encoding
        metadata["content_length"] = len(content)
        metadata["lines_count"] = content.count('\n') + 1
        
        # Cria e retorna o documento
        return Document(
            content=content,
            metadata=metadata,
            source=str(file_path.absolute())
        )
    
    def _read_content(self, file_path: Path, encoding: str) -> str:
        """
        Lê o conteúdo do arquivo com o encoding especificado.
        
        Args:
            file_path: Caminho do arquivo
            encoding: Encoding a ser usado
            
        Returns:
            Conteúdo do arquivo como string
        """
        with open(file_path, 'r', encoding=encoding, errors='replace') as f:
            return f.read()
    
    def _detect_encoding(self, file_path: Path) -> str:
        """
        Detecta o encoding do arquivo automaticamente.
        
        Args:
            file_path: Caminho do arquivo
            
        Returns:
            Nome do encoding detectado
        """
        # Lê os primeiros bytes para detectar encoding
        with open(file_path, 'rb') as f:
            raw_data = f.read(10000)  # Lê até 10KB para detecção
        
        # Detecta encoding
        result = chardet.detect(raw_data)
        detected_encoding = result.get('encoding', self.encoding)
        confidence = result.get('confidence', 0)
        
        # Se a confiança for muito baixa, usa encoding padrão
        if confidence < 0.7:
            return self.encoding
        
        return detected_encoding or self.encoding

