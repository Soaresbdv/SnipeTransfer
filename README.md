# 🧾 Snipe-IT Inventory Manager

Sistema modularizado em Python para gerenciamento de inventário via Snipe-IT. Este projeto permite:

- ✅ Transferir ativos para usuários automaticamente via um arquivo `.csv`.
- 🔍 Auditar duplicidades de ativos (headset, monitor, webcam) atribuídos a um mesmo usuário.
- 🪵 Gerar logs detalhados de cada operação realizada.
- 📊 Exportar relatórios em `.csv` com os usuários que possuem ativos duplicados.

---

## 📁 Estrutura do Projeto

```
snipeit_inventory/
├── .env                         # Variáveis de ambiente com URL e token da API
├── transferencias.csv           # Arquivo de entrada para transferências
├── usuarios_com_ativos_duplicados.csv  # Gerado pela auditoria
├── logs/
│   └── log_transferencias_<timestamp>.txt  # Logs das execuções
├── requirements.txt             # Dependências Python
├── README.md                    # Documentação
└── src/
    ├── __init__.py
    ├── assign.py                # Transferência de ativos a partir do CSV
    ├── audit.py                 # Auditoria de ativos duplicados
    └── api.py                   # Módulo de comunicação com a API do Snipe-IT
```

---

## ⚙️ Requisitos

- Python 3.8+
- Conta de API ativa no Snipe-IT com permissões adequadas
- Biblioteca `requests` e `python-dotenv`

---

## 📦 Instalação

```bash
# Clone o repositório
git clone https://github.com/Soaresbdv/SnipeTransfer.git
cd SnipeTransfer

# Crie o arquivo de ambiente
cp .env

# Edite o .env com suas configurações
# SNIPEIT_URL=https://seudominio.snipeitapp.com
# SNIPEIT_TOKEN=seu_token_api

# Instale as dependências
pip install -r requirements.txt
```

---

## 📐 Exemplo de `.env`

```ini
SNIPEIT_URL=https://inventario.setuptecnologia.com.br
SNIPEIT_TOKEN=snipeit_token_aqui
```

---

## ✅ Transferência de Ativos

### Formato do `transferencias.csv`

```csv
username,asset_tag
nome.sobremome.silva,ST99999
```

### Executar:

```bash
python -m src.assign
```

- O script vai:
  - Ler o CSV
  - Atribuir os ativos aos respectivos usuários
  - Gerar um log completo em `logs/`

---

## 🔍 Auditoria de Ativos Duplicados

Verifica quem tem mais de um **headset**, **monitor** ou **webcam**.

### Executar:

```bash
python -m src.audit
```

### Resultado:

Um arquivo será salvo como:

```
usuarios_com_ativos_duplicados.csv
```

Exemplo de conteúdo:

```csv
username,item_type,quantidade
joao.silva,monitor,2
ana.moura,headset,3
```

---

## 🪵 Logs Automáticos

Todos os resultados da transferência são registrados automaticamente em:

```
logs/log_transferencias_<DATA_HORA>.txt
```

---

## 🧼 .gitignore

Ignora arquivos e pastas desnecessárias:

```
__pycache__/
.env
logs/
*.pyc
*.zip
```

---

## 🚀 Melhorias Futuras

- Integração com banco de dados para controle histórico
- Validação de tipos de ativos por regex
- Exportação em Excel com gráficos
- Interface Web para uploads e controle de erros

---