"""
Text Reader - Leitor de arquivos de texto simples

Suporta: .txt, .md (markdown), .log, .csv
"""

from pathlib import Path
from typing import Optional, Union, List
import chardet
import hashlib
from loguru import logger

from .base_reader import BaseReader, Document


class TextReader(BaseReader):
    """
    Reader para arquivos de texto simples.
    
    Suporta detecção automática de encoding e múltiplos formatos de texto.
    """
    
    # Lista de encodings para fallback
    FALLBACK_ENCODINGS = ["latin-1", "cp1252", "iso-8859-1", "utf-16"]
    
    def __init__(
        self, 
        encoding: str = "utf-8", 
        auto_detect_encoding: bool = True,
        detection_sample_size: int = 10000
    ):
        """
        Inicializa o TextReader.
        
        Args:
            encoding: Codificação padrão (usado se auto_detect_encoding=False)
            auto_detect_encoding: Se True, tenta detectar encoding automaticamente
            detection_sample_size: Tamanho da amostra para detecção de encoding (bytes)
        """
        super().__init__(encoding)
        self.auto_detect_encoding = auto_detect_encoding
        self.detection_sample_size = detection_sample_size
        self.supported_extensions = [".txt", ".md", ".log", ".text"]
    
    def read(self, file_path: Union[Path, str]) -> Document:
        """
        Lê um arquivo de texto e retorna um Document.
        
        Args:
            file_path: Caminho do arquivo de texto (Path ou string)
            
        Returns:
            Document contendo o conteúdo e metadados
            
        Raises:
            FileNotFoundError: Se o arquivo não existir
            ValueError: Se o arquivo não puder ser lido
        """
        # Converte para Path se necessário
        if isinstance(file_path, str):
            file_path = Path(file_path)
        
        logger.debug(f"Reading text file: {file_path}")
        
        # Valida o arquivo
        self._validate_file_exists(file_path)
        
        # Detecta encoding se necessário
        encoding = self._detect_encoding(file_path) if self.auto_detect_encoding else self.encoding
        
        # Lê o conteúdo com fallback de encoding
        content, actual_encoding = self._read_with_fallback(file_path, encoding)
        
        # Extrai metadados
        metadata = self._extract_basic_metadata(file_path)
        metadata["encoding"] = actual_encoding
        metadata["content_length"] = len(content)
        metadata["char_count"] = len(content)
        metadata["lines_count"] = len(content.splitlines()) if content else 0
        metadata["word_count"] = len(content.split()) if content else 0
        metadata["content_hash"] = hashlib.md5(content.encode()).hexdigest()
        
        # Determina se permite vazio
        allow_empty = len(content) == 0
        
        # Cria e retorna o documento
        document = Document(
            content=content,
            metadata=metadata,
            source=str(file_path.absolute()),
            allow_empty=allow_empty
        )
        
        logger.info(f"Successfully read {file_path.name} ({metadata['lines_count']} lines, {actual_encoding})")
        
        return document
    
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
    
    def _read_with_fallback(self, file_path: Path, preferred_encoding: str) -> tuple[str, str]:
        """
        Lê o arquivo tentando múltiplos encodings se necessário.
        
        Args:
            file_path: Caminho do arquivo
            preferred_encoding: Encoding preferencial
            
        Returns:
            Tupla (conteúdo, encoding_usado)
        """
        # Tenta com encoding preferencial primeiro
        try:
            content = self._read_content(file_path, preferred_encoding)
            return content, preferred_encoding
        except UnicodeDecodeError as e:
            logger.warning(f"Failed to read {file_path.name} with {preferred_encoding}: {e}")
            
            # Tenta encodings de fallback
            for fallback_encoding in self.FALLBACK_ENCODINGS:
                try:
                    logger.debug(f"Trying fallback encoding: {fallback_encoding}")
                    content = self._read_content(file_path, fallback_encoding)
                    logger.info(f"Successfully read with fallback encoding: {fallback_encoding}")
                    return content, fallback_encoding
                except UnicodeDecodeError:
                    continue
            
            # Se todos falharem, levanta erro
            raise ValueError(
                f"Failed to read file {file_path} with any encoding. "
                f"Tried: {preferred_encoding}, {', '.join(self.FALLBACK_ENCODINGS)}"
            )
    
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
            raw_data = f.read(self.detection_sample_size)
        
        # Se arquivo estiver vazio, retorna encoding padrão
        if not raw_data:
            logger.debug(f"Empty file, using default encoding: {self.encoding}")
            return self.encoding
        
        # Detecta encoding
        result = chardet.detect(raw_data)
        detected_encoding = result.get('encoding', self.encoding)
        confidence = result.get('confidence', 0)
        
        logger.debug(
            f"Encoding detection: {detected_encoding} "
            f"(confidence: {confidence:.2f}) for {file_path.name}"
        )
        
        # Se a confiança for muito baixa, usa encoding padrão
        if confidence < 0.7:
            logger.warning(
                f"Low confidence ({confidence:.2f}) for encoding detection, "
                f"using default: {self.encoding}"
            )
            return self.encoding
        
        return detected_encoding or self.encoding

