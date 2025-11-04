"""
Testes para TextReader
"""

import pytest
from pathlib import Path
import tempfile
import os

from module_1_ingestion.readers import TextReader, Document


class TestTextReader:
    """Testes para a classe TextReader."""
    
    def setup_method(self):
        """Setup executado antes de cada teste."""
        self.reader = TextReader()
        self.temp_dir = tempfile.mkdtemp()
    
    def teardown_method(self):
        """Cleanup executado após cada teste."""
        # Remove arquivos temporários
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_reader_initialization(self):
        """Testa a inicialização do TextReader."""
        reader = TextReader()
        assert reader.encoding == "utf-8"
        assert reader.auto_detect_encoding is True
        assert ".txt" in reader.supported_extensions
        assert ".md" in reader.supported_extensions
    
    def test_supports_text_files(self):
        """Testa se o reader identifica arquivos suportados."""
        assert self.reader.supports(Path("test.txt"))
        assert self.reader.supports(Path("test.md"))
        assert self.reader.supports(Path("test.log"))
        assert not self.reader.supports(Path("test.pdf"))
        assert not self.reader.supports(Path("test.docx"))
    
    def test_read_simple_text_file(self):
        """Testa leitura de arquivo de texto simples."""
        # Cria arquivo de teste
        test_file = Path(self.temp_dir) / "test.txt"
        test_content = "Hello, World!\nThis is a test file.\nLine 3."
        
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(test_content)
        
        # Lê o arquivo
        document = self.reader.read(test_file)
        
        # Valida resultado
        assert isinstance(document, Document)
        assert document.content == test_content
        assert document.source == str(test_file.absolute())
        assert document.metadata["file_name"] == "test.txt"
        assert document.metadata["file_extension"] == ".txt"
        assert document.metadata["encoding"] in ["utf-8", "ascii"]
        assert document.metadata["lines_count"] == 3
        assert document.metadata["content_length"] == len(test_content)
    
    def test_read_empty_file(self):
        """Testa leitura de arquivo vazio."""
        test_file = Path(self.temp_dir) / "empty.txt"
        test_file.touch()
        
        # Deve lançar erro pois conteúdo está vazio
        with pytest.raises(ValueError, match="content cannot be empty"):
            self.reader.read(test_file)
    
    def test_read_nonexistent_file(self):
        """Testa leitura de arquivo que não existe."""
        test_file = Path(self.temp_dir) / "nonexistent.txt"
        
        with pytest.raises(FileNotFoundError):
            self.reader.read(test_file)
    
    def test_read_markdown_file(self):
        """Testa leitura de arquivo markdown."""
        test_file = Path(self.temp_dir) / "test.md"
        test_content = "# Title\n\nThis is **markdown**.\n\n- Item 1\n- Item 2"
        
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(test_content)
        
        document = self.reader.read(test_file)
        
        assert document.content == test_content
        assert document.metadata["file_extension"] == ".md"
    
    def test_read_with_special_characters(self):
        """Testa leitura de arquivo com caracteres especiais."""
        test_file = Path(self.temp_dir) / "special.txt"
        test_content = "Texto com acentuação: café, açúcar, José\nEmojis: 😊 🚀 🎉\nSímbolos: © ® ™"
        
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(test_content)
        
        document = self.reader.read(test_file)
        
        assert document.content == test_content
        assert "café" in document.content
        assert "😊" in document.content
    
    def test_metadata_extraction(self):
        """Testa extração de metadados."""
        test_file = Path(self.temp_dir) / "metadata_test.txt"
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write("Content for metadata test")
        
        document = self.reader.read(test_file)
        metadata = document.metadata
        
        # Verifica campos obrigatórios
        required_fields = [
            "file_name", "file_path", "file_extension",
            "file_size_bytes", "created_at", "modified_at",
            "reader_type", "encoding", "content_length", "lines_count"
        ]
        
        for field in required_fields:
            assert field in metadata, f"Missing metadata field: {field}"
        
        assert metadata["reader_type"] == "TextReader"
        assert metadata["file_size_bytes"] > 0

