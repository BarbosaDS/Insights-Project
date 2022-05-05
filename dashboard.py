import pandas as pd
import streamlit as st
import numpy as np
from streamlit_folium import folium_static
import folium
from folium.plugins import MarkerCluster
import geopandas
import plotly.express as px
from datetime import datetime

pd.set_option('display.float_format', lambda x: '%.2f' % x)

@st.cache(allow_output_mutation=True)
def get_data(path):
    data = pd.read_csv(path)

    return data

@st.cache(allow_output_mutation=True)
def get_geofile(url):
     geofile = geopandas.read_file(url)

     return geofile

def clean_data(data):
    # transformar formato da data
    data['date'] = pd.to_datetime(data['date']).dt.strftime('%Y-%m-%d')
    # Deletando os ID's repetidos, deixando o último cadastrado
    data = data.drop_duplicates(subset=['id'], keep='last')
    # Removendo imóvel com suposto erro de digitação no atributo 'bedrooms'
    data.drop(data.loc[data['bedrooms'] == 33].index, inplace=True)
    #transformando formato da coluna 'waterfront'
    data['waterfront'] = data['waterfront'].astype(str)

    return data

def set_feature(data):
    # Ano de construção: >< 1955
    data['constrution'] = data['yr_built'].apply(lambda x: '> 1955' if x > 1955
    else '< 1955')

    # Reforma
    data['renovated'] = data['yr_renovated'].apply(lambda x: 'no' if x == 0
    else 'yes')

    # Imoveis com porão ou sem porão
    data['basement'] = data['sqft_basement'].apply(lambda x: 'no' if x == 0
    else 'yes')

    # Waterfront
    data['waterfront_'] = data['waterfront'].apply(lambda x: 'sim' if x == '1'
    else 'não')

    # Colunas auxiliares pra def insights
    data['year'] = pd.to_datetime(data['date']).dt.year
    data['year'] = data['year'].astype(str)
    data['year_month'] = pd.to_datetime(data['date']).dt.strftime('%Y-%m')

    # Season
    data['mouth'] = pd.to_datetime(data['date']).dt.month
    data['season'] = data['mouth'].apply(lambda x: 'summer' if (x > 5) & (x < 8) else
    'spring' if (x > 2) & (x < 5) else
    'fall' if (x > 8) & (x < 12) else
    'winter')

    # Descrição das condições
    data['describe_condition'] = data['condition'].apply(lambda x: 'too bad' if x == 1 else
                                                         'ruim' if x == 2 else
                                                         'medio'if x == 3 else
                                                         'bom' if x == 4 else
                                                         'perfeito')

    data['price_m2'] = data['price'] / data['sqft_lot']

    return data

