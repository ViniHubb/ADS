# -*- coding: utf-8 -*-
"""
etapa3_filas_experimentos.py
============================
ETAPA 3 - Avaliacao de Desempenho + Projeto de Experimentos.

Conteudo:
  1. Parametros: le lambda (taxa de chegada) gerado pela etapa 2.
  2. Modelagem ANALITICA (Teoria das Filas, M/M/c) -> dimensiona os
     servidores Web e de Banco para atender o SLA no pico de trafego.
  3. SIMULACAO de fila (recursao de Lindley, dois estagios em serie) e
     validacao contra o modelo analitico.
  4. Projeto Fatorial 2^k (k=3) com replicas:
        - efeitos, soma de quadrados e % de contribuicao;
        - tabela ANOVA (F e p-valor);
        - intervalos de confianca dos efeitos;
        - erro maximo e numero ideal de amostras.

Uso:
    python etapa3_filas_experimentos.py
(rode a etapa 2 antes, para gerar resultados/parametros.json)
"""

import os
import json
import itertools

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats

import config


# ---------------------------------------------------------------------------
# Utilitarios
# ---------------------------------------------------------------------------
def titulo(texto):
    print("\n" + "=" * 70)
    print(texto)
    print("=" * 70)


def salvar_figura(nome):
    os.makedirs(config.PASTA_FIGURAS, exist_ok=True)
    caminho = os.path.join(config.PASTA_FIGURAS, nome)
    plt.tight_layout()
    plt.savefig(caminho, dpi=120)
    plt.close()
    print(f"   [figura salva] {caminho}")


def carregar_lambda():
    if not os.path.exists(config.ARQUIVO_PARAMETROS):
        raise SystemExit(
            "ERRO: resultados/parametros.json nao encontrado. "
            "Rode antes:  python etapa2_caracterizacao.py")
    with open(config.ARQUIVO_PARAMETROS, encoding="utf-8") as f:
        p = json.load(f)
    return p["lambda_medio_reqs"], p["lambda_pico_reqs"]


# ---------------------------------------------------------------------------
# 2. Modelagem analitica - M/M/c (Erlang C)
# ---------------------------------------------------------------------------
def erlang_c(c, a):
    """Probabilidade de espera (formula C de Erlang) para M/M/c.
    c = nº de servidores, a = carga oferecida em Erlangs (a = lambda/mu)."""
    rho = a / c
    if rho >= 1:
        return 1.0  # instavel
    soma = sum(a**n / _fact(n) for n in range(c))
    ultimo = a**c / (_fact(c) * (1 - rho))
    return ultimo / (soma + ultimo)


def _fact(n):
    r = 1
    for i in range(2, n + 1):
        r *= i
    return r


def resposta_mmc(lmbda, demanda, c):
    """Tempo de resposta medio em um estagio M/M/c.
    demanda = D = 1/mu (s/requisicao); c servidores."""
    mu = 1.0 / demanda
    a = lmbda / mu               # carga oferecida (Erlangs) = lambda*D
    rho = a / c
    if rho >= 1:
        return float("inf")
    pw = erlang_c(c, a)
    wq = pw / (c * mu - lmbda)   # espera media na fila
    return wq + demanda          # + tempo de servico = tempo de resposta


def dimensionar(lmbda_pico):
    titulo("2) MODELAGEM ANALITICA - Dimensionamento (Teoria das Filas, M/M/c)")
    print("PREMISSAS (o dataset nao traz tempos de servidor):")
    print(f"   D_web = {config.D_WEB*1000:.1f} ms/req   "
          f"D_db = {config.D_DB*1000:.1f} ms/req   SLA = {config.SLA_SEGUNDOS}s")
    print(f"   lambda de pico (do dataset) = {lmbda_pico:.2f} req/s")

    # nº minimo para estabilidade em cada estagio (precisa c > lambda*D => rho<1)
    c_web = int(np.floor(lmbda_pico * config.D_WEB)) + 1
    c_db = int(np.floor(lmbda_pico * config.D_DB)) + 1

    # aumenta servidores ate o tempo de resposta total ficar <= SLA
    while True:
        r_web = resposta_mmc(lmbda_pico, config.D_WEB, c_web)
        r_db = resposta_mmc(lmbda_pico, config.D_DB, c_db)
        r_total = r_web + r_db
        if r_total <= config.SLA_SEGUNDOS and r_web < float("inf") \
                and r_db < float("inf"):
            break
        # adiciona servidor ao estagio com maior tempo de resposta
        if r_web >= r_db:
            c_web += 1
        else:
            c_db += 1
        if c_web + c_db > 1000:  # guarda de seguranca
            break

    print("\nRESULTADO DO DIMENSIONAMENTO (no pico):")
    print(f"   Servidores Web necessarios : {c_web}  "
          f"(utilizacao = {lmbda_pico*config.D_WEB/c_web*100:.1f}%, "
          f"R_web = {r_web*1000:.2f} ms)")
    print(f"   Servidores BD  necessarios : {c_db}  "
          f"(utilizacao = {lmbda_pico*config.D_DB/c_db*100:.1f}%, "
          f"R_db  = {r_db*1000:.2f} ms)")
    print(f"   Tempo de resposta total    : {r_total*1000:.2f} ms "
          f"(SLA = {config.SLA_SEGUNDOS*1000:.0f} ms)")

    # grafico R x lambda: vai ate perto da SATURACAO do gargalo para mostrar
    # a curva caracteristica da fila (plana e depois disparando -> "joelho").
    # capacidade = menor taxa que satura algum estagio (c/D req/s).
    capacidade = min(c_web / config.D_WEB, c_db / config.D_DB)
    lambdas = np.linspace(1, 0.995 * capacidade, 300)
    rs = []
    for lm in lambdas:
        rw = resposta_mmc(lm, config.D_WEB, c_web)
        rd = resposta_mmc(lm, config.D_DB, c_db)
        rs.append((rw + rd) * 1000 if np.isfinite(rw + rd) else np.nan)
    plt.figure(figsize=(7, 4.5))
    plt.plot(lambdas, rs, color="#4C72B0", label="tempo de resposta")
    plt.axhline(config.SLA_SEGUNDOS * 1000, ls="--", color="#C44E52", label="SLA")
    plt.axvline(lmbda_pico, ls=":", color="gray", label="lambda pico (dados)")
    plt.axvline(capacidade, ls="-.", color="#DD8452",
                label=f"saturacao (~{capacidade:.0f} req/s)")
    # limita o eixo Y para o "joelho" e o cruzamento do SLA ficarem visiveis
    plt.ylim(0, config.SLA_SEGUNDOS * 1000 * 1.5)
    plt.title(f"Tempo de resposta x carga  (Web={c_web}, BD={c_db} servidor(es))")
    plt.xlabel("lambda (req/s)"); plt.ylabel("tempo de resposta (ms)")
    plt.legend()
    salvar_figura("08_resposta_vs_carga.png")
    print(f"   Capacidade maxima (saturacao do gargalo): ~{capacidade:.0f} req/s")
    print(f"   No pico de {lmbda_pico:.0f} req/s o sistema usa apenas "
          f"{lmbda_pico/capacidade*100:.1f}% da capacidade.")

    return c_web, c_db


