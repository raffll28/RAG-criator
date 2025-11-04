# 📚 Documentação - RAG Facilitator

Bem-vindo à documentação completa do projeto RAG Facilitator!

## 📖 Índice de Documentação

### 🏗️ Arquitetura e Design

**[Design Patterns e Orientação a Objetos](DESIGN_PATTERNS.md)**
- Por que usar OO neste projeto
- Padrões de design implementados (Factory, Template Method, Registry, Singleton)
- Princípios SOLID aplicados
- Vantagens para extensibilidade e manutenção
- Exemplos práticos de extensão

### 🔧 Módulos

**[Módulo 1 - Ingestão de Dados](MODULE_1_INGESTION.md)**
- Visão geral do sistema de readers
- Como usar (forma simples, factory, reader específico)
- Metadados gerados
- Como adicionar novos readers
- Guia de testes
- Próximos readers planejados

### 📝 Changelog

**[Melhorias Implementadas](IMPROVEMENTS.md)**
- Resumo completo das melhorias recentes
- Bugs corrigidos
- Novas funcionalidades
- Estatísticas e métricas
- Design patterns aplicados
- Próximos passos

## 🚀 Guias Rápidos

### Para Usuários

1. **Começar a usar**:
   - Leia o [README principal](../README.md)
   - Veja os [exemplos práticos](../examples/example_readers.py)
   - Consulte [MODULE_1_INGESTION.md](MODULE_1_INGESTION.md) para detalhes

2. **Adicionar suporte a novo tipo de arquivo**:
   - Veja [Como adicionar novos readers](MODULE_1_INGESTION.md#-adicionando-novos-readers)
   - Exemplo completo em [DESIGN_PATTERNS.md](DESIGN_PATTERNS.md#-exemplo-de-extenso-futura)

### Para Desenvolvedores

1. **Entender a arquitetura**:
   - [DESIGN_PATTERNS.md](DESIGN_PATTERNS.md) - Conceitos fundamentais
   - [MODULE_1_INGESTION.md](MODULE_1_INGESTION.md) - Implementação prática

2. **Contribuir**:
   - Leia [IMPROVEMENTS.md](IMPROVEMENTS.md) para entender o estado atual
   - Siga os padrões estabelecidos em [DESIGN_PATTERNS.md](DESIGN_PATTERNS.md)
   - Execute os testes: `pytest tests/ -v`

## 📂 Estrutura da Documentação

```
docs/
├── README.md                    # Este arquivo (índice)
├── DESIGN_PATTERNS.md          # Arquitetura e padrões
├── MODULE_1_INGESTION.md       # Documentação do Módulo 1
└── IMPROVEMENTS.md             # Changelog detalhado
```

## 🔗 Links Úteis

- **Repositório**: [GitHub](https://github.com/raffll28/RAG-criator)
- **Exemplos**: [`examples/`](../examples/)
- **Testes**: [`tests/`](../tests/)
- **README Principal**: [README.md](../README.md)

## 📌 Convenções

### Commits
Seguimos [Conventional Commits](https://www.conventionalcommits.org/):
```
feat(scope): adiciona nova funcionalidade
fix(scope): corrige bug
refactor(scope): refatora código
docs(scope): atualiza documentação
test(scope): adiciona/modifica testes
```

### Código
- **Linguagem**: Código em inglês, comentários e docs em português
- **Style**: PEP8 para Python
- **Type hints**: Obrigatórios em funções públicas
- **Docstrings**: Google style

### Testes
- Cobertura mínima: 80%
- Testes unitários para cada classe
- Testes de integração para workflows completos

## 🆘 Precisa de Ajuda?

1. **Dúvidas sobre uso**: Consulte [MODULE_1_INGESTION.md](MODULE_1_INGESTION.md)
2. **Dúvidas sobre arquitetura**: Leia [DESIGN_PATTERNS.md](DESIGN_PATTERNS.md)
3. **Problemas/Bugs**: Abra uma issue no GitHub
4. **Sugestões**: Pull requests são bem-vindos!

---

**Última atualização**: 04/11/2025  
**Versão do projeto**: 0.1.0 (Módulo 1 em desenvolvimento)

