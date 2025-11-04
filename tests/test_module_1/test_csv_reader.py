"""
Testes para CSVReader
"""

import pytest
from pathlib import Path
import tempfile
import os
import csv

from module_1_ingestion.readers import CSVReader, Document


class TestCSVReader:
    """Testes para a classe CSVReader."""
    
    def setup_method(self):
        """Setup executado antes de cada teste."""
        self.reader = CSVReader()
        self.temp_dir = tempfile.mkdtemp()
    
    def teardown_method(self):
        """Cleanup executado após cada teste."""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def _create_test_csv(self, filename: str, rows: list, delimiter: str = ",") -> Path:
        """
        Cria um CSV de teste.
        
        Args:
            filename: Nome do arquivo
            rows: Lista de linhas (cada linha é uma lista de valores)
            delimiter: Delimitador
            
        Returns:
            Path do arquivo criado
        """
        file_path = Path(self.temp_dir) / filename
        
        with open(file_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f, delimiter=delimiter)
            for row in rows:
                writer.writerow(row)
        
        return file_path
    
    def test_reader_initialization(self):
        """Testa a inicialização do CSVReader."""
        reader = CSVReader()
        assert reader.delimiter == ","
        assert reader.auto_detect_delimiter is True
        assert ".csv" in reader.supported_extensions
        assert ".tsv" in reader.supported_extensions
    
    def test_supports_csv_files(self):
        """Testa se o reader identifica arquivos CSV."""
        assert self.reader.supports(Path("test.csv"))
        assert self.reader.supports(Path("test.tsv"))
        assert not self.reader.supports(Path("test.txt"))
    
    def test_read_simple_csv(self):
        """Testa leitura de CSV simples."""
        rows = [
            ["Name", "Age", "City"],
            ["Alice", "30", "New York"],
            ["Bob", "25", "London"]
        ]
        test_file = self._create_test_csv("test.csv", rows)
        
        document = self.reader.read(test_file)
        
        assert isinstance(document, Document)
        assert "Name" in document.content
        assert "Alice" in document.content
        assert document.metadata["file_extension"] == ".csv"
        assert document.metadata["rows_count"] == 3
        assert document.metadata["columns_count"] == 3
        assert document.metadata["reader_type"] == "CSVReader"
    
    def test_read_tsv_file(self):
        """Testa leitura de arquivo TSV."""
        rows = [
            ["Column1", "Column2"],
            ["Value1", "Value2"]
        ]
        test_file = self._create_test_csv("test.tsv", rows, delimiter="\t")
        
        # Reader deve detectar tab como delimitador
        document = self.reader.read(test_file)
        
        assert document.metadata["is_tsv"] is True
        assert "Column1" in document.content
    
    def test_csv_with_custom_delimiter(self):
        """Testa CSV com delimitador customizado."""
        rows = [
            ["A", "B", "C"],
            ["1", "2", "3"]
        ]
        test_file = self._create_test_csv("custom.csv", rows, delimiter=";")
        
        # Auto-detect deve encontrar o delimitador
        document = self.reader.read(test_file)
        
        assert "A" in document.content
        assert document.metadata["delimiter"] == ";"
    
    def test_read_nonexistent_csv(self):
        """Testa leitura de CSV que não existe."""
        test_file = Path(self.temp_dir) / "nonexistent.csv"
        
        with pytest.raises(FileNotFoundError):
            self.reader.read(test_file)
    
    def test_csv_metadata_extraction(self):
        """Testa extração de metadados do CSV."""
        rows = [
            ["Header1", "Header2"],
            ["Data1", "Data2"]
        ]
        test_file = self._create_test_csv("metadata.csv", rows)
        
        document = self.reader.read(test_file)
        metadata = document.metadata
        
        # Verifica campos obrigatórios
        required_fields = [
            "rows_count", "columns_count", "headers", "delimiter",
            "word_count", "content_length", "content_hash"
        ]
        
        for field in required_fields:
            assert field in metadata, f"Missing metadata field: {field}"
        
        assert metadata["headers"] == ["Header1", "Header2"]
        assert metadata["rows_count"] == 2
    
    def test_empty_csv(self):
        """Testa leitura de CSV vazio."""
        test_file = self._create_test_csv("empty.csv", [])
        
        document = self.reader.read(test_file)
        
        assert document.allow_empty is True
        assert document.metadata["is_empty"] is True
        assert document.metadata["rows_count"] == 0
    
    def test_csv_no_autodetect(self):
        """Testa CSV sem auto-detecção de delimitador."""
        reader = CSVReader(auto_detect_delimiter=False, delimiter=",")
        rows = [["A", "B"], ["1", "2"]]
        test_file = self._create_test_csv("noauto.csv", rows)
        
        document = reader.read(test_file)
        
        assert document.metadata["delimiter"] == ","