def buy_houses(data,geofile):


    st.sidebar.write('     ')
    st.sidebar.write('Menu 2')
    st.sidebar.write('Filtros para seleções dos imóveis sugeridos para compra e sua posterior análise de lucro pós-venda:')
    st.title('Imóveis sugeridos para compra')
    st.write('Condição:a) Imóveis abaixo do preço mediano da região')
    st.write('Condição:b) Imóveis em boas condições')

    # Agrupar os imóveis por zipcode
    df1 = data[['zipcode', 'price']].groupby('zipcode').median().reset_index()

    # renomear a coluna price criada em df1 como price_median
    df1 = df1.rename(columns={'price': 'price_median'})

    # adicionar essa coluna ao dataset original
    data = pd.merge(df1, data, on='zipcode', how='inner')

    # status
    for i in range(len(data)):
        if (data.loc[i, 'price'] < data.loc[i, 'price_median']) & (data.loc[i, 'condition'] >= 3):
            data.loc[i, 'status'] = 'buy'
        else:
            data.loc[i, 'status'] = 'no buy'

    # Seleção dos imóveis
    buy_houses = data[data['status'] == 'buy'].sort_values(by=['describe_condition', 'price'])

    f_condition = st.sidebar.multiselect('Insira a Condição', buy_houses['describe_condition'].unique())
    f_zipcode = st.sidebar.multiselect('Insira o Zipcode', buy_houses['zipcode'].unique())

    if (f_zipcode != []) & (f_condition != []):
        buy_houses = buy_houses.loc[(buy_houses['zipcode'].isin(f_zipcode)) & (buy_houses['describe_condition'].isin(f_condition)), :]
    elif (f_zipcode != []) & (f_condition == []):
        buy_houses = buy_houses.loc[data['zipcode'].isin(f_zipcode), :]
    elif (f_zipcode == []) & (f_condition != []):
        buy_houses = buy_houses.loc[buy_houses['describe_condition'].isin(f_condition), :]
    else:
        buy_houses = buy_houses.copy()

    st.dataframe(buy_houses[['id','zipcode', 'price', 'price_median', 'describe_condition']])
    st.sidebar.write('Foram encontrados {} imóveis dentro das condições acima, sugeridos para compra'.format(len(buy_houses)))

    st.title('Avaliação dos imóveis listados a partir das condições do menu 2')
    st.write('Condição: a) Se o preço da compra for maior que a mediana da região + sazonalidade. O preço da venda será igual ao preço da compra + 10% ')
    st.write('Condição: b) Se o preço da compra for menor que a mediana da região + sazonalidade. O preço da venda será igual ao preço da compra + 30% ')

    # Agrupar os imóveis por região ( coluna zipcode ) e por sazonalidade(season)
    # Dentro de cada região/season encontrar a mediana do preço do imóvel.

    df2 = data[['zipcode', 'season', 'price']].groupby(['zipcode', 'season']).median().reset_index()
    df2 = df2.rename(columns={'price': 'price_median_season'})

    # unir df2 com df
    buy_houses = pd.merge(buy_houses, df2, how='inner', on=['zipcode', 'season'])

    for i in range(len(buy_houses)):
        if buy_houses.loc[i, 'price'] <= buy_houses.loc[i, 'price_median_season']:
            buy_houses.loc[i, 'sale_price'] = buy_houses.loc[i, 'price'] * 1.30
        elif buy_houses.loc[i, 'price'] > buy_houses.loc[i, 'price_median_season']:
            buy_houses.loc[i, 'sale_price'] = buy_houses.loc[i, 'price'] * 1.10
        else:
            pass

    buy_houses['profit'] = buy_houses['sale_price'] - buy_houses['price']
    st.dataframe(buy_houses[['id','zipcode', 'price','season', 'price_median_season', 'describe_condition', 'sale_price' , 'profit']])
    st.sidebar.write('O lucro total, dada as condições, será de US$ {} '.format(buy_houses['profit'].sum()))

    # Mapa de localização
    st.title('Visão geral dos imóveis selecionados')

    st.header('Localização')

    # Base Map - Folium
    density_map = folium.Map(location=[buy_houses['lat'].mean(), buy_houses['long'].mean()], default_zoom_start=15)
    marker_cluster = MarkerCluster().add_to(density_map)

    for name, row in buy_houses.iterrows():
        folium.Marker([row['lat'], row['long']],
                      popup='Buy price U${0} |Sell Price US$ {1} with profit of US$ {2}. Features: {3} sqft, {4} bedrooms, {5} bathrooms, year built: {6}'.format(
                          row['price'],
                          row['sale_price'],
                          row['profit'],
                          row['sqft_living'],
                          row['bedrooms'],
                          row['bathrooms'],
                          row['yr_built'])).add_to(marker_cluster)

    folium_static(density_map)

    # Mapa de densidade
    st.header('Densidade de lucro')
    df4 = buy_houses[['profit', 'zipcode']].groupby('zipcode').mean().reset_index()
    df4.columns = ['ZIP', 'PROFIT']
    geofile = geofile[geofile['ZIP'].isin(df4['ZIP'].tolist())]
    region_price_map = folium.Map(location=[buy_houses['lat'].mean(), buy_houses['long'].mean()], default_zoom_start=15)
    region_price_map.choropleth(data=df4,
                                geo_data=geofile,
                                columns=['ZIP', 'PROFIT'],
                                key_on='feature.properties.ZIP',
                                fill_color='YlOrRd',
                                fill_opacity=0.7,
                                line_opacity=0.2,
                                legend_name='AVG PROFIT')

    folium_static(region_price_map)

    # ---- Insights - Imóveis selecionados --------- #

    st.title('Insights - Imóveis selecionados')
    df = buy_houses[['zipcode', 'bedrooms', 'bathrooms', 'floors', 'season',
                     'renovated', 'describe_condition', 'waterfront_', 'basement', 'grade', 'view', 'constrution']]

    st.subheader("Os atributos abaixo a maior lucratividade dentre a seleção dos imóveis acima:")
    st.write("Legenda: Profit = Lucro total por zipcode selecionado")
    st.write("         Zipcode = Zipcode Selecionado")
    st.write(" Caso não selecione nada. Aparecerá uma visão geral do lucro por zipcode")
    conditions = []
    for i in df.columns:
        ins = buy_houses[['profit', i]].groupby(i).sum().reset_index()

        plot = px.bar(ins, x=i, y='profit', color=i, labels={i: i, "profit": "Profit"},
                      template='simple_white')
        plot.update_layout(showlegend=False)
        st.plotly_chart(plot, use_container_width=True)
        ins2 = ins[ins['profit'] == ins['profit'].max()]
        conditions.append(ins2.iloc[0, 0])
        st.write('Imóveis mais lucrativos são os com "{}" igual a "{}"'.format(i, ins2.iloc[0, 0]))

    # Tabela com resumo
    st.subheader("Distribuição dos imóveis e lucros dentre os insights encontrados: ")
    dx = pd.DataFrame(columns=['atributo', 'condicao', 'total_imoveis', '%_imoveis', 'lucro_total', '%_lucro'])
    dx['atributo'] = ['zipcode', 'bedrooms', 'bathrooms', 'floors', 'season',
                      'renovated', 'describe_condition', 'waterfront_', 'basement', 'grade', 'view', 'constrution']
    dx['condicao'] = conditions

    for i in range(len(dx)):
        dx.loc[i, 'total_imoveis'] = buy_houses['id'][
            buy_houses[dx.loc[i, 'atributo']] == dx.loc[i, 'condicao']].count()
        dx.loc[i, '%_imoveis'] = float(dx.loc[i, 'total_imoveis'] / buy_houses['id'].count() * 100)
        dx.loc[i, 'lucro_total'] = buy_houses['profit'][
            buy_houses[dx.loc[i, 'atributo']] == dx.loc[i, 'condicao']].sum()
        dx.loc[i, '%_lucro'] = float(dx.loc[i, 'lucro_total'] / buy_houses['profit'].sum() * 100)

    dx["condicao"] = dx["condicao"].astype(str)
    st.dataframe(dx)

    return None

