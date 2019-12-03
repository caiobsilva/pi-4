#!/usr/bin/env python
# coding: utf-8

# In[2]:


import datetime as dt
import pandas as pd
import requests
import folium
import json

#print('importado')


# In[3]:


boundaries_map = 'static/res/custom.geo.json'


# In[4]:

#FUNDOS DE PREVIDÊNCIA COMO PORCENTAGEM DO PIB
def gerar_dados_fundos():
    df_share_gdp = pd.read_csv('static/res/2.1. Assets as share of GDP.csv')

    #Eliminando colunas inúteis
    df_share_gdp.drop('Pension Plan Type', axis=1, inplace=True)
    df_share_gdp.drop('PPTYP', axis=1, inplace=True)
    df_share_gdp.drop('DTYP', axis=1, inplace=True)
    df_share_gdp.drop('Definition Type', axis=1, inplace=True)
    df_share_gdp.drop('CTYP', axis=1, inplace=True)
    df_share_gdp.drop('Contract Type', axis=1, inplace=True)
    df_share_gdp.drop('VAR', axis=1, inplace=True)
    df_share_gdp.drop('Variable', axis=1, inplace=True)
    df_share_gdp.drop('IND', axis=1, inplace=True)
    df_share_gdp.drop('Indicator', axis=1, inplace=True)
    df_share_gdp.drop('Flags', axis=1, inplace=True)
    df_share_gdp.drop('Flag Codes', axis=1, inplace=True)
    df_share_gdp.drop('Reference Period', axis=1, inplace=True)
    df_share_gdp.drop('Reference Period Code', axis=1, inplace=True)
    df_share_gdp.drop('PowerCode', axis=1, inplace=True)
    df_share_gdp.drop('PowerCode Code', axis=1, inplace=True)
    df_share_gdp.drop('Unit', axis=1, inplace=True)
    df_share_gdp.drop('YEA', axis=1, inplace=True)

    #Dividindo dataframes por anos
    df_share_gdp_2008=df_share_gdp[df_share_gdp['Year'] == 2008]
    df_share_gdp_2008.reset_index(inplace=True, drop=True)
    df_share_gdp_2009=df_share_gdp[df_share_gdp['Year'] == 2009]
    df_share_gdp_2009.reset_index(inplace=True, drop=True)
    df_share_gdp_2010=df_share_gdp[df_share_gdp['Year'] == 2010]
    df_share_gdp_2010.reset_index(inplace=True, drop=True)
    df_share_gdp_2011=df_share_gdp[df_share_gdp['Year'] == 2011]
    df_share_gdp_2011.reset_index(inplace=True, drop=True)
    df_share_gdp_2012=df_share_gdp[df_share_gdp['Year'] == 2012]
    df_share_gdp_2012.reset_index(inplace=True, drop=True)
    df_share_gdp_2013=df_share_gdp[df_share_gdp['Year'] == 2013]
    df_share_gdp_2013.reset_index(inplace=True, drop=True)
    df_share_gdp_2014=df_share_gdp[df_share_gdp['Year'] == 2014]
    df_share_gdp_2014.reset_index(inplace=True, drop=True)
    df_share_gdp_2015=df_share_gdp[df_share_gdp['Year'] == 2015]
    df_share_gdp_2015.reset_index(inplace=True, drop=True)
    df_share_gdp_2016=df_share_gdp[df_share_gdp['Year'] == 2016]
    df_share_gdp_2016.reset_index(inplace=True, drop=True)
    df_share_gdp_2017=df_share_gdp[df_share_gdp['Year'] == 2017]
    df_share_gdp_2017.reset_index(inplace=True, drop=True)
    df_share_gdp_2018=df_share_gdp[df_share_gdp['Year'] == 2018]
    df_share_gdp_2018.reset_index(inplace=True, drop=True)

    df_share_gdp_2018.head(10)


# In[5]:


