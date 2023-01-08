# Bibliotecas
# Processamento dos dados - Pandas
import pandas as pd
# Extrair dados de uma API
import json
import requests
# Visualização de mapas
import folium
from folium.features import Choropleth
# Visualização dos dados - Matplotlib e Seaborn
import matplotlib.pyplot as plt
import seaborn as sns



class Dados:
    
    def __init__(self):
        self.df_lt = pd.read_csv('data/cnes_LT.csv', encoding = "ISO-8859-1", sep = ';', low_memory=False, index_col=None)
        self.malha_goias = requests.get('https://servicodados.ibge.gov.br/api/v3/malhas/estados/GO?formato=application/vnd.geo+json')
        self.dados_municipios = pd.read_csv('csv/municipios.csv', encoding='utf-8', low_memory=False, index_col=None)
        self.dados_lat_lon_goias = None
        self.df_lt_municipios_goias = None
        
    def mapa_estado_goias(self):
        json_goias_malha = self.malha_goias.json()
        
        mapa_goias = folium.Map(
            location=[-14.4086569,-51.31668],
            tiles="cartodbpositron",
            zoom_start=6,
        )

        folium.GeoJson(json_goias_malha, name="geojson").add_to(mapa_goias)
        folium.LayerControl().add_to(mapa_goias)
        
        return mapa_goias
    
    def get_dados_lat_lon_goias(self):
        if self.dados_lat_lon_goias is None:
            self.dados_lat_lon_goias = self.dados_municipios[self.dados_municipios['codigo_uf']==52]
        return self.dados_lat_lon_goias
    
    def transform_codigoibge_7to6_digits(self):
        self.dados_lat_lon_goias['codigo_ibge'] = self.dados_lat_lon_goias['codigo_ibge'].astype(str)
        # Aplica lambda para transformar o código do IBGE de 7 dígitos para 6 dígitos
        self.dados_lat_lon_goias['codigo_ibge'] = self.dados_lat_lon_goias['codigo_ibge'].map(lambda num: num[:6])
        self.dados_lat_lon_goias['codigo_ibge'] = self.dados_lat_lon_goias['codigo_ibge'].astype(int)
        return self.dados_lat_lon_goias
    
    def merge_df_lt_dados_lat_lon_goias(self):
        self.df_lt_municipios_goias = pd.merge(self.df_lt, self.dados_lat_lon_goias, how='left', left_on=['CODUFMUN'], right_on=['codigo_ibge'])
        return self.df_lt_municipios_goias 