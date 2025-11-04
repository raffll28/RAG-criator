"""
Testes para ReaderFactory
"""

import pytest
from pathlib import Path
import tempfile
import os

from module_1_ingestion.readers import (
    ReaderFactory, 
    get_factory, 
    read_file,
    TextReader,
    Document
)


class TestReaderFactory:
    """Testes para a classe ReaderFactory."""
    
    def setup_method(self):
        """Setup executado antes de cada teste."""
        self.factory = ReaderFactory()
        self.temp_dir = tempfile.mkdtemp()
    
    def teardown_method(self):
        """Cleanup executado após cada teste."""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_factory_initialization(self):
        """Testa inicialização da factory."""
        factory = ReaderFactory()
        assert factory is not None
        assert len(factory.supported_extensions) > 0
    
    def test_register_reader(self):
        """Testa registro de um reader."""
        factory = ReaderFactory()
        initial_count = len(factory.supported_extensions)
        
        # TextReader já está registrado por padrão
        assert ".txt" in factory.supported_extensions
        assert ".md" in factory.supported_extensions
    
    def test_get_reader(self):
        """Testa obtenção de reader apropriado."""
        reader = self.factory.get_reader("test.txt")
        assert reader is not None
        assert isinstance(reader, TextReader)
        
        reader = self.factory.get_reader(Path("test.md"))
        assert reader is not None
        assert isinstance(reader, TextReader)
    
    def test_get_reader_unsupported(self):
        """Testa obtenção de reader para tipo não suportado."""
        reader = self.factory.get_reader("test.pdf")
        assert reader is None
        
        reader = self.factory.get_reader("test.unknown")
        assert reader is None
    
    def test_can_read(self):
        """Testa verificação de suporte."""
        assert self.factory.can_read("test.txt") is True
        assert self.factory.can_read("test.md") is True
        assert self.factory.can_read("test.log") is True
        assert self.factory.can_read("test.pdf") is False
        assert self.factory.can_read("test.docx") is False
    
    def test_read_file_via_factory(self):
        """Testa leitura de arquivo através da factory."""
        test_file = Path(self.temp_dir) / "factory_test.txt"
        test_content = "Testing factory pattern"
        
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(test_content)
        
        document = self.factory.read(test_file)
        
        assert isinstance(document, Document)
        assert document.content == test_content
        assert document.metadata["reader_type"] == "TextReader"
    
    def test_read_unsupported_file(self):
        """Testa leitura de arquivo não suportado."""
        test_file = Path(self.temp_dir) / "test.pdf"
        test_file.touch()
        
        with pytest.raises(ValueError, match="No reader available"):
            self.factory.read(test_file)
    
    def test_supported_extensions(self):
        """Testa lista de extensões suportadas."""
        extensions = self.factory.supported_extensions
        assert isinstance(extensions, list)
        assert ".txt" in extensions
        assert ".md" in extensions
        assert len(extensions) > 0
        # Verifica se está ordenada
        assert extensions == sorted(extensions)
    
    def test_list_readers(self):
        """Testa listagem de readers registrados."""
        readers = self.factory.list_readers()
        assert isinstance(readers, dict)
        assert "TextReader" in readers
        assert ".txt" in readers["TextReader"]


class TestGlobalFactory:
    """Testes para funções globais da factory."""
    
    def test_get_factory_singleton(self):
        """Testa se get_factory retorna singleton."""
        factory1 = get_factory()
        factory2 = get_factory()
        
        # Deve ser a mesma instância
        assert factory1 is factory2
    
    def test_read_file_convenience_function(self):
        """Testa função de conveniência read_file."""
        temp_dir = tempfile.mkdtemp()
        try:
            test_file = Path(temp_dir) / "convenience_test.txt"
            test_content = "Testing convenience function"
            
            with open(test_file, 'w', encoding='utf-8') as f:
                f.write(test_content)
            
            document = read_file(test_file)
            
            assert isinstance(document, Document)
            assert document.content == test_content
        finally:
            import shutil
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)


class TestDocumentEnhancements:
    """Testes para melhorias na classe Document."""
    
    def test_document_hash(self):
        """Testa geração de hash do documento."""
        doc = Document(
            content="Test content",
            metadata={"test": "data"},
            source="test.txt",
            allow_empty=False
        )
        
        hash1 = doc.get_content_hash()
        assert isinstance(hash1, str)
        assert len(hash1) == 32  # MD5 hash length
        
        # Mesmo conteúdo deve gerar mesmo hash
        doc2 = Document(
            content="Test content",
            metadata={"different": "metadata"},
            source="different.txt",
            allow_empty=False
        )
        hash2 = doc2.get_content_hash()
        assert hash1 == hash2
        
        # Conteúdo diferente deve gerar hash diferente
        doc3 = Document(
            content="Different content",
            metadata={"test": "data"},
            source="test.txt",
            allow_empty=False
        )
        hash3 = doc3.get_content_hash()
        assert hash1 != hash3
    
    def test_document_preview(self):
        """Testa geração de preview do documento."""
        short_content = "Short content"
        doc1 = Document(
            content=short_content,
            metadata={},
            source="test.txt"
        )
        
        preview1 = doc1.get_preview(max_length=100)
        assert preview1 == short_content
        
        long_content = "A" * 300
        doc2 = Document(
            content=long_content,
            metadata={},
            source="test.txt"
        )
        
        preview2 = doc2.get_preview(max_length=50)
        assert len(preview2) == 53  # 50 + "..."
        assert preview2.endswith("...")
        assert preview2.startswith("AAA")
    
    def test_document_is_empty_metadata(self):
        """Testa flag is_empty nos metadados."""
        doc_empty = Document(
            content="",
            metadata={},
            source="empty.txt",
            allow_empty=True
        )
        assert doc_empty.metadata["is_empty"] is True
        
        doc_not_empty = Document(
            content="Content",
            metadata={},
            source="notempty.txt"
        )
        assert doc_not_empty.metadata["is_empty"] is False