def insights(data):
    st.title('Hipóteses')

    c1, c2 = st.columns(2)

    #H1
    c1.subheader('H1 . Imóveis que possuem vista para água, são 30% mais caros, na média.')
    h1 = data[['price', 'waterfront_']].groupby('waterfront_').mean().reset_index()
    fig2 = px.bar(h1, x='waterfront_', y='price', color='waterfront_', labels={"waterfront_": "Visão para água",
                                                                            "price": "Preço"}, template='simple_white')
    fig2.update_layout(showlegend=False)
    c1.plotly_chart(fig2, use_container_width=True)
    h1_percent = (h1.loc[1, 'price'] - h1.loc[0, 'price']) / h1.loc[0, 'price']
    c1.write('H1 é verdadeira. Os imóveis com vista pra água são em média {0:.0%} mais caros'.format(h1_percent))

    # H2
    c2.subheader('H2. Móveis com data de construção menor que 1955, são 50% mais baratos, na média.')
    h2 = data[['price', 'constrution']].groupby('constrution').mean().reset_index()
    fig3 = px.bar(h2, x='constrution', y='price', color='constrution', labels={"constrution": "Ano da construção",
                                                                               "price": "Preço"},template='simple_white')
    fig3.update_layout(showlegend=False)
    c2.plotly_chart(fig3, use_container_width=True)
    h2_percent = (h2.loc[1, 'price'] - h2.loc[0, 'price']) / h2.loc[1, 'price']
    c2.write('H2 é falsa, a média do preço é irrelevante. Os imóveis construídos antes de 1955, são em média apenas {0:.0%} mais baratos'.format(h2_percent))

    c3, c4 = st.columns(2)

    #H3
    c3.subheader('H3: Imóveis sem porão (sqrt_lot), são 40% maiores do que os imóveis com porão.')
    h3 = data[['sqft_lot', 'basement']].groupby('basement').mean().reset_index()
    fig4 = px.bar(h3, x='basement', y='sqft_lot', color='basement', labels={"basement": "Imóvel com porão",
                                                                               "sqft_lot": "Tamanho total do imóvel"},
                  template='simple_white')
    fig4.update_layout(showlegend=False)
    c3.plotly_chart(fig4, use_container_width=True)
    h3_percent = (h3.loc[0,'sqft_lot'] - h3.loc[1,'sqft_lot']) / h3.loc[1,'sqft_lot']
    c3.write('H3 é verdadeira. Os imóveis sem porão possuem área do lote {0:.0%} maior. Apesar de não ser 40%, iremos considerar como verdadeiro pois a diferença é significativa e dá para usar como métrica na definição de preço para revenda'.format(h3_percent))

    #H4
    c4.subheader('H4  O crescimento do preço dos imóveis YoY ( Year over Year) é de 10%.')
    h4 = data[['price', 'year']].groupby('year').mean().reset_index()
    fig5 = px.bar(h4, x='year', y='price', color='year', labels={"year": "Ano", "price": "Preço médio"},
                  template='simple_white')
    fig5.update_layout(showlegend=False)
    c4.plotly_chart(fig5, use_container_width=True)
    h4_percent = (h4.loc[1, 'price'] - h4.loc[0, 'price']) / h4.loc[0, 'price']
    c4.write('H4 é falsa, pois o crescimento do preço entre os anos foi de {0:.2%}'.format(h4_percent))

    #H5
    st.subheader('H5: Quanto maior o número de banheiros, maior será o preço')
    h5 = data[['price', 'bathrooms']].groupby('bathrooms').mean().reset_index()
    fig6 = px.bar(h5, x='bathrooms', y='price', color='bathrooms', labels={"bathrooms": "Nº banheiros", "price": "Preço médio"},
                  template='simple_white')
    fig6.update_layout(showlegend=False)
    st.plotly_chart(fig6, x='bathrooms', y='price', use_container_width=True)
    median = h5['bathrooms'].median()
    bed_above = h5['price'][h5['bathrooms'] > median].mean()
    bed_below = h5['price'][h5['bathrooms'] < median].mean()
    h5_percent = (bed_above - bed_below) / bed_below
    st.write('H5 é verdadeira. Segundo o gráfico, o preço aumenta conforme o número de banheiros aumenta. Podemos ver que certos imóveis com 6 e 7 banheiros estão baratos. Podemos análisar as condições desse imóvel e aumentar o preço de revenda conforme.')

    return None

