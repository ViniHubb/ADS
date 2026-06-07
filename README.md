# Análise de Desempenho — E-commerce de Cosméticos (CSI693 / UFOP)

Código da análise do projeto de **Avaliação de Desempenho de Sistemas**.
Aplica, sobre o dataset *eCommerce events history in cosmetics shop* (Kaggle),
as três famílias de técnicas exigidas pelo professor:

| Técnica exigida | Onde está |
|---|---|
| Sumarização estatística + histogramas | `etapa2_caracterizacao.py` |
| PCA (Análise de Componentes Principais) | `etapa2_caracterizacao.py` |
| Clusterização (K-Means) → perfis de usuário | `etapa2_caracterizacao.py` |
| Teoria das Filas (modelagem analítica, M/M/c) | `etapa3_filas_experimentos.py` |
| Simulação de fila (validação) | `etapa3_filas_experimentos.py` |
| Fatorial 2^k, ANOVA, IC, erro máximo e nº de amostras | `etapa3_filas_experimentos.py` |

## Arquivos

- `config.py` — todos os parâmetros (mês usado, SLA, demandas de serviço,
  nº de réplicas...). **Ajuste aqui** para mudar a configuração.
- `etapa2_caracterizacao.py` — caracterização da carga.
- `etapa3_filas_experimentos.py` — avaliação de desempenho + experimentos.
- `requirements.txt` — dependências.
- `dataset/` — onde ficam os CSVs (os arquivos **não** vão para o GitHub).
- `resultados/figuras/` — gráficos gerados (criada automaticamente).
- `resultados/parametros.json` — taxa de chegada λ extraída na etapa 2 e usada na etapa 3.

## Como executar (passo a passo)

### 1. Clonar o repositório

```powershell
git clone <URL-do-repositorio>
cd ADS
```

### 2. Baixar o dataset (NÃO vem no repositório)

Os CSVs têm ~2,4 GB no total, então **não** ficam no GitHub. Baixe do Kaggle e
coloque os arquivos `.csv` na pasta `dataset/`:

🔗 https://www.kaggle.com/datasets/mkechinov/ecommerce-events-history-in-cosmetics-shop

A pasta deve ficar assim:

```
dataset/
  2019-Oct.csv
  2019-Nov.csv
  ...
```

> Basta o `2019-Oct.csv` para rodar com a configuração padrão. Se quiser deixar
> os CSVs em outro lugar, aponte a variável de ambiente `ADS_DATASET` para a
> pasta deles (ex.: `$env:ADS_DATASET = "D:\dados"`), sem precisar editar o código.

### 3. Instalar as dependências

```powershell
pip install -r requirements.txt
```

> ⚠️ **Python 3.14 é muito novo.** Se a instalação de alguma biblioteca
> falhar (sem *wheel* disponível), crie um ambiente virtual com Python 3.12:
>
> ```powershell
> py -3.12 -m venv .venv
> .\.venv\Scripts\Activate.ps1
> pip install -r requirements.txt
> ```

### 4. Rodar os scripts

Execute na ordem (a etapa 2 gera o `parametros.json` que a etapa 3 consome):

```powershell
python etapa2_caracterizacao.py
python etapa3_filas_experimentos.py
```

As tabelas/números aparecem no **console** e os gráficos são salvos em
`resultados/figuras/`. Basta copiá-los para o relatório final.

## Observações metodológicas (para o relatório)

- **Amostragem:** por padrão processa-se **1 mês** (`2019-Oct.csv`) com amostra
  determinística de ~10% das *sessões* (sessões completas preservadas), o que
  mantém o uso de memória baixo. Ajuste `SAMPLE_DIVISOR`/`ARQUIVO_MES` em `config.py`.
- **Premissas das filas:** o dataset não contém tempos de servidor; portanto as
  demandas de serviço `D_WEB`/`D_DB` e o `SLA` são premissas de engenharia,
  declaradas em `config.py` e impressas na execução. A taxa de chegada λ, essa
  sim, é extraída dos dados (eventos por segundo).
- **2^k:** o sub-modelo do experimento usa 1 servidor por estágio para isolar o
  efeito da *velocidade* dos servidores; os níveis de λ são escalados para manter
  a fila estável. A simulação com réplicas fornece o erro experimental real usado
  na ANOVA.
