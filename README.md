#  House Rocket Insights Project
Projeto de Insights de compra e venda de Imóvel

<img src="https://github.com/BarbosaDS/Insights-Project/blob/50ac3a15f168c464b6d12724ff41560dc4a7d742/projeto01.jpg" width=70% height=70%/>

## Problema de compra e venda de imóveis

A House Rocket é uma empresa do ramo imobiliário. A qual tem como função, compra e venda de imóveis. Recentemente, essa empresa recebeu um catálogo com mais de 15.000 casas para fazer uma análise de compra e venda. Por ser um alto volume de dados, a empresa não conseguiu fazer a análise de cada empresa pelos meios convencionais e recorreu a mim, um cientista de dados, para fazer a análise e tratamento desses dados para eles.

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

Todo o meu Dashboard foi criado com o intuíto de ser um App de visualização. Nele, a empresa pode selecionar a condição do imóvel e o zipcode o qual deseja análisar os dados e automaticamente irá retornar o lucro total da venda dos imóveis nas condições escolhidas. 

Através das minhas análises baseadas em sazonalidade e máximização de lucro na venda, os 5 imóveis os quais terão o maior lucro após suas vendas são os seguintes: 

<img src="https://github.com/BarbosaDS/Insights-Project/blob/fbc8bc9bac9b77caffee5e93890e95069783baaa/data.head.png">