#GASTOS COM PREVIDÊNCIA COM PORCENTAGEM DO PIB
def gerar_mapa_gastos(ano):
    df_gdp_spending = pd.read_csv('static/res/1.1. OECD Pensions as share GDP.csv', header=0)

    #Eliminando colunas inúteis
    df_gdp_spending.drop('INDICATOR', axis=1, inplace=True)
    df_gdp_spending.drop('MEASURE', axis=1, inplace=True)
    df_gdp_spending.drop('FREQUENCY', axis=1, inplace=True)
    df_gdp_spending.drop('Flag Codes', axis=1, inplace=True)

    #Dropa linhas de gasto privado
    i = 0
    for gasto in df_gdp_spending['SUBJECT']:
        if gasto == 'PRIV':
            df_gdp_spending.drop([i], axis=0, inplace=True)

        i+=1
    df_gdp_spending.reset_index(inplace=True,drop=True)

    #Adicionando dados brasileiros
    bra_data = {'LOCATION': ['BRA','BRA','BRA','BRA','BRA','BRA','BRA','BRA','BRA','BRA','BRA','BRA','BRA','BRA','BRA','BRA','BRA','BRA','BRA','BRA','BRA','BRA'], 
                'SUBJECT': ['PUB','PUB','PUB','PUB','PUB','PUB','PUB','PUB','PUB','PUB','PUB','PUB','PUB','PUB','PUB','PUB','PUB','PUB','PUB','PUB','PUB','PUB'], 
                'TIME': [1995,1996,1997,1998,1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016], 
                'Value': [4.98,5.25,5.15,5.76,5.75,5.77,6.00,6.08,6.52,6.65,7.00,7.20,7.04,6.78,7.16,7.38,8.20,8.30,8.40,8.50,9.00,9.90]}

    #Adicionando dados russos
    rus_data = {'LOCATION': ['RUS','RUS','RUS'], 
                'SUBJECT': ['PUB','PUB','PUB'], 
                'TIME': [2014,2015,2016], 
                'Value': [7.05,8.94,9.10]}

    #Adicionando valores máximos e mínimos
    max_data = {'LOCATION': ['MAX','MAX','MAX','MAX','MAX','MAX','MAX','MAX','MAX','MAX','MAX','MAX','MAX','MAX','MAX','MAX','MAX','MAX','MAX','MAX','MAX','MAX','MAX'], 
                'SUBJECT': ['PUB','PUB','PUB','PUB','PUB','PUB','PUB','PUB','PUB','PUB','PUB','PUB','PUB','PUB','PUB','PUB','PUB','PUB','PUB','PUB','PUB','PUB','PUB'], 
                'TIME': [1994,1995,1996,1997,1998,1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016], 
                'Value': [20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20]}

    min_data = {'LOCATION': ['MIN','MIN','MIN','MIN','MIN','MIN','MIN','MIN','MIN','MIN','MIN','MIN','MIN','MIN','MIN','MIN','MIN','MIN','MIN','MIN','MIN','MIN','MIN'], 
                'SUBJECT': ['PUB','PUB','PUB','PUB','PUB','PUB','PUB','PUB','PUB','PUB','PUB','PUB','PUB','PUB','PUB','PUB','PUB','PUB','PUB','PUB','PUB','PUB','PUB'], 
                'TIME': [1994,1995,1996,1997,1998,1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016], 
                'Value': [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]}

    df_bra = pd.DataFrame(bra_data)
    df_rus = pd.DataFrame(rus_data)
    df_max = pd.DataFrame(max_data)
    df_min = pd.DataFrame(min_data)
    df_gdp_spending = df_gdp_spending.append(df_bra)
    df_gdp_spending = df_gdp_spending.append(df_rus)
    df_gdp_spending = df_gdp_spending.append(df_max)
    df_gdp_spending = df_gdp_spending.append(df_min)
    df_gdp_spending.reset_index(inplace=True,drop=True)

    #Dividindo dataframes por anos
    df_gdp_spending_1994=df_gdp_spending[df_gdp_spending['TIME'] == 1994]
    df_gdp_spending_1994.reset_index(inplace=True, drop=True)
    df_gdp_spending_1995=df_gdp_spending[df_gdp_spending['TIME'] == 1995]
    df_gdp_spending_1995.reset_index(inplace=True, drop=True)
    df_gdp_spending_1996=df_gdp_spending[df_gdp_spending['TIME'] == 1996]
    df_gdp_spending_1996.reset_index(inplace=True, drop=True)
    df_gdp_spending_1997=df_gdp_spending[df_gdp_spending['TIME'] == 1997]
    df_gdp_spending_1997.reset_index(inplace=True, drop=True)
    df_gdp_spending_1998=df_gdp_spending[df_gdp_spending['TIME'] == 1998]
    df_gdp_spending_1998.reset_index(inplace=True, drop=True)
    df_gdp_spending_1999=df_gdp_spending[df_gdp_spending['TIME'] == 1999]
    df_gdp_spending_1999.reset_index(inplace=True, drop=True)
    df_gdp_spending_2000=df_gdp_spending[df_gdp_spending['TIME'] == 2000]
    df_gdp_spending_2000.reset_index(inplace=True, drop=True)
    df_gdp_spending_2001=df_gdp_spending[df_gdp_spending['TIME'] == 2001]
    df_gdp_spending_2001.reset_index(inplace=True, drop=True)
    df_gdp_spending_2002=df_gdp_spending[df_gdp_spending['TIME'] == 2002]
    df_gdp_spending_2002.reset_index(inplace=True, drop=True)
    df_gdp_spending_2003=df_gdp_spending[df_gdp_spending['TIME'] == 2003]
    df_gdp_spending_2003.reset_index(inplace=True, drop=True)
    df_gdp_spending_2004=df_gdp_spending[df_gdp_spending['TIME'] == 2004]
    df_gdp_spending_2004.reset_index(inplace=True, drop=True)
    df_gdp_spending_2005=df_gdp_spending[df_gdp_spending['TIME'] == 2005]
    df_gdp_spending_2005.reset_index(inplace=True, drop=True)
    df_gdp_spending_2006=df_gdp_spending[df_gdp_spending['TIME'] == 2006]
    df_gdp_spending_2006.reset_index(inplace=True, drop=True)
    df_gdp_spending_2007=df_gdp_spending[df_gdp_spending['TIME'] == 2007]
    df_gdp_spending_2007.reset_index(inplace=True, drop=True)
    df_gdp_spending_2008=df_gdp_spending[df_gdp_spending['TIME'] == 2008]
    df_gdp_spending_2008.reset_index(inplace=True, drop=True)
    df_gdp_spending_2009=df_gdp_spending[df_gdp_spending['TIME'] == 2009]
    df_gdp_spending_2009.reset_index(inplace=True, drop=True)
    df_gdp_spending_2010=df_gdp_spending[df_gdp_spending['TIME'] == 2010]
    df_gdp_spending_2010.reset_index(inplace=True, drop=True)
    df_gdp_spending_2011=df_gdp_spending[df_gdp_spending['TIME'] == 2011]
    df_gdp_spending_2011.reset_index(inplace=True, drop=True)
    df_gdp_spending_2012=df_gdp_spending[df_gdp_spending['TIME'] == 2012]
    df_gdp_spending_2012.reset_index(inplace=True, drop=True)
    df_gdp_spending_2013=df_gdp_spending[df_gdp_spending['TIME'] == 2013]
    df_gdp_spending_2013.reset_index(inplace=True, drop=True)
    df_gdp_spending_2014=df_gdp_spending[df_gdp_spending['TIME'] == 2014]
    df_gdp_spending_2014.reset_index(inplace=True, drop=True)
    df_gdp_spending_2015=df_gdp_spending[df_gdp_spending['TIME'] == 2015]
    df_gdp_spending_2015.reset_index(inplace=True, drop=True)
    df_gdp_spending_2016=df_gdp_spending[df_gdp_spending['TIME'] == 2016]
    df_gdp_spending_2016.reset_index(inplace=True, drop=True)

    #df_gdp_spending_2015.head()
    df_gdp_spending.tail(50)

    # In[6]:

    a = open('static/res/custom.geo.json')
    a = json.load(a)
    i=0

    c = []

    for co in a['features']:
        c.append(a['features'][i]['properties']['admin'])
        print(a['features'][i]['properties']['admin'])
        
        i+=1

    # In[7]:

    #Lista com todos os países do geojson
    countr_dict = {'Country': c}
    countr_dict['Country']

    # In[8]:

    #Dicionário com todos os DFs de gasto. Serve para seleção dos dados desejados.
    data_df = {1994: df_gdp_spending_1994, 
            1995: df_gdp_spending_1995, 
            1996: df_gdp_spending_1996, 
            1997: df_gdp_spending_1997, 
            1998: df_gdp_spending_1998, 
            1999: df_gdp_spending_1999, 
            2000: df_gdp_spending_2000,
            2001: df_gdp_spending_2001, 
            2002: df_gdp_spending_2002, 
            2003: df_gdp_spending_2003, 
            2004: df_gdp_spending_2004, 
            2005: df_gdp_spending_2005, 
            2006: df_gdp_spending_2006, 
            2007: df_gdp_spending_2007, 
            2008: df_gdp_spending_2008, 
            2009: df_gdp_spending_2009, 
            2010: df_gdp_spending_2010, 
            2011: df_gdp_spending_2011, 
            2012: df_gdp_spending_2012, 
            2013: df_gdp_spending_2013, 
            2014: df_gdp_spending_2014, 
            2015: df_gdp_spending_2015, 
            2016: df_gdp_spending_2016}

    data_df_funds = {2008: df_share_gdp_2008, 
                2009: df_share_gdp_2009,  
                2010: df_share_gdp_2010,  
                2011: df_share_gdp_2011,  
                2012: df_share_gdp_2012,  
                2013: df_share_gdp_2013, 
                2014: df_share_gdp_2014, 
                2015: df_share_gdp_2015,  
                2016: df_share_gdp_2016,  
                2017: df_share_gdp_2017, 
                2018: df_share_gdp_2018}


