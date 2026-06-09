# Análise de Desempenho | E-commerce de Cosméticos

Dataset: [eCommerce events history in cosmetics shop](https://www.kaggle.com/datasets/mkechinov/ecommerce-events-history-in-cosmetics-shop) — **baixado automaticamente** (~700 MB/mês).

## Estrutura

| Arquivo | Descrição |
|---|---|
| `config.py` | Parâmetros globais — **edite aqui** |
| `baixar_dataset.py` | Baixa o CSV do mês do Kaggle se não existir em `dataset/` |
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

### 3. Rodar os scripts (nesta ordem)

```powershell
python etapa2_caracterizacao.py       # baixa o dataset e gera resultados/parametros.json
python etapa3_filas_experimentos.py   # consome parametros.json
```

O dataset é baixado automaticamente via `kagglehub` na primeira execução (sem token). Já tem os CSVs? Coloque-os em `dataset/` que o download é pulado (outra pasta: `$env:ADS_DATASET = "D:\dados"`).

Saída numérica no console; gráficos em `resultados/figuras/`.
