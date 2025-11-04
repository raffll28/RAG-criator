"""
Testes para PDFReader
"""

import pytest
from pathlib import Path
import tempfile
import os
import time
import fitz  # PyMuPDF

from module_1_ingestion.readers import PDFReader, Document


class TestPDFReader:
    """Testes para a classe PDFReader."""
    
    def setup_method(self):
        """Setup executado antes de cada teste."""
        self.reader = PDFReader()
        self.temp_dir = tempfile.mkdtemp()
    
    def teardown_method(self):
        """Cleanup executado após cada teste."""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def _create_test_pdf(self, filename: str, content: str, pages: int = 1) -> Path:
        """
        Cria um PDF de teste.
        
        Args:
            filename: Nome do arquivo
            content: Conteúdo de texto
            pages: Número de páginas
            
        Returns:
            Path do arquivo criado
        """
        file_path = Path(self.temp_dir) / filename
        doc = fitz.open()  # Novo PDF
        
        for page_num in range(pages):
            page = doc.new_page()
            page.insert_text((50, 50), f"{content}\nPágina {page_num + 1}")
        
        doc.save(file_path)
        doc.close()
        time.sleep(0.1)  # Pequeno delay para Windows liberar o arquivo
        return file_path
    
    def test_reader_initialization(self):
        """Testa a inicialização do PDFReader."""
        reader = PDFReader()
        assert reader.extract_images_text is False
        assert ".pdf" in reader.supported_extensions
    
    def test_supports_pdf_files(self):
        """Testa se o reader identifica arquivos PDF."""
        assert self.reader.supports(Path("test.pdf"))
        assert not self.reader.supports(Path("test.txt"))
        assert not self.reader.supports(Path("test.docx"))
    
    def test_read_simple_pdf(self):
        """Testa leitura de PDF simples."""
        test_file = self._create_test_pdf("test.pdf", "Hello PDF World!")
        
        document = self.reader.read(test_file)
        
        assert isinstance(document, Document)
        assert "Hello PDF World" in document.content
        assert document.metadata["file_extension"] == ".pdf"
        assert document.metadata["pages"] == 1
        assert document.metadata["reader_type"] == "PDFReader"
    
    def test_read_multi_page_pdf(self):
        """Testa leitura de PDF com múltiplas páginas."""
        test_file = self._create_test_pdf("multipage.pdf", "Content", pages=3)
        
        document = self.reader.read(test_file)
        
        assert document.metadata["pages"] == 3
        assert document.content.count("Página") == 3
    
    def test_read_nonexistent_pdf(self):
        """Testa leitura de PDF que não existe."""
        test_file = Path(self.temp_dir) / "nonexistent.pdf"
        
        with pytest.raises(FileNotFoundError):
            self.reader.read(test_file)
    
    def test_pdf_metadata_extraction(self):
        """Testa extração de metadados do PDF."""
        test_file = self._create_test_pdf("metadata_test.pdf", "Test content")
        
        document = self.reader.read(test_file)
        metadata = document.metadata
        
        # Verifica campos obrigatórios
        required_fields = [
            "pages", "pdf_version", "is_encrypted", "is_pdf_valid",
            "word_count", "content_length", "content_hash"
        ]
        
        for field in required_fields:
            assert field in metadata, f"Missing metadata field: {field}"
        
        assert metadata["is_encrypted"] is False
        assert metadata["pages"] > 0
    
    def test_empty_pdf(self):
        """Testa leitura de PDF vazio (sem texto extraível)."""
        # Cria PDF sem texto
        test_file = Path(self.temp_dir) / "empty.pdf"
        doc = fitz.open()
        doc.new_page()  # Página vazia
        doc.save(test_file)
        doc.close()
        time.sleep(0.1)  # Pequeno delay para Windows liberar o arquivo
        
        document = self.reader.read(test_file)
        
        assert document.allow_empty is True
        assert document.metadata["is_empty"] is True
        assert document.metadata["pages"] == 1

