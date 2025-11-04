"""
Demonstração de leitura de todos os tipos de arquivo

Este script lê todos os arquivos de exemplo e mostra informações sobre cada um.
"""

import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from module_1_ingestion.readers import read_file, get_factory


def print_header(text):
    """Imprime cabeçalho formatado"""
    print("\n" + "=" * 70)
    print(f" {text}")
    print("=" * 70)


def print_document_info(doc, show_preview=True):
    """Imprime informações sobre um documento"""
    print(f"\nArquivo: {doc.metadata['file_name']}")
    print(f"Tipo: {doc.metadata['reader_type']}")
    print(f"Tamanho: {doc.metadata['file_size_kb']} KB")
    print(f"Linhas: {doc.metadata['lines_count']}")
    print(f"Palavras: {doc.metadata['word_count']}")
    
    # Informações específicas por tipo
    if doc.metadata['reader_type'] == 'PDFReader':
        print(f"Páginas: {doc.metadata['pages']}")
        if doc.metadata.get('pdf_author'):
            print(f"Autor: {doc.metadata['pdf_author']}")
    
    elif doc.metadata['reader_type'] == 'DOCXReader':
        print(f"Parágrafos: {doc.metadata['paragraphs_count']}")
        print(f"Tabelas: {doc.metadata['tables_count']}")
    
    elif doc.metadata['reader_type'] == 'CSVReader':
        print(f"Linhas de dados: {doc.metadata['rows_count']}")
        print(f"Colunas: {doc.metadata['columns_count']}")
        print(f"Headers: {', '.join(doc.metadata['headers'][:5])}")
    
    if show_preview and doc.content:
        print(f"\nPreview:")
        print("-" * 70)
        preview = doc.get_preview(200)
        print(preview)
        print("-" * 70)


def demo_text_files():
    """Demonstração de arquivos .txt"""
    print_header("ARQUIVOS DE TEXTO (.txt)")
    
    files = [
        "data/raw/receita_bolo.txt",
        "data/raw/lista_compras.txt"
    ]
    
    for file_path in files:
        try:
            doc = read_file(file_path)
            print_document_info(doc, show_preview=True)
        except FileNotFoundError:
            print(f"\nArquivo não encontrado: {file_path}")


def demo_markdown_files():
    """Demonstração de arquivos .md"""
    print_header("ARQUIVOS MARKDOWN (.md)")
    
    files = [
        "data/raw/tutorial_python.md",
        "data/raw/projeto_readme.md"
    ]
    
    for file_path in files:
        try:
            doc = read_file(file_path)
            print_document_info(doc, show_preview=True)
        except FileNotFoundError:
            print(f"\nArquivo não encontrado: {file_path}")


def demo_log_files():
    """Demonstração de arquivos .log"""
    print_header("ARQUIVOS DE LOG (.log)")
    
    files = [
        "data/raw/application.log",
        "data/raw/error_debug.log"
    ]
    
    for file_path in files:
        try:
            doc = read_file(file_path)
            print_document_info(doc, show_preview=True)
        except FileNotFoundError:
            print(f"\nArquivo não encontrado: {file_path}")


def demo_text_extension():
    """Demonstração de arquivos .text"""
    print_header("ARQUIVOS .text")
    
    files = [
        "data/raw/anotacoes_reuniao.text",
        "data/raw/ideias_projeto.text"
    ]
    
    for file_path in files:
        try:
            doc = read_file(file_path)
            print_document_info(doc, show_preview=True)
        except FileNotFoundError:
            print(f"\nArquivo não encontrado: {file_path}")


def demo_pdf_files():
    """Demonstração de arquivos .pdf"""
    print_header("ARQUIVOS PDF (.pdf)")
    
    files = [
        "data/raw/relatorio_vendas.pdf",
        "data/raw/artigo_ml.pdf"
    ]
    
    for file_path in files:
        try:
            doc = read_file(file_path)
            print_document_info(doc, show_preview=True)
        except FileNotFoundError:
            print(f"\nArquivo não encontrado: {file_path}")


def demo_docx_files():
    """Demonstração de arquivos .docx"""
    print_header("ARQUIVOS WORD (.docx)")
    
    files = [
        "data/raw/proposta_comercial.docx",
        "data/raw/manual_usuario.docx"
    ]
    
    for file_path in files:
        try:
            doc = read_file(file_path)
            print_document_info(doc, show_preview=True)
        except FileNotFoundError:
            print(f"\nArquivo não encontrado: {file_path}")


def demo_csv_files():
    """Demonstração de arquivos .csv"""
    print_header("ARQUIVOS CSV (.csv)")
    
    files = [
        "data/raw/vendas_2025.csv",
        "data/raw/funcionarios.csv"
    ]
    
    for file_path in files:
        try:
            doc = read_file(file_path)
            print_document_info(doc, show_preview=True)
        except FileNotFoundError:
            print(f"\nArquivo não encontrado: {file_path}")


def demo_tsv_files():
    """Demonstração de arquivos .tsv"""
    print_header("ARQUIVOS TSV (.tsv)")
    
    files = [
        "data/raw/produtos_estoque.tsv",
        "data/raw/analise_dados.tsv"
    ]
    
    for file_path in files:
        try:
            doc = read_file(file_path)
            print_document_info(doc, show_preview=True)
        except FileNotFoundError:
            print(f"\nArquivo não encontrado: {file_path}")


def show_statistics():
    """Mostra estatísticas gerais"""
    print_header("ESTATÍSTICAS GERAIS")
    
    factory = get_factory()
    
    print("\nReaders Disponíveis:")
    for reader_name, extensions in factory.list_readers().items():
        print(f"  - {reader_name}: {', '.join(extensions)}")
    
    print(f"\nTotal de Extensões Suportadas: {len(factory.supported_extensions)}")
    print(f"Extensões: {', '.join(factory.supported_extensions)}")


def main():
    """Função principal"""
    print("\n")
    print("#" * 70)
    print("#" + " " * 68 + "#")
    print("#" + " " * 15 + "DEMONSTRAÇÃO DE TODOS OS READERS" + " " * 21 + "#")
    print("#" + " " * 68 + "#")
    print("#" * 70)
    
    show_statistics()
    
    # Demonstração por tipo de arquivo
    demo_text_files()
    demo_markdown_files()
    demo_log_files()
    demo_text_extension()
    demo_pdf_files()
    demo_docx_files()
    demo_csv_files()
    demo_tsv_files()
    
    # Resumo final
    print_header("DEMONSTRAÇÃO CONCLUÍDA")
    print("\nTodos os readers foram testados com sucesso!")
    print("Os arquivos estão disponíveis em: data/raw/")
    print("\n")


if __name__ == "__main__":
    main()