def overview_data(data):
    st.title('PROJETO DE INSIGHTS')
    st.subheader('https://barbosads.github.io/portfolio_projetos/')

    st.sidebar.subheader('Visualização geral:')
    st.sidebar.write('Menu 1')
    f_attributes = st.sidebar.multiselect('Escolha as colunas para VIsualização geral', data.columns)
    f_zipcode = st.sidebar.multiselect(
        'Escolha o zipcode para Average Values',
        data['zipcode'].unique())


    if (f_zipcode != []) & (f_attributes != []):
        data_overview = data.loc[data['zipcode'].isin(f_zipcode), f_attributes]
        data = data.loc[data['zipcode'].isin(f_zipcode), :]


    elif (f_zipcode != []) & (f_attributes == []):
        data_overview = data.loc[data['zipcode'].isin(f_zipcode), :]
        data = data.loc[data['zipcode'].isin(f_zipcode), :]


    elif (f_zipcode == []) & (f_attributes != []):
        data_overview = data.loc[:, f_attributes]


    else:
        data_overview = data.copy()



    st.title('Visualização geral dos Dados')
    st.write('Ver Menu 1 na barra lateral')
    st.write(data_overview.head(), height=400)


    c1, c2 = st.columns((1, 1))

    # Average metrics
    df1 = data[['id', 'zipcode']].groupby('zipcode').count().reset_index()
    df2 = data[['price', 'zipcode']].groupby('zipcode').mean().reset_index()
    df3 = data[['sqft_living', 'zipcode']].groupby('zipcode').mean().reset_index()
    df4 = data[['price_m2', 'zipcode']].groupby('zipcode').mean().reset_index()

    # merge
    m1 = pd.merge(df1, df2, on='zipcode', how='inner')
    m2 = pd.merge(m1, df3, on='zipcode', how='inner')
    df = pd.merge(m2, df4, on='zipcode', how='inner')

    df.columns = ['ZIPCODE', 'TOTAL HOUSES', 'PRICE', 'SQRT LIVING',
                  'PRICE/M2']

    c1.header('Average Values')
    c1.dataframe(df, height=300)

    # Statistic Descriptive
    num_attributes = data.select_dtypes(include=['int64', 'float64'])
    media = pd.DataFrame(num_attributes.apply(np.mean))
    mediana = pd.DataFrame(num_attributes.apply(np.median))
    std = pd.DataFrame(num_attributes.apply(np.std))

    max_ = pd.DataFrame(num_attributes.apply(np.max))
    min_ = pd.DataFrame(num_attributes.apply(np.min))

    df1 = pd.concat([max_, min_, media, mediana, std], axis=1).reset_index()

    df1.columns = ['attributes', 'max', 'min', 'mean', 'median', 'std']

    c2.header('Análise Descritiva')
    c2.dataframe(df1, height=300)

    return None



