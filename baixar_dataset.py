# -*- coding: utf-8 -*-
"""
baixar_dataset.py
=================
Download automatico do dataset publico do Kaggle (eCommerce events history in
cosmetics shop) usando kagglehub - a mesma abordagem do notebook ADS_PROJECT.

Vantagem do kagglehub: para um dataset PUBLICO ele baixa sem exigir token
configurado a mao (em Colab/Kaggle autentica sozinho). Em vez de cada colega
baixar e copiar o CSV manualmente, este modulo localiza/baixa SOZINHO o
arquivo do mes necessario e devolve o caminho dele.

Para economizar banda/disco, baixamos apenas o CSV do mes (config.ARQUIVO_MES)
via o parametro path=, e nao o dataset inteiro (~2,4 GB).

Uso isolado (opcional):
    python baixar_dataset.py
"""

import os

import config

# Identificador do dataset no Kaggle (dono/slug), extraido da URL:
# https://www.kaggle.com/datasets/mkechinov/ecommerce-events-history-in-cosmetics-shop
DATASET_KAGGLE = "mkechinov/ecommerce-events-history-in-cosmetics-shop"


def garantir_dataset(arquivo=None):
    """
    Garante que o CSV do mes esteja disponivel e retorna o caminho completo
    dele. Se ja existir localmente (em config.PASTA_DADOS), usa esse; caso
    contrario, baixa do Kaggle via kagglehub.
    """
    arquivo = arquivo or config.ARQUIVO_MES

    # 1) Se o colega ja colocou o CSV na pasta local (ou via ADS_DATASET), usa.
    local = os.path.join(config.PASTA_DADOS, arquivo)
    if os.path.exists(local):
        return local

    # 2) Senao, baixa do Kaggle. Importamos aqui dentro para que a ausencia do
    #    pacote so atrapalhe quando realmente precisarmos baixar.
    try:
        import kagglehub
    except ImportError:
        raise SystemExit(
            "ERRO: o pacote 'kagglehub' nao esta instalado.\n"
            "   Rode:  pip install -r requirements.txt\n"
            "   (ou:   pip install kagglehub)")

    print(f"Dataset nao encontrado localmente. Baixando do Kaggle: {arquivo}")
    try:
        # path= baixa apenas o arquivo do mes (nao o dataset inteiro).
        caminho = kagglehub.dataset_download(DATASET_KAGGLE, path=arquivo)
    except Exception as e:
        raise SystemExit(
            "ERRO: nao foi possivel baixar o dataset do Kaggle.\n"
            f"   Detalhe: {e}\n\n"
            "   Em alguns ambientes o kagglehub pede login na primeira vez.\n"
            "   Alternativa: baixe o CSV manualmente do Kaggle e coloque em:\n"
            f"       {config.PASTA_DADOS}\n"
            "   https://www.kaggle.com/datasets/mkechinov/"
            "ecommerce-events-history-in-cosmetics-shop")

    print(f"   OK! Dataset pronto em: {caminho}")
    return caminho


if __name__ == "__main__":
    garantir_dataset()
