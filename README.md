# trabalho-bd-2

Repositório para análise e consulta de desastres naturais utilizando FastAPI, CouchDB e Docker.

## Estrutura de Diretórios

- `main.py` — Ponto de entrada da API FastAPI.
- `queries_router.py` — Rotas de consulta à base de dados.
- `deps.py` — Dependências e utilitários para injeção de dependências.
- `startup/` — Scripts de inicialização do banco de dados e carregamento de dados:
  - `db_initialization.py` — Inicialização e gerenciamento do container CouchDB via Docker.
  - `data_initialization.py` — Carregamento e inserção dos dados no banco.
- `data/` — Dados utilizados no projeto:
  - `emdat.xlsx` — Base de dados original.
  - `emdat_docs.pkl` — Cache dos documentos processados.
- `notebooks/` — Notebooks para processamento e análise de dados.
- `pyproject.toml` — Dependências do projeto.

## Dependências

- Python >= 3.12
- Docker (necessário para rodar o CouchDB via container)
- As dependências Python estão listadas em `pyproject.toml`:
  - couchdb
  - docker
  - fastapi[standard]
  - openpyxl
  - pandas
  - plotly
  - requests
  - yarl

## Como Executar

### 1. Usando `uv` (recomendado)

```bash
uv sync  # Instala as dependências
uv pip list  # Verifica dependências (opcional)
uv run fastapi dev  # Executa a aplicação em modo de desenvolvimento, com hot-reloading ativo
#ou
uv run fastapi run  # Executa a aplicação para deploy
```

### 2. Usando `pip`

```bash
python -m venv .venv
source .venv/bin/activate
pip install .  # Instala as dependências por meio do pyproject.toml
# ou
pip install couchdb docker fastapi[standard] openpyxl pandas plotly requests yarl  # Instala as dependências manualmente
python fastapi dev  # Executa a aplicação em modo de desenvolvimento, com hot-reloading ativo
# ou
python fastapi run  # Executa a aplicação para deploy
```

### 3. Pré-requisito: Docker

Certifique-se de que o Docker está instalado e em execução. O banco CouchDB será iniciado automaticamente pelo sistema ao rodar a aplicação.

## Observações
- Os dados são carregados automaticamente na primeira execução.
- As views do CouchDB são criadas via design document.
- A API estará disponível em `http://localhost:8000` (ou porta configurada).
- As rotas de consulta estão sob o prefixo `/queries`.
- A documentação gerada pelo FastAPI está disponível em `http://localhost:8000/docs`.