def comercial(data):
    # ====================================================
    # Distribuicao dos imoveis por categorias comerciais
    # ====================================================

    st.sidebar.title('Opções Comerciais')
    st.title('Atributos Comerciais')

    # ------- Average Price per Year
    data['date'] = pd.to_datetime(data['date']).dt.strftime('%Y-%m-%d')

    # filters
    min_year_built = int(data['yr_built'].min())
    max_year_built = int(data['yr_built'].max())

    st.sidebar.subheader('Select Max Year Built')
    f_year_built = st.sidebar.slider('Year Built', min_year_built,
                                     max_year_built,
                                     min_year_built)

    st.header('Average Price per Year built')

    # data selection
    df = data.loc[data['yr_built'] < f_year_built]
    df = df[['yr_built', 'price']].groupby('yr_built').mean().reset_index()

    fig = px.line(df, x='yr_built', y='price')

    st.plotly_chart(fig, use_container_width=True)

    # ------- Average Price per Day

    st.header('Average Price per day')
    st.sidebar.subheader('Select Max Date')

    # filters
    min_date = datetime.strptime(data['date'].min(), '%Y-%m-%d')
    max_date = datetime.strptime(data['date'].max(), '%Y-%m-%d')

    f_date = st.sidebar.slider('Date', min_date, max_date,
                               min_date)  # nesse filtro o primeiro é o minimo, segundo max e o terceiro default

    # data filtering
    data['date'] = pd.to_datetime(data['date'])

    df = data.loc[data['date'] < f_date]
    df = df[['date', 'price']].groupby('date').mean().reset_index()

    # plot
    fig = px.line(df, x='date', y='price')
    st.plotly_chart(fig, use_container_width=True)

    # --------- Histograma
    st.header('Price Distribution')
    st.sidebar.subheader(" Select Max Price")

    # filter
    min_price = int(data['price'].min())
    max_price = int(data['price'].max())
    avg_price = int(data['price'].mean())

    # data filtering
    f_price = st.sidebar.slider('Price', min_price, max_price, avg_price)
    df = data.loc[data['price'] < f_price]

    # data plot
    fig = px.histogram(df, x='price', nbins=50)  # nbins quer dizer quantas barras quer no histograma
    st.plotly_chart(fig, use_container_width=True)

    return None

def attributes_distribution(data):
    # =================================================
    # Distruibuicao dos imoveis por categorias fisicas
    # =================================================
    st.sidebar.title('Attributes Options')
    st.title('House Attributes')

    # filters
    f_bedrooms = st.sidebar.selectbox('Max number os bedrooms',
                                      sorted(set(data[
                                                     'bedrooms'].unique())))  # o sorted set é para que o filtro fique ordenado, se botar sem fica desorde

    f_bathrooms = st.sidebar.selectbox('Max number os bathrooms',
                                       sorted(set(data['bathrooms'].unique())))

    c1, c2 = st.columns(2)
    # House per bedrooms
    c1.header('Houses per bedrooms')
    df = data[data['bedrooms'] < f_bedrooms]
    fig = px.histogram(df, x='bedrooms', nbins=19)
    c1.plotly_chart(fig, use_container_width=True)

    # House per bathrooms
    c2.header('Houses per bathrooms')
    df = data[data['bathrooms'] < f_bathrooms]
    fig = px.histogram(df, x='bathrooms', nbins=19)
    c2.plotly_chart(fig, use_container_width=True)

    # filters
    f_floors = st.sidebar.selectbox('Max number of floor',
                                    sorted(set(data['floors'].unique())))

    f_waterview = st.sidebar.checkbox('Only Houses with Water view')

    c1, c2 = st.columns(2)

    # House per floors
    c1.header('Houses per floor')
    df = data[data['floors'] < f_floors]
    fig = px.histogram(df, x='floors', nbins=19)
    c1.plotly_chart(fig, use_container_width=True)

    # House per water view
    if f_waterview:
        df = data[data['waterfront'] == 1]
    else:
        df = data.copy()

    fig = px.histogram(df, x='waterfront', nbins=10)
    c2.plotly_chart(fig, use_container_width=True)

    return None


if __name__ == '__main__':


  #ETL
  # data extration
  path = 'kc_house_data.csv'
  url = 'https://opendata.arcgis.com/datasets/83fc2e72903343aabff6de8cb445b81c_2.geojson'

  # get geofile
  data = get_data(path)
  geofile = get_geofile(url)

  # transformation
  data = clean_data(data)
  data = set_feature(data)

  overview_data(data)
  insights(data)
  buy_houses( data, geofile )
  comercial(data)
  attributes_distribution(data)