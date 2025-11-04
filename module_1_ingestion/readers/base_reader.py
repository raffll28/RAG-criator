"""
Base Reader - Classe abstrata para leitores de arquivos

Define a interface que todos os readers devem implementar.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Document:
    """
    Representa um documento processado.
    
    Attributes:
        content: Conteúdo do documento
        metadata: Metadados do documento (path, tipo, data, etc.)
        source: Caminho do arquivo fonte
    """
    content: str
    metadata: Dict[str, Any]
    source: str
    
    def __post_init__(self):
        """Valida e normaliza os dados após inicialização."""
        if not self.content:
            raise ValueError("Document content cannot be empty")
        
        if not self.source:
            raise ValueError("Document source cannot be empty")


class BaseReader(ABC):
    """
    Classe abstrata base para todos os readers.
    
    Cada reader deve implementar:
    - read(): Método para ler um arquivo específico
    - supports(): Verifica se o reader suporta um tipo de arquivo
    """
    
    def __init__(self, encoding: str = "utf-8"):
        """
        Inicializa o reader.
        
        Args:
            encoding: Codificação padrão para leitura de arquivos
        """
        self.encoding = encoding
        self.supported_extensions: List[str] = []
    
    @abstractmethod
    def read(self, file_path: Path) -> Document:
        """
        Lê um arquivo e retorna um Document.
        
        Args:
            file_path: Caminho do arquivo a ser lido
            
        Returns:
            Document contendo o conteúdo e metadados
            
        Raises:
            FileNotFoundError: Se o arquivo não existir
            ValueError: Se o arquivo não puder ser lido
        """
        pass
    
    def supports(self, file_path: Path) -> bool:
        """
        Verifica se este reader suporta o arquivo.
        
        Args:
            file_path: Caminho do arquivo
            
        Returns:
            True se o reader suporta o arquivo, False caso contrário
        """
        return file_path.suffix.lower() in self.supported_extensions
    
    def _extract_basic_metadata(self, file_path: Path) -> Dict[str, Any]:
        """
        Extrai metadados básicos do arquivo.
        
        Args:
            file_path: Caminho do arquivo
            
        Returns:
            Dicionário com metadados básicos
        """
        stat = file_path.stat()
        
        return {
            "file_name": file_path.name,
            "file_path": str(file_path.absolute()),
            "file_extension": file_path.suffix.lower(),
            "file_size_bytes": stat.st_size,
            "created_at": datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "modified_at": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "reader_type": self.__class__.__name__,
        }
    
    def _validate_file_exists(self, file_path: Path) -> None:
        """
        Valida se o arquivo existe e é acessível.
        
        Args:
            file_path: Caminho do arquivo
            
        Raises:
            FileNotFoundError: Se o arquivo não existir
            ValueError: Se o caminho não for um arquivo
        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if not file_path.is_file():
            raise ValueError(f"Path is not a file: {file_path}")

