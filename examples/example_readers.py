"""
Exemplo de uso dos Readers do Módulo 1

Demonstra as diferentes formas de uso e funcionalidades disponíveis.
"""

import sys
from pathlib import Path

# Adiciona o diretório raiz ao path para imports funcionarem
sys.path.insert(0, str(Path(__file__).parent.parent))

from module_1_ingestion.readers import read_file, ReaderFactory, TextReader
import tempfile


def example_simple_usage():
    """Exemplo 1: Uso mais simples - função read_file()"""
    print("=" * 60)
    print("EXEMPLO 1: Uso Simples")
    print("=" * 60)
    
    # Criar arquivo de exemplo
    temp_dir = tempfile.mkdtemp()
    test_file = Path(temp_dir) / "example.txt"
    
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write("Este é um exemplo de arquivo.\nCom múltiplas linhas.\n")
    
    # Ler arquivo - forma mais simples
    doc = read_file(test_file)
    
    print(f"\nArquivo: {doc.metadata['file_name']}")
    print(f"Tamanho: {doc.metadata['file_size_kb']} KB")
    print(f"Linhas: {doc.metadata['lines_count']}")
    print(f"Palavras: {doc.metadata['word_count']}")
    print(f"Encoding: {doc.metadata['encoding']}")
    print(f"\nConteúdo:\n{doc.content}")
    print(f"\nPreview: {doc.get_preview(50)}")
    
    # Cleanup
    import shutil
    shutil.rmtree(temp_dir)


def example_factory_usage():
    """Exemplo 2: Usando Factory explicitamente"""
    print("\n" + "=" * 60)
    print("EXEMPLO 2: Usando Factory")
    print("=" * 60)
    
    factory = ReaderFactory()
    
    # Listar readers disponíveis
    print("\nReaders Disponíveis:")
    for reader_name, extensions in factory.list_readers().items():
        print(f"  {reader_name}: {', '.join(extensions)}")
    
    print(f"\nExtensões Suportadas: {factory.supported_extensions}")
    
    # Verificar suporte
    print(f"\nPode ler .txt? {factory.can_read('test.txt')}")
    print(f"Pode ler .pdf? {factory.can_read('test.pdf')}")
    
    # Criar e ler arquivo
    temp_dir = tempfile.mkdtemp()
    md_file = Path(temp_dir) / "example.md"
    
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write("# Título\n\nEste é um **markdown**.\n")
    
    doc = factory.read(md_file)
    print(f"\nReader usado: {doc.metadata['reader_type']}")
    print(f"Conteúdo:\n{doc.content}")
    
    # Cleanup
    import shutil
    shutil.rmtree(temp_dir)


def example_specific_reader():
    """Exemplo 3: Usando reader específico com configurações"""
    print("\n" + "=" * 60)
    print("EXEMPLO 3: Reader Específico Configurado")
    print("=" * 60)
    
    # Criar reader com configurações customizadas
    reader = TextReader(
        encoding="utf-8",
        auto_detect_encoding=True,
        detection_sample_size=5000  # Amostra menor para detecção
    )
    
    temp_dir = tempfile.mkdtemp()
    test_file = Path(temp_dir) / "config_example.txt"
    
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write("Texto com acentuação: café, açúcar, José\n")
        f.write("Caracteres especiais: © ® ™\n")
    
    doc = reader.read(test_file)
    
    print(f"\nConteúdo lido com sucesso:")
    print(doc.content)
    print(f"\nEncoding detectado: {doc.metadata['encoding']}")
    
    # Cleanup
    import shutil
    shutil.rmtree(temp_dir)


def example_document_features():
    """Exemplo 4: Funcionalidades do Document"""
    print("\n" + "=" * 60)
    print("EXEMPLO 4: Funcionalidades do Document")
    print("=" * 60)
    
    temp_dir = tempfile.mkdtemp()
    
    # Arquivo 1
    file1 = Path(temp_dir) / "doc1.txt"
    content = "Este é um documento de exemplo para demonstrar as funcionalidades."
    with open(file1, 'w', encoding='utf-8') as f:
        f.write(content)
    
    doc1 = read_file(file1)
    
    # Hash para deduplicação
    hash1 = doc1.get_content_hash()
    print(f"\nHash do documento: {hash1}")
    
    # Preview
    print(f"Preview (30 chars): {doc1.get_preview(30)}")
    
    # Arquivo 2 (conteúdo idêntico)
    file2 = Path(temp_dir) / "doc2.txt"
    with open(file2, 'w', encoding='utf-8') as f:
        f.write(content)
    
    doc2 = read_file(file2)
    hash2 = doc2.get_content_hash()
    
    print(f"\nDocumento 2 hash: {hash2}")
    print(f"Hashes sao iguais? {hash1 == hash2}")
    print("  => Util para detectar duplicatas!")
    
    # Arquivo vazio
    file3 = Path(temp_dir) / "empty.txt"
    file3.touch()
    
    doc3 = read_file(file3)
    print(f"\nArquivo vazio:")
    print(f"  is_empty: {doc3.metadata['is_empty']}")
    print(f"  allow_empty: {doc3.allow_empty}")
    print(f"  lines_count: {doc3.metadata['lines_count']}")
    
    # Cleanup
    import shutil
    shutil.rmtree(temp_dir)


def example_metadata_exploration():
    """Exemplo 5: Explorando metadados completos"""
    print("\n" + "=" * 60)
    print("EXEMPLO 5: Metadados Completos")
    print("=" * 60)
    
    temp_dir = tempfile.mkdtemp()
    test_file = Path(temp_dir) / "metadata_example.log"
    
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write("2024-11-04 10:00:00 INFO Application started\n")
        f.write("2024-11-04 10:00:01 DEBUG Loading configuration\n")
        f.write("2024-11-04 10:00:02 INFO Server listening on port 8000\n")
    
    doc = read_file(test_file)
    
    print("\nTodos os Metadados:")
    for key, value in sorted(doc.metadata.items()):
        print(f"  {key:20s}: {value}")
    
    # Cleanup
    import shutil
    shutil.rmtree(temp_dir)


def main():
    """Executa todos os exemplos"""
    print("\n")
    print("=" * 60)
    print(" " * 10 + "EXEMPLOS DE USO - READERS MODULO 1")
    print("=" * 60)
    
    example_simple_usage()
    example_factory_usage()
    example_specific_reader()
    example_document_features()
    example_metadata_exploration()
    
    print("\n" + "=" * 60)
    print("Exemplos concluidos com sucesso!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()

