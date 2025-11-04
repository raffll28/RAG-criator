"""
Reader Factory - Factory Pattern para seleção automática de readers

Facilita a adição de novos tipos de arquivo sem modificar código existente.
"""

from pathlib import Path
from typing import Union, List, Dict, Type, Optional
from loguru import logger

from .base_reader import BaseReader, Document
from .text_reader import TextReader
from .pdf_reader import PDFReader
from .docx_reader import DOCXReader
from .csv_reader import CSVReader


class ReaderFactory:
    """
    Factory para criar readers automaticamente baseado no tipo de arquivo.
    
    Implementa o padrão Factory + Registry para facilitar extensibilidade.
    """
    
    def __init__(self):
        """Inicializa a factory com readers padrão."""
        self._readers: Dict[str, Type[BaseReader]] = {}
        self._reader_instances: Dict[str, BaseReader] = {}
        
        # Registra readers padrão
        self.register_reader(TextReader)
        self.register_reader(PDFReader)
        self.register_reader(DOCXReader)
        self.register_reader(CSVReader)
    
    def register_reader(self, reader_class: Type[BaseReader]) -> None:
        """
        Registra um novo reader na factory.
        
        Args:
            reader_class: Classe do reader (não instância)
            
        Example:
            factory = ReaderFactory()
            factory.register_reader(PDFReader)
        """
        # Cria instância do reader
        reader_instance = reader_class()
        
        # Registra para cada extensão suportada
        for ext in reader_instance.supported_extensions:
            self._readers[ext] = reader_class
            self._reader_instances[ext] = reader_instance
            logger.debug(f"Registered {reader_class.__name__} for extension: {ext}")
    
    def get_reader(self, file_path: Union[Path, str]) -> Optional[BaseReader]:
        """
        Retorna o reader apropriado para o arquivo.
        
        Args:
            file_path: Caminho do arquivo
            
        Returns:
            Instância do reader ou None se não houver suporte
        """
        if isinstance(file_path, str):
            file_path = Path(file_path)
        
        extension = file_path.suffix.lower()
        
        if extension in self._reader_instances:
            logger.debug(f"Found reader for {extension}: {self._reader_instances[extension].__class__.__name__}")
            return self._reader_instances[extension]
        
        logger.warning(f"No reader found for extension: {extension}")
        return None
    
    def can_read(self, file_path: Union[Path, str]) -> bool:
        """
        Verifica se existe um reader para o arquivo.
        
        Args:
            file_path: Caminho do arquivo
            
        Returns:
            True se houver suporte, False caso contrário
        """
        if isinstance(file_path, str):
            file_path = Path(file_path)
        
        return file_path.suffix.lower() in self._readers
    
    def read(self, file_path: Union[Path, str]) -> Document:
        """
        Lê um arquivo usando o reader apropriado automaticamente.
        
        Args:
            file_path: Caminho do arquivo
            
        Returns:
            Document processado
            
        Raises:
            ValueError: Se não houver reader para o tipo de arquivo
            FileNotFoundError: Se o arquivo não existir
        """
        reader = self.get_reader(file_path)
        
        if reader is None:
            if isinstance(file_path, str):
                file_path = Path(file_path)
            raise ValueError(
                f"No reader available for file type: {file_path.suffix}. "
                f"Supported extensions: {self.supported_extensions}"
            )
        
        return reader.read(file_path)
    
    @property
    def supported_extensions(self) -> List[str]:
        """
        Retorna lista de extensões suportadas.
        
        Returns:
            Lista de extensões
        """
        return sorted(self._readers.keys())
    
    def list_readers(self) -> Dict[str, List[str]]:
        """
        Lista todos os readers registrados e suas extensões.
        
        Returns:
            Dicionário {nome_reader: [extensões]}
        """
        result = {}
        for ext, reader in self._reader_instances.items():
            reader_name = reader.__class__.__name__
            if reader_name not in result:
                result[reader_name] = []
            if ext not in result[reader_name]:
                result[reader_name].append(ext)
        
        return result


# Singleton global para facilitar uso
_global_factory = None


def get_factory() -> ReaderFactory:
    """
    Retorna instância global da factory (Singleton).
    
    Returns:
        ReaderFactory global
    """
    global _global_factory
    if _global_factory is None:
        _global_factory = ReaderFactory()
    return _global_factory


def read_file(file_path: Union[Path, str]) -> Document:
    """
    Função de conveniência para ler um arquivo.
    
    Args:
        file_path: Caminho do arquivo
        
    Returns:
        Document processado
        
    Example:
        from module_1_ingestion.readers import read_file
        
        doc = read_file("data/sample.txt")
        print(doc.content)
    """
    factory = get_factory()
    return factory.read(file_path)