# In[12]:

def gerar_mapa_gasto(ano):
    map2 = folium.Map(location=[30,5], zoom_start=1.8, min_zoom=1.8, max_bounds=True)

    folium.Choropleth(
        geo_data=boundaries_map,
        data=data_df[ano], #seleciona os dados por meio do dicionário de dataframes
        columns=['LOCATION', 'Value'],
        key_on='feature.properties.adm0_a3',
        label_color='White',
        fill_color='RdBu',
        fill_opacity=0.8,
        line_color='White',
        line_opacity=0.4
    ).add_to(map2)

    map2.save(outfile='templates/map.html')


    print("Total de países com dados: " + str(len(data_df[ano])-2)) #-2 pq 2 valores são de max e min
    map2

def gerar_mapa_fundos(ano):
    #Mapa coroplético
    map2 = folium.Map(location=[30,5], zoom_start=1.8, min_zoom=1.8, max_bounds=True)

    folium.Choropleth(
        geo_data=boundaries_map,
        data=data_df_funds[ano], #seleciona os dados por meio do dicionário de dataframes
        columns=['COU', 'Value'],
        key_on='feature.properties.adm0_a3',
        label_color='White',
        fill_color='RdBu',
        fill_opacity=0.8,
        line_color='White',
        line_opacity=0.4
    ).add_to(map2)

    map2.save(outfile='templates/map.html')


    print("Total de países com dados: " + str(len(data_df[ano])-2)) #-2 pq 2 valores são de max e min
    map2