# Análise de Desempenho | E-commerce de Cosméticos

Dataset: [eCommerce events history in cosmetics shop](https://www.kaggle.com/datasets/mkechinov/ecommerce-events-history-in-cosmetics-shop) — **não incluso** (~2,4 GB).

## Estrutura

| Arquivo | Descrição |
|---|---|
| `config.py` | Parâmetros globais — **edite aqui** |
| `etapa2_caracterizacao.py` | Estatísticas, PCA, K-Means |
| `etapa3_filas_experimentos.py` | Filas M/M/c, simulação, fatorial 2^k |
| `requirements.txt` | Dependências |
| `dataset/` | CSVs locais (ignorados pelo git) |
| `resultados/` | Figuras e `parametros.json` (gerados automaticamente) |

## Execução

### 1. Clonar
```powershell
git clone <URL-do-repositorio>
cd ADS
```

### 2. Criar ambiente virtual e instalar dependências

> ⚠️ Python 3.14 pode não ter wheels disponíveis. Prefira Python 3.12.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1      # Windows
# source .venv/bin/activate       # Linux/macOS
pip install -r requirements.txt
```

### 3. Baixar o dataset

Coloque os CSVs em `dataset/`. O mínimo necessário para a config padrão é `2019-Oct.csv`.
Para usar outra pasta: `$env:ADS_DATASET = "D:\dados"`.

### 4. Rodar os scripts (nesta ordem)

```powershell
python etapa2_caracterizacao.py       # gera resultados/parametros.json
python etapa3_filas_experimentos.py   # consome parametros.json
```

Saída numérica no console; gráficos em `resultados/figuras/`.
