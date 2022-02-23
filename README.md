#  House Rocket Insights Project
Projeto de Insights de compra e venda de Imóvel

<img src="https://github.com/BarbosaDS/Insights-Project/blob/50ac3a15f168c464b6d12724ff41560dc4a7d742/projeto01.jpg" width=70% height=70%/>

## Problema de compra e venda de imóveis

A House Rocket é uma empresa do ramo imobiliário. A qual tem como função, compra e venda de imóveis. Recentemente, essa empresa recebeu um catálogo com mais de 15.000 casas para fazer uma análise de compra e venda. Por ser um alto volume de dados, a empresa não conseguiu fazer a análise de cada imóvel pelos meios convencionais e recorreu a mim, um cientista de dados, para fazer a análise e tratamento desses dados para eles.

Essa análise tem como tarefas principais:

- Selecionar os imóveis com as melhores condições para a compra e venda.
- Criar um Dashboard iterativo no Heroku. O qual o CEO da empresa possa análisar ele mesmo os imóveis
- Trazer insights de négocio a partir dos dados disponíveis do catálogo

## Perguntas de Negócio

- Quais são os imóveis que a House Rocket deveria comprar?
- Uma vez a casa comprada, qual o melhor momento para vendê-las e por qual preço?

O trabalho de um Data Scientist, vai muito além de tratar uma enorme quantidade de dados. O principal objetivo dele, é gerar valor com esses dados, dar um objetivo e projetar um retorno financeiro com eles. 

As quatro preocupações básicas do cientista de dados são disputa de dados, engenharia de recursos, modelagem e relatórios de resultados. Entretanto, o objetivo desse projeto é exclusivamente, tratar os dados e gerar insights através dele. Apesar de simplório, irei mostrar como a maioria dos problemas que nós, cientistas, lidamos, são resolvidos com coneitos básicos e regras básicas.

## Dados utilizados:

