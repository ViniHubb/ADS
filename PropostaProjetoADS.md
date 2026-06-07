Universidade Federal de Ouro Preto

Instituto de Ciências Exatas e Aplicadas 

Departamento de Computação e Sistemas (DECSI)

(CSI693) \- Avaliação de desempenho de sistemas \- Turma 11

Proposta de projeto

Géssica Teixeira Bomfim \- 21.1.8019

Laura Lima Marques \- 21.1.8022

Paulo Luiz Mendes Souza \- 21.1.8011

Vinicius Niquini Andrade de Jesus \- 21.1.8008

Professor: Darlan Nunes de Brito

João Monlevade

Maio de 2026

[**Definição do problema	2**](#definição-do-problema)

[**Motivação	2**](#motivação)

[**Trabalhos relacionados	2**](#trabalhos-relacionados)

[**Cronograma e metodologia	3**](#cronograma-e-metodologia)

[**Referências	4**](#referências)

## Definição do problema {#definição-do-problema}

O objetivo deste projeto é caracterizar a carga de trabalho e dimensionar a infraestrutura computacional de um e-commerce do setor de cosméticos utilizando dados empíricos de navegação. O problema central consiste em processar logs reais de acesso (contendo eventos como view, cart, remove\_from\_cart e purchase) para aplicar técnicas de agrupamento e redução de dimensionalidade (PCA), identificando os diferentes perfis de comportamento dos usuários. Com base na taxa de chegada de requisições extraída dessa caracterização, buscaremos aplicar a modelagem analítica (teoria das filas) e o projeto de experimentos (modelo Fatorial $2^k$) para determinar a configuração ideal entre servidores Web e de Banco de Dados. A meta é garantir tempos de resposta dentro dos limites aceitáveis durante variações extremas de tráfego, sem recorrer a escolhas arbitrárias de infraestrutura.

## Motivação {#motivação}

Em sistemas de e-commerce voltados para o nicho de beleza e cosméticos, o comportamento do usuário envolve intensa navegação visual e comparação de produtos, gerando uma carga de trabalho onde a proporção de requisições de visualização (views) é muito superior às transações financeiras efetivas (purchases). O dimensionamento baseado apenas em intuição frequentemente resulta em dois erros comuns, o subdimensionamento, que causa gargalos, lentidão sistêmica e perda direta de receita por abandono de carrinho, ou o superdimensionamento, que eleva drasticamente os custos operacionais de nuvem sem retorno financeiro proporcional.

A motivação principal deste trabalho é substituir decisões empíricas por metodologias quantitativas de Engenharia de Desempenho. Ao compreender matematicamente o impacto de diferentes componentes do sistema através da análise de variância (ANOVA), torna-se possível encontrar o ponto ótimo de investimento. Isso garante um ambiente resiliente a picos de demanda promocionais, assegurando a qualidade de serviço ao usuário ao mesmo tempo em que se otimiza a alocação de recursos financeiros e computacionais da empresa.

## Trabalhos relacionados {#trabalhos-relacionados}

Dois artigos foram escolhidos e serão analisados para auxiliar na realização do projeto. O primeiro, “A Methodology for Workload Characterization of E-commerce Sites”, propõe uma metodologia para caracterização de carga de trabalho em sites de comércio eletrônico, utilizando modelos de comportamento dos usuários e padrões de navegação para compreender melhor as interações realizadas no sistema. O artigo também apresenta métricas e algoritmos voltados para análise e agrupamento de perfis de acesso.

O segundo, “Workload Characterization for an E-commerce Web Site”, analisa as características das requisições feitas a um servidor de e-commerce, observando aspectos como utilização de páginas dinâmicas, protocolos SSL, acesso a imagens e distribuição das requisições ao longo do tempo, buscando identificar fatores que impactam o desempenho dos servidores web.

## Cronograma e metodologia {#cronograma-e-metodologia}

O projeto será desenvolvido em etapas simples. Primeiro, será definida a carga de trabalho do sistema com base em dados reais de um marketplace. Esses dados serão analisados usando estatísticas básicas para entender o comportamento dos usuários. Depois, serão aplicadas técnicas para identificar padrões de uso, como agrupamento de dados.

Em seguida, será criado um modelo simplificado do sistema para avaliar seu desempenho em diferentes níveis de carga. Também serão realizados experimentos, variando alguns parâmetros do sistema, para observar como eles afetam o desempenho. Os resultados serão analisados com apoio de métodos estatísticos e, por fim, interpretados para identificar possíveis problemas e sugerir melhorias na infraestrutura.

**Etapa 1**

* Definição do problema, planejamento inicial e entrega da proposta  
* Decidir o escopo exato, escolher o dataset público que será usado e escrever o documento estipulando os objetivos, a motivação e a metodologia simplificada. 

**Etapa 2**

* Estudo das técnicas e definição/coleta da carga de trabalho  
* Análise exploratória e caracterização da carga  
* Aplicação de técnicas de caracterização (ex: agrupamento e redução de dados)  
* Baixar o dataset, extrair as informações mais importantes e rodar os scripts de Python para sumarização estatística, Análise de Componentes Principais (PCA) e Clusterização.

**Etapa 3**

* Desenvolvimento da abordagem de avaliação de desempenho  
* Execução dos experimentos e coleta de resultados  
* Análise dos resultados e interpretação  
* Usar a Teoria das Filas (Modelagem Analítica) com os dados da Etapa 2 para dimensionar os servidores. Em seguida, aplicar o Projeto Fatorial $2^k$ e a ANOVA para descobrir matematicamente qual configuração de servidor é a melhor.

**Etapa 4**

* Escrita do relatório final e preparação para entrega  
* Juntar a proposta da Etapa 1, os gráficos da Etapa 2 e as tabelas matemáticas da Etapa 3 em um único documento. Escrever a análise crítica e formatar a apresentação final.

## Referências {#referências}

WANG, Qing et al. Workload characterization for an E-commerce web site. In: **CASCON**. 2003\. p. 313-327. 

MENASCÉ, Daniel A. et al. A methodology for workload characterization of e-commerce sites. In: **Proceedings of the 1st ACM conference on Electronic commerce**. 1999\. p. 119-128. 

MKECHINOV, M. *eCommerce events history in cosmetics shop*. San Francisco: Kaggle, 2020\. Disponível em: [https://www.kaggle.com/datasets/mkechinov/ecommerce-events-history-in-cosmetics-shop](https://www.kaggle.com/datasets/mkechinov/ecommerce-events-history-in-cosmetics-shop).