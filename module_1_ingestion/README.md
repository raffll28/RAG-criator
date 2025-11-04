# Módulo 1 - Ingestão de Dados

Sistema modular e extensível para leitura de arquivos diversos.

## 🎯 Objetivo

Ler arquivos de diferentes formatos e converter em documentos estruturados para processamento posterior (chunking e vetorização).

## 📚 Características

### ✅ Implementado

- **TextReader**: Arquivos de texto (`.txt`, `.md`, `.log`, `.csv`)
  - Detecção automática de encoding
  - Fallback inteligente para múltiplos encodings
  - Suporte a arquivos vazios
  - Metadados ricos (hash, contadores, timestamps)
  
- **Factory Pattern**: Seleção automática de reader
  - Registro dinâmico de novos readers
  - Interface simples e conveniente
  - Extensível sem modificar código existente

- **Sistema de Logging**: Rastreamento completo
  - Logs de debug, info e warning
  - Detecção de encoding
  - Fallback de encodings

## 🚀 Uso

### Forma Simples (Recomendada)

```python
from module_1_ingestion.readers import read_file

# Lê qualquer arquivo suportado automaticamente
document = read_file("data/sample.txt")

print(f"Conteúdo: {document.content}")
print(f"Linhas: {document.metadata['lines_count']}")
print(f"Palavras: {document.metadata['word_count']}")
print(f"Encoding: {document.metadata['encoding']}")
```

### Usando Factory Explicitamente

```python
from module_1_ingestion.readers import ReaderFactory

factory = ReaderFactory()

# Verifica se pode ler
if factory.can_read("data/document.md"):
    doc = factory.read("data/document.md")

# Lista readers disponíveis
print(factory.list_readers())
# {'TextReader': ['.csv', '.log', '.md', '.text', '.txt']}
```

### Usando Reader Específico

```python
from module_1_ingestion.readers import TextReader

reader = TextReader(
    encoding="utf-8",
    auto_detect_encoding=True,
    detection_sample_size=10000
)

document = reader.read("data/file.txt")
```

### Trabalhando com Document

```python
from module_1_ingestion.readers import read_file

doc = read_file("data/article.md")

# Preview do conteúdo
print(doc.get_preview(max_length=100))

# Hash para deduplicação
print(f"Hash: {doc.get_content_hash()}")

# Metadados completos
print(f"Tamanho: {doc.metadata['file_size_kb']} KB")
print(f"Criado em: {doc.metadata['created_at']}")
print(f"Processado em: {doc.metadata['processed_at']}")
print(f"Vazio: {doc.metadata['is_empty']}")
```

## 🔧 Adicionando Novos Readers

### 1. Criar Nova Classe Reader

```python
from module_1_ingestion.readers.base_reader import BaseReader, Document
from pathlib import Path
from typing import Union

class PDFReader(BaseReader):
    def __init__(self):
        super().__init__()
        self.supported_extensions = [".pdf"]
    
    def read(self, file_path: Union[Path, str]) -> Document:
        if isinstance(file_path, str):
            file_path = Path(file_path)
        
        self._validate_file_exists(file_path)
        
        # Sua lógica de extração de PDF
        content = extract_pdf_content(file_path)
        
        metadata = self._extract_basic_metadata(file_path)
        metadata["pages"] = count_pages(file_path)
        
        return Document(
            content=content,
            metadata=metadata,
            source=str(file_path.absolute())
        )
```

### 2. Registrar na Factory

```python
from module_1_ingestion.readers import get_factory
from my_readers import PDFReader

factory = get_factory()
factory.register_reader(PDFReader)

# Agora pode usar automaticamente
doc = factory.read("document.pdf")
```

## 📊 Metadados Gerados

Todos os documentos incluem:

| Campo | Descrição |
|-------|-----------|
| `file_name` | Nome do arquivo |
| `file_path` | Caminho absoluto |
| `file_extension` | Extensão |
| `file_size_bytes` | Tamanho em bytes |
| `file_size_kb` | Tamanho em KB |
| `created_at` | Data de criação (ISO) |
| `modified_at` | Data de modificação (ISO) |
| `processed_at` | Data de processamento (ISO) |
| `reader_type` | Nome do reader usado |
| `encoding` | Encoding usado (TextReader) |
| `content_length` | Tamanho do conteúdo |
| `char_count` | Contagem de caracteres |
| `lines_count` | Contagem de linhas |
| `word_count` | Contagem de palavras |
| `content_hash` | Hash MD5 do conteúdo |
| `is_empty` | Se o arquivo está vazio |

## 🧪 Testes

```bash
# Executar todos os testes
pytest tests/test_module_1/ -v

# Com cobertura
pytest tests/test_module_1/ --cov=module_1_ingestion --cov-report=html
```

## 🔜 Próximos Readers

- **PDFReader**: Documentos PDF
- **DOCXReader**: Documentos Word
- **CodeReader**: Arquivos de código-fonte
- **JSONReader**: Arquivos JSON estruturados
- **ImageReader**: Extração de texto de imagens (OCR)

## 🎨 Padrões de Design Utilizados

### Factory Pattern
- **Problema**: Criar objetos sem especificar classe exata
- **Solução**: `ReaderFactory` seleciona reader automaticamente
- **Vantagem**: Adicionar novos readers sem modificar código cliente

### Template Method
- **Problema**: Algoritmo comum com passos específicos
- **Solução**: `BaseReader` define estrutura, subclasses implementam detalhes
- **Vantagem**: Reuso de código, consistência

### Registry Pattern
- **Problema**: Descobrir readers disponíveis dinamicamente
- **Solução**: Factory mantém registro de readers por extensão
- **Vantagem**: Extensibilidade, descoberta automática