* O Dataset foi obtido no [Kaggle](https://www.kaggle.com/harlfoxem/housesalesprediction)
* Importante se situar sobre as varíaveis abaixo antes de visualizar o dashboard no heroku

Suas variáveis são: 

Variável | Definição
------------ | -------------
|id | Núemro identificador de cada imóvel.|
|date | Data em que a propriedade ficou a venda.|
|season | estação do ano/sazonalidade que a propriedade ficou a venda.|
|price | Preço de compra de cada imóvel.|
|price_median_season | Preço de compra de cada imóvel.|
|profit | Lucro da empresa, após a venda de determinado imóvel.|
|bedrooms | Número de quartos.|
|bathrooms | O número de banheiros, o valor 0,5 indica um quarto com banheiro, mas sem chuveiro. O valor 0,75 ou 3/4 banheiro representa um banheiro que contém uma pia, um vaso sanitário e um chuveiro ou banheira.|
|sqft_living | Pés quadrados do interior das casas.|
|sqft_lot | Pés quadrados do terreno das casas.|
|floors | Número de andares.|
|waterfront | Varíavel que indica se a casa tem vista para a água ou não. Sendo 1 para Sim e 0 para não|
|view | Vista, Um índice de 0 a 4 de quão boa era a visualização da propriedade. Onde 0=baixa e 4 = alta|
|condition | Um índice de 1 a 5 sobre o estado das moradias, 1 indica propriedade ruim e 5 perfeita|
|sqft_above | Os pés quadrados do espaço habitacional interior acima do nível do solo.|
|sqft_basement | Os pés quadrados do espaço habitacional interior abaixo do nível do solo.|
|yr_built | Ano de construção da propriedade.|
|yr_renovated | Representa o ano em que o imóvel foi reformado. Considera o número ‘0’ para descrever as propriedades nunca renovadas.|
|zipcode | Um código de cinco dígitos para indicar a área onde se encontra a propriedade.|
|lat | Latitude.|
|long | Longitude.|
|sqft_living15 | O tamanho médio em pés quadrados do espaço interno de habitação para as 15 casas mais próximas.|
|sqft_lot15 | Tamanho médio dos terrenos em metros quadrados para as 15 casas mais próximas.|

*Além do dataset acima citado, foi utilizado um arquivo geojson para a criação de mapas de densidade. A API foi extraída do site ArcGIS Hub.*

## Limpeza de dados feitas:

- Foi verificado que existem diversos ID's repetidos no dataset, esses foram removidos.

- Foi identificado um Outlier e o mesmo foi removido. Se trata de um imóvel o qual o número de quartos estava muito descrepante dos padrões do dataset.


## Premissas de negócio:

- Será utilizado o critério de sazonalidade na análise exploratória de dados. Tal decisão foi tomada, pois diversos fatores decorrentes da estação do ano, interefere na definição do preço de venda do imóvel. Podemos comprar um imóvel em uma estação o qual o preço seja mais barato, e vender em uma estação que seja mais valorizado. 
 
- Todos os produtos de dados entregues devem ser acessíveis via internet e também através de dispositivos móveis.

- Todo o Planejamento da solução será discutido e análisado pelo time de negócios da empresa.

- Iremos análisar imóveis que esteja em condições apenas boas, médias e perfeitas.

## Ferramentas

Quais ferramentas serão usadas no processo?

- Python 3.9.5
- IDE Pycharm
- Streamlit
- Heroku
- Jupyter Notebook

## Planejamento da Solução:

- Coleta dos dados
- Visualização e limpeza dos dados
- Realizar a análise exploratória dos dados
- Gerar insights e validar
- Criar um dashboard com todos meus insights e colocar em produção

## Detalhamento da solução:

Todo o meu Dashboard foi criado com o intuíto de ser um App de visualização. Nele, a empresa pode selecionar a condição do imóvel e o zipcode o qual deseja análisar os dados e automaticamente irá retornar o lucro total da venda dos imóveis nas condições escolhidas. Além disso, nele contém:

 - Tabela contendo todos os imóveis do catálogo e suas caracteristicas. Podendo filtrar suas características atráves de um menu lateral
 - Tabela contendo uma análise descritiva (valor mínimo, máximo, médio, mediano e desvio padrão) de cada variável do portfólio
 - Hipóteses criadas através dos dados validadas em verdadeiras ou falsas
 - Uma tabela contendo os imóveis sugeridos para compra
 - Tabelas, mapas e gráfico interativos, mostrando várias métricas como lucro, sazonalidade entre outros. Baseados totalmente na escolha de imóveis do usuário
 - Mapa de densidade de preço e localização dos imóveis escolhidos
 - Gráfico interativo de preço médio por ano de construção do imóvel.
 - Gráfico interativo de preço médio por dia de construção do imóvel
 - Gráfico contendo a distribuição de números de quartos,banheiros,andares e vista para a água. Podendo filtrar todos os valores existentes em cada variável.
 - Gráficos comparando valores das variáveis, e definindo qual valor contem a quantidade de imóveis que trará maior lucro pós venda.
 
 ## Respondendo as perguntas de negócio:
 
1. Para responder a seguinte pergunta :"Quais são os imóveis que a House Rocket deveria comprar?", levamos em conta dois critétios para análise:
 
 - Só iremos avaliar imóveis em boas condições pra cima. Tendo em vista que imóveis com condições ruins demandam reforma o que aumentaria ainda mais o preço destinado para compra
 - Todos os imóveis que seráo destinados para compra, serão aqueles o qual o preço de venda esteja abaixo do preço médio de venda daquela região. Por naturalmente sofrer uma valorização regional.
 
2. Para responder a seguinte pergunta : "Uma vez a casa comprada, qual o melhor momento para vendê-las e por qual preço?", iremos definir duas condições para definição do preço de venda:
 
 - Se o preço da compra for maior que a mediana da região + sazonalidade. O preço da venda será igual ao preço da compra + 10%
 
 - Se o preço da compra for menor que a mediana da região + sazonalidade. O preço da venda será igual ao preço da compra + 30%

## Disponibilização de Dashboard

Link para o dashboard:  [<img alt="Heroku" src="https://img.shields.io/badge/heroku-%23430098.svg?style=for-the-badge&logo=heroku&logoColor=white"/>](https://barbosag-analytics.herokuapp.com/)

Todas minhas análises baseadas no tópico anterior, além de todas as funcionalidades já ditas do dashboard, podem ser conferidas lá.

## Principais Insights das análises:

1. Os imóveis com vista pra água são em média 212% mais caros

 - Insight : Usando o critério da sazonalidade, sabemos que certos imóveis tendem a cair de preço a depender da estação de ano em que se encontra. Prospectar para comprar imóveis com vista para a água quando os mesmos estiverem mais baratos, e vender na estação que mais será valorizado.
 
2. Quanto maior o número de banheiros, maior será o preço

- Insight: Analisando o dataframe, vimos que quanto mais banheiros, mais caro será o imóvel. Entretanto, tem imóveis com muitos banheiros que não seguem o padrão de preço dos demais,estão muito mais baratos. Tendo essa analise em vista, prospectar imóveis cujo o preço esteja abaixo dos demais, tendo em vista a quantidade de banheiros. Analisar o que o faz ser mais barato e ver formas de valorizar o seu preço na revenda.

3. Através das análises, concluímos que os 5 imóveis que trarão mais lucro na revenda sejam esses:

<img src="https://github.com/BarbosaDS/Insights-Project/blob/fbc8bc9bac9b77caffee5e93890e95069783baaa/data.head.png">


## Conclusão:

O principal objetivo do projeto era o de encontrar imóveis para compra e revenda. Além disso fazer uma análise de maximização de lucro de todas as vendas. Todos os desafios propostos foram cumpridos, então o objetivo do projeto foi alcançado. O dashboard posto em produção pode ser acesso via navegador, tanto no celular ou computador pelo [Heroku](https://barbosag-analytics.herokuapp.com/)

## Próximos passos

Melhorias nos dashboards e projetos podem ser incrementados em projetos futuros:

* Analisamos imóveis apenas com qualidade boa para melhor. Altas oportunidades podem ter sido perdidas em casas de menores qualidades
* Pode ser criado um boot via telegram onde ao botar o ID da casa apareça todas as informações sobre elas, inclusive o lucro pós venda.
* Caso tenha alguma melhoria para me sugerir, pode me contactar através do meu [LinkeldIn](https://www.linkedin.com/in/gabriel-barbosa-80a50a18a/)

Made By Gabriel Barbosa
[Portfólio](https://barbosads.github.io/portfolio_projetos/)
[LinkeldIn](https://www.linkedin.com/in/gabriel-barbosa-80a50a18a/)
