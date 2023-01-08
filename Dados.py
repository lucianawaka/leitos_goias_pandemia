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
        # Carrega os dados de leitos sus e não sus
        self.df_lt = pd.read_csv('csv/df_lt.csv', encoding = "ISO-8859-1", low_memory=False, index_col=None)
        self.dt_qt_leitos_sus_nsus = pd.read_csv('csv/df_leitos_sus_nsus_goias.csv', encoding = "ISO-8859-1", low_memory=False, index_col=None)
        # Carrega os dados de malha do estado de Goiás
        self.malha_goias = requests.get('https://servicodados.ibge.gov.br/api/v3/malhas/estados/GO?formato=application/vnd.geo+json')
        
        
        
        
        self.dados_municipios = pd.read_csv('csv/municipios.csv', encoding='utf-8', low_memory=False, index_col=None)
        self.dados_lat_lon_goias = None
        self.df_lt_municipios_goias = None
        
    # Introdução - contexto geral do projeto - Estado de Goiás
    def mapa_estado_goias(self):
        '''Função para gerar um mapa do estado de Goiás'''
        json_goias_malha = self.malha_goias.json()
        
        mapa_goias = folium.Map(
            location=[-14.4086569,-51.31668],
            tiles="cartodbpositron",
            zoom_start=6,
        )

        folium.GeoJson(json_goias_malha, name="geojson").add_to(mapa_goias)
        folium.LayerControl().add_to(mapa_goias)
        
        return mapa_goias     
    
    # Desenvolvimento - Análise dos dados de leitos SUS e não SUS
    def generate_lineplot_qt_leitos_sus_nsus(self):
        '''Função para gerar um gráfico de linha com a quantidade de leitos SUS e não SUS por ano'''
        
        # Configura o tema do gráfico
        ## Cores
        colors = ['#282f6b', '#b22200', '#eace3f', '#224f20', '#b35c1e', '#419391', '#839c56','#3b89bc']
        ## Tamanho
        theme = {'figure.figsize' : (15, 10)}
        ## Aplica o tema
        sns.set_theme(rc = theme,
                    palette = colors)
        plt.figure(figsize=(15,10))
        plt.suptitle('Quantidade de Leitos SUS e não SUS por Ano', fontsize=20, color='#404040', fontweight=550, y = 0.95)
        plt.xlabel(' ')
        sns.lineplot(data = self.dt_qt_leitos_sus_nsus) # dados leitos sus e não sus
        plt.legend(fontsize=20)
        plt.legend(fontsize="x-large", labels=["Leitos SUS", "Leitos não SUS"]) 
        plt.annotate('Fonte: https://datasus.saude.gov.br/transferencia-de-arquivos - CNES/LT',
                    xy = (1.0, -0.07),
                    xycoords='axes fraction',
                    ha='right',
                    va="center",
                    fontsize=14);    
        
    

    
