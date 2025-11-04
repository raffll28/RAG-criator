"""
Base Reader - Classe abstrata para leitores de arquivos

Define a interface que todos os readers devem implementar.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any, Optional, List, Union
from dataclasses import dataclass, field
from datetime import datetime
import hashlib


@dataclass
class Document:
    """
    Representa um documento processado.
    
    Attributes:
        content: Conteúdo do documento
        metadata: Metadados do documento (path, tipo, data, etc.)
        source: Caminho do arquivo fonte
        allow_empty: Se True, permite conteúdo vazio (para arquivos vazios válidos)
    """
    content: str
    metadata: Dict[str, Any]
    source: str
    allow_empty: bool = False
    
    def __post_init__(self):
        """Valida e normaliza os dados após inicialização."""
        if not self.content and not self.allow_empty:
            raise ValueError("Document content cannot be empty. Set allow_empty=True if intentional.")
        
        if not self.source:
            raise ValueError("Document source cannot be empty")
        
        # Adiciona flag de vazio nos metadados
        if "is_empty" not in self.metadata:
            self.metadata["is_empty"] = len(self.content) == 0
    
    def get_content_hash(self) -> str:
        """
        Gera hash MD5 do conteúdo para deduplicação.
        
        Returns:
            Hash MD5 do conteúdo
        """
        return hashlib.md5(self.content.encode()).hexdigest()
    
    def get_preview(self, max_length: int = 200) -> str:
        """
        Retorna preview do conteúdo.
        
        Args:
            max_length: Tamanho máximo do preview
            
        Returns:
            Preview do conteúdo
        """
        if len(self.content) <= max_length:
            return self.content
        return self.content[:max_length] + "..."


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
    def read(self, file_path: Union[Path, str]) -> Document:
        """
        Lê um arquivo e retorna um Document.
        
        Args:
            file_path: Caminho do arquivo a ser lido (Path ou string)
            
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
            "file_size_kb": round(stat.st_size / 1024, 2),
            "created_at": datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "modified_at": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "reader_type": self.__class__.__name__,
            "processed_at": datetime.now().isoformat(),
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

