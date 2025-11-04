# RAG Facilitator

Sistema modular para criação otimizada de RAGs (Retrieval-Augmented Generation) totalmente local e gratuito.

## 🎯 Objetivo

Facilitar a criação de sistemas RAG através de três módulos independentes:

1. **Módulo 1 - Ingestão de Dados**: Lê diretórios com diversos tipos de arquivos e estrutura os dados para banco vetorial
2. **Módulo 2 - Benchmark**: Testa diversos formatos de vetorização e otimiza a performance
3. **Módulo 3 - Criador RAG**: Implementa o RAG com os parâmetros otimizados

## 🛠️ Stack Tecnológico

- **Linguagem**: Python 3.10+
- **Banco Vetorial**: Qdrant
- **LLM**: Ollama (local)
- **Embeddings**: Sentence-Transformers (local)
- **Versionamento**: Git/GitHub

## 📁 Estrutura do Projeto

```
rag-facilitator/
├── module_1_ingestion/      # Ingestão e processamento de dados
│   ├── readers/             # Leitores por tipo de arquivo
│   ├── chunkers/            # Estratégias de chunking
│   └── processors/          # Limpeza e metadados
├── module_2_benchmark/      # Testes de performance
│   ├── embeddings/          # Benchmark de embeddings
│   ├── vector_stores/       # Benchmark de configurações
│   └── metrics/             # Métricas e relatórios
├── module_3_rag/            # Sistema RAG completo
│   ├── indexer/             # Indexação vetorial
│   ├── retriever/           # Sistema de busca
│   └── generator/           # Geração de respostas
├── shared/                  # Utilitários compartilhados
├── data/                    # Dados do projeto
├── config/                  # Arquivos de configuração
└── tests/                   # Testes automatizados
```

## 🚀 Setup Inicial

### Pré-requisitos

- Python 3.10 ou superior
- Git
- Docker (para Qdrant)
- Ollama instalado

### Instalação

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd rag-facilitator
```

2. Crie e ative o ambiente virtual:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/WSL2
python3 -m venv venv
source venv/bin/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Inicie o Qdrant:
```bash
docker-compose up -d
```

## 📝 Status do Desenvolvimento

- [x] Estrutura do projeto
- [ ] Módulo 1 - Ingestão
- [ ] Módulo 2 - Benchmark
- [ ] Módulo 3 - RAG

## 🤝 Contribuindo

Este é um projeto em desenvolvimento ativo. Contribuições são bem-vindas!

## 📄 Licença

A definir

## 📧 Contato

A definir