# ---------------------------------------------------------------------------
# 3. Simulacao - recursao de Lindley (dois estagios em serie)
# ---------------------------------------------------------------------------
def simular_tandem(lmbda, d_web, d_db, n=None, seed=0):
    """Simula uma fila M/M/1 em dois estagios em serie (Web -> BD) via
    recursao de Lindley e retorna o tempo medio de resposta (s)."""
    if n is None:
        n = config.N_CLIENTES_SIM
    rng = np.random.default_rng(seed)

    # chegadas: interchegadas Exp(lambda) -> tempos de chegada acumulados
    interchegadas = rng.exponential(1.0 / lmbda, n)
    chegada = np.cumsum(interchegadas)

    # tempos de servico Exp(media = demanda)
    s1 = rng.exponential(d_web, n)
    s2 = rng.exponential(d_db, n)

    saida1 = np.empty(n)
    saida2 = np.empty(n)
    d1_ant = 0.0
    d2_ant = 0.0
    for i in range(n):
        # estagio 1 (Web): comeca quando chega E o servidor esta livre
        ini1 = chegada[i] if chegada[i] > d1_ant else d1_ant
        d1_ant = ini1 + s1[i]
        saida1[i] = d1_ant
        # estagio 2 (BD): chega quando sai do estagio 1
        ini2 = saida1[i] if saida1[i] > d2_ant else d2_ant
        d2_ant = ini2 + s2[i]
        saida2[i] = d2_ant

    warmup = n // 10  # descarta os 10% iniciais (regime transitorio)
    resposta = saida2[warmup:] - chegada[warmup:]
    return float(resposta.mean())


def validar_simulacao(lmbda_validacao):
    titulo("3) SIMULACAO (Lindley) x ANALITICO (M/M/1) - validacao do modelo")
    d_web, d_db = config.D_WEB, config.D_DB
    # garante estabilidade na validacao
    lm = min(lmbda_validacao, 0.7 / max(d_web, d_db))

    r_sim = simular_tandem(lm, d_web, d_db, seed=config.SEED)
    r_ana = d_web / (1 - lm * d_web) + d_db / (1 - lm * d_db)  # M/M/1 em serie
    erro = abs(r_sim - r_ana) / r_ana * 100
    print(f"   lambda usado          : {lm:.2f} req/s")
    print(f"   R analitico (M/M/1)   : {r_ana*1000:.3f} ms")
    print(f"   R simulado (Lindley)  : {r_sim*1000:.3f} ms")
    print(f"   diferenca relativa    : {erro:.2f}%  "
          f"({'OK, modelo valido' if erro < 10 else 'verificar'})")


# ---------------------------------------------------------------------------
# 4. Projeto Fatorial 2^k (k=3) com replicas
# ---------------------------------------------------------------------------
def niveis_lambda(lmbda_medio, lmbda_pico):
    """Define os dois niveis do fator C (taxa de chegada).
    Para o sub-modelo de 1 servidor por estagio, escala lambda de modo a
    manter a fila estavel mesmo na pior configuracao (servidores lentos)."""
    if config.FATOR_C_LAMBDA is not None:
        return config.FATOR_C_LAMBDA
    pior_d = max(max(config.FATOR_A_WEB), max(config.FATOR_B_DB))
    lmbda_alto = 0.80 / pior_d     # rho <= 0.80 no pior caso (estavel)
    lmbda_baixo = lmbda_alto / 2.0
    return (lmbda_baixo, lmbda_alto)


def configuracao(sinais, niv_a, niv_b, niv_c):
    """Converte sinais (-1/+1) de (A,B,C) nos parametros da simulacao.
    sinal -1 -> nivel baixo (indice 0); +1 -> nivel alto (indice 1)."""
    sa, sb, sc = sinais
    d_web = niv_a[1] if sa > 0 else niv_a[0]
    d_db = niv_b[1] if sb > 0 else niv_b[0]
    lmbda = niv_c[1] if sc > 0 else niv_c[0]
    return d_web, d_db, lmbda


