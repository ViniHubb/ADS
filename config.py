# -*- coding: utf-8 -*-
"""
config.py
=========
Parametros centralizados do projeto de Avaliacao de Desempenho (CSI693 / UFOP).

Ajuste aqui os caminhos e as constantes; os dois scripts (etapa2 e etapa3)
importam tudo deste arquivo. Assim voce muda o mes analisado, a fracao de
amostragem, o SLA, etc. em um unico lugar.
"""

import os

# ---------------------------------------------------------------------------
# Caminhos
# ---------------------------------------------------------------------------
# Pasta onde estao os CSVs baixados do Kaggle (eCommerce events history in
# cosmetics shop). Ordem de busca (portavel entre maquinas):
#   1) variavel de ambiente ADS_DATASET, se definida;
#   2) a pasta "dataset" dentro do projeto (padrao recomendado);
# Os CSVs NAO vao para o GitHub (sao grandes); cada colega baixa do Kaggle
# e coloca em ./dataset/  (veja o README).
_PASTA_PROJETO = os.path.dirname(os.path.abspath(__file__))
PASTA_DADOS = os.environ.get(
    "ADS_DATASET", os.path.join(_PASTA_PROJETO, "dataset"))

# Mes que sera analisado (etapa de caracterizacao). Use 1 mes para ser rapido.
ARQUIVO_MES = "2019-Oct.csv"

# Caminho completo do arquivo do mes escolhido.
CAMINHO_CSV = os.path.join(PASTA_DADOS, ARQUIVO_MES)

# Pastas de saida (criadas automaticamente em tempo de execucao).
PASTA_RESULTADOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resultados")
PASTA_FIGURAS = os.path.join(PASTA_RESULTADOS, "figuras")
ARQUIVO_PARAMETROS = os.path.join(PASTA_RESULTADOS, "parametros.json")

# ---------------------------------------------------------------------------
# Leitura / amostragem (etapa 2)
# ---------------------------------------------------------------------------
# Tamanho do bloco lido por vez (linhas). Mantem o uso de memoria baixo.
CHUNKSIZE = 1_000_000

# Amostragem deterministica por sessao: ~1/SAMPLE_DIVISOR das sessoes.
# Ex.: 10 -> aproximadamente 10% das sessoes (sessoes completas preservadas).
SAMPLE_DIVISOR = 10

# Semente para reprodutibilidade (clustering, simulacao, etc.).
SEED = 42

# ---------------------------------------------------------------------------
# Clusterizacao (etapa 2)
# ---------------------------------------------------------------------------
# Faixa de k testada no metodo do cotovelo / silhueta.
K_MIN = 2
K_MAX = 8

# ---------------------------------------------------------------------------
# Avaliacao de desempenho / filas (etapa 3)
# ---------------------------------------------------------------------------
# Demandas de servico POR REQUISICAO (em segundos). O dataset NAO traz tempos
# de servidor, entao estes valores sao PREMISSAS de engenharia (documentadas
# no relatorio). Web costuma ser mais leve que o Banco de Dados.
D_WEB = 0.004   # 4 ms por requisicao no servidor Web
D_DB = 0.010    # 10 ms por requisicao no servidor de Banco de Dados

# Objetivo de tempo de resposta (SLA), em segundos.
SLA_SEGUNDOS = 1.0

# ---------------------------------------------------------------------------
# Projeto de Experimentos - Fatorial 2^k (etapa 3)
# ---------------------------------------------------------------------------
# Numero de replicas (seeds diferentes) por combinacao de fatores.
R_REPLICAS = 10

# Numero de clientes (requisicoes) simulados em cada execucao da fila.
N_CLIENTES_SIM = 50_000

# Nivel de confianca para os intervalos (ex.: 0.95 -> 95%).
NIVEL_CONFIANCA = 0.95

# Fatores do experimento 2^k. Para cada fator, (nivel_baixo, nivel_alto).
# A = velocidade do servidor Web  -> demanda de servico D_web (s). Menor = mais rapido.
FATOR_A_WEB = (0.006, 0.003)      # lento (6 ms)  vs  rapido (3 ms)
# B = velocidade do servidor de BD -> demanda de servico D_db (s).
FATOR_B_DB = (0.014, 0.007)       # lento (14 ms) vs  rapido (7 ms)
# C = taxa de chegada lambda (req/s). (normal, pico). Se None, usa os valores
# de lambda medio/pico extraidos do dataset na etapa 2.
FATOR_C_LAMBDA = None