def fatorial_2k(lmbda_medio, lmbda_pico):
    titulo("4) PROJETO FATORIAL 2^k (k=3) com replicas")
    niv_a = config.FATOR_A_WEB
    niv_b = config.FATOR_B_DB
    niv_c = niveis_lambda(lmbda_medio, lmbda_pico)
    r = config.R_REPLICAS

    print("FATORES (nivel baixo '-' / nivel alto '+'):")
    print(f"   A = veloc. Web  : D_web = {niv_a[0]*1000:.1f}ms (-)  /  "
          f"{niv_a[1]*1000:.1f}ms (+)")
    print(f"   B = veloc. BD   : D_db  = {niv_b[0]*1000:.1f}ms (-)  /  "
          f"{niv_b[1]*1000:.1f}ms (+)")
    print(f"   C = carga lambda: {niv_c[0]:.1f} (-)  /  {niv_c[1]:.1f} req/s (+)")
    print(f"   Replicas por combinacao: r = {r}")
    print(f"   (lambda real do dataset: medio={lmbda_medio:.1f}, "
          f"pico={lmbda_pico:.1f} req/s)")

    # --- matriz do experimento: 8 combinacoes x r replicas ---
    combinacoes = list(itertools.product([-1, 1], repeat=3))  # (A,B,C)
    nomes = ["A", "B", "C", "AB", "AC", "BC", "ABC"]

    cell_means = []         # media de cada combinacao
    todas_respostas = []    # todas as observacoes (para erro/amostras)
    matriz_obs = np.zeros((8, r))

    print("\nRodando simulacoes...")
    for i, sinais in enumerate(combinacoes):
        d_web, d_db, lmbda = configuracao(sinais, niv_a, niv_b, niv_c)
        for j in range(r):
            y = simular_tandem(lmbda, d_web, d_db,
                               seed=config.SEED + 100 * i + j)
            matriz_obs[i, j] = y
            todas_respostas.append(y)
        cell_means.append(matriz_obs[i].mean())
    cell_means = np.array(cell_means)
    todas_respostas = np.array(todas_respostas)

    # --- matriz de sinais (contrastes) incluindo interacoes ---
    A = np.array([c[0] for c in combinacoes])
    B = np.array([c[1] for c in combinacoes])
    C = np.array([c[2] for c in combinacoes])
    colunas = {
        "A": A, "B": B, "C": C,
        "AB": A * B, "AC": A * C, "BC": B * C, "ABC": A * B * C,
    }

    # --- efeitos (coeficientes q) e soma de quadrados ---
    n_comb = 8
    media_geral = todas_respostas.mean()
    efeitos, SS = {}, {}
    for nome in nomes:
        s = colunas[nome]
        q = np.sum(s * cell_means) / n_comb           # coeficiente do modelo
        efeitos[nome] = q
        SS[nome] = (q ** 2) * n_comb * r              # soma de quadrados

    # --- SST e SSE ---
    SST = np.sum((todas_respostas - media_geral) ** 2)
    SSE = np.sum((matriz_obs - cell_means[:, None]) ** 2)  # variacao intra-celula
    # checagem: SST ~ soma(SS efeitos) + SSE

    # --- ANOVA ---
    df_efeito = 1
    df_erro = n_comb * (r - 1)
    MSE = SSE / df_erro
    alpha = 1 - config.NIVEL_CONFIANCA
    t_crit = stats.t.ppf(1 - alpha / 2, df_erro)
    se_efeito = np.sqrt(MSE / (n_comb * r))           # erro padrao do coef.

    print("\n" + "-" * 78)
    print(f"{'Fonte':6s}{'Efeito(2q)':>14s}{'SS':>14s}{'%contrib':>10s}"
          f"{'F':>10s}{'p-valor':>10s}{'signif':>8s}")
    print("-" * 78)
    soma_contrib = 0.0
    contribs = {}
    for nome in nomes:
        ms = SS[nome] / df_efeito
        F = ms / MSE
        p = stats.f.sf(F, df_efeito, df_erro)
        contrib = SS[nome] / SST * 100
        contribs[nome] = contrib
        soma_contrib += contrib
        sig = "sim" if p < alpha else "nao"
        # "Efeito" reportado = 2*q (variacao do baixo p/ alto)
        print(f"{nome:6s}{2*efeitos[nome]*1000:>14.3f}{SS[nome]:>14.6f}"
              f"{contrib:>9.2f}%{F:>10.2f}{p:>10.4f}{sig:>8s}")
    contrib_erro = SSE / SST * 100
    print(f"{'Erro':6s}{'':>14s}{SSE:>14.6f}{contrib_erro:>9.2f}%")
    print("-" * 78)
    print(f"Efeitos em ms (variacao do nivel baixo para o alto). "
          f"SST = {SST:.6f}  (soma %: {soma_contrib+contrib_erro:.1f}%)")
    print(f"MSE = {MSE:.3e}   df_erro = {df_erro}   "
          f"t_crit({config.NIVEL_CONFIANCA*100:.0f}%) = {t_crit:.3f}")

    # --- intervalos de confianca dos efeitos ---
    print(f"\nINTERVALOS DE CONFIANCA dos coeficientes "
          f"({config.NIVEL_CONFIANCA*100:.0f}%):")
    print(f"   erro padrao do coeficiente = {se_efeito*1000:.4f} ms")
    print(f"   {'Fonte':6s}{'q (ms)':>12s}{'IC inferior':>14s}"
          f"{'IC superior':>14s}{'inclui 0?':>12s}")
    for nome in nomes:
        q_ms = efeitos[nome] * 1000
        h = t_crit * se_efeito * 1000
        lo, hi = q_ms - h, q_ms + h
        inclui0 = "sim" if lo <= 0 <= hi else "NAO (signif.)"
        print(f"   {nome:6s}{q_ms:>12.4f}{lo:>14.4f}{hi:>14.4f}{inclui0:>14s}")

    # --- erro maximo e numero ideal de amostras (sobre a resposta) ---
    titulo("Erro maximo e numero ideal de amostras (analise da resposta)")
    n_total = len(todas_respostas)
    s = todas_respostas.std(ddof=1)
    z = stats.norm.ppf(1 - alpha / 2)
    erro_max = z * s / np.sqrt(n_total)              # meia-largura do IC
    precisao_rel = 0.05                              # alvo: 5% da media
    n_ideal = (z * s / (precisao_rel * media_geral)) ** 2
    print(f"   media da resposta      : {media_geral*1000:.3f} ms")
    print(f"   desvio padrao (s)      : {s*1000:.3f} ms")
    print(f"   nº de amostras (n)     : {n_total}")
    print(f"   erro maximo ({config.NIVEL_CONFIANCA*100:.0f}%)   : "
          f"+/- {erro_max*1000:.4f} ms "
          f"({erro_max/media_geral*100:.2f}% da media)")
    print(f"   IC da media            : "
          f"[{(media_geral-erro_max)*1000:.3f}, "
          f"{(media_geral+erro_max)*1000:.3f}] ms")
    print(f"   nº ideal de amostras para precisao de "
          f"{precisao_rel*100:.0f}% : {int(np.ceil(n_ideal))}")

    # --- grafico de % de contribuicao (Pareto) ---
    itens = sorted(contribs.items(), key=lambda kv: kv[1], reverse=True)
    rotulos = [k for k, _ in itens] + ["Erro"]
    valores = [v for _, v in itens] + [contrib_erro]
    plt.figure(figsize=(8, 4))
    plt.bar(rotulos, valores, color="#4C72B0")
    plt.title("Importancia dos fatores - % de contribuicao na variacao")
    plt.ylabel("% da variacao total (SST)")
    for i, v in enumerate(valores):
        plt.text(i, v + 0.5, f"{v:.1f}%", ha="center", fontsize=8)
    salvar_figura("09_contribuicao_fatores.png")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    lmbda_medio, lmbda_pico = carregar_lambda()
    titulo("ETAPA 3 - Avaliacao de Desempenho e Projeto de Experimentos")
    print(f"lambda do dataset:  medio = {lmbda_medio:.2f} req/s   "
          f"pico = {lmbda_pico:.2f} req/s")

    dimensionar(lmbda_pico)
    validar_simulacao(lmbda_pico)
    fatorial_2k(lmbda_medio, lmbda_pico)

    titulo("ETAPA 3 CONCLUIDA")
    print("Figuras em:", config.PASTA_FIGURAS)


if __name__ == "__main__":
    main()
