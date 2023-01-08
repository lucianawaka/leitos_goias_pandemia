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
        self.dt_qt_leitos_sus_nsus = None
        
        
    # Funções para dados de leitos cadastrados no subsistema LT do sistema CNES - SUS e NÃO SUS
    def transform_competen_to_datetime(self):
        '''Função para transformar a coluna competência em date yyyy-mm-dd'''
        
        self.df_lt['COMPETEN'] = self.df_lt['COMPETEN'].astype(str)
        self.df_lt['COMPETEN'] =  self.df_lt['COMPETEN'].map(lambda data: pd.to_datetime(data+'01',format='%Y-%m-%d'))
    
    
    def create_year_column(self):
        '''Função para criar uma coluna com o ano da competência'''
        self.df_lt['ANO'] =  self.df_lt['COMPETEN'].map(lambda ano:ano.strftime("%Y"))

    
    def create_df_leitos_sus_nsus_goias(self):
        '''Função para retornar os dados de leitos SUS e não SUS de Goiás'''
        
        # Qt leitos SUS por Competência
        qt_sus = self.df_lt.groupby(['COMPETEN'])['QT_SUS'].sum()
    
        # Qt leitos NÃO SUS por Competência
        qt_nsus = self.df_lt.groupby(['COMPETEN'])['QT_NSUS'].sum()

        qt_sus.columns = ['COMPETEN', 'Quantidade Leitos SUS']
        qt_nsus.columns = ['COMPETEN', 'Quantidade Leitos NÃO SUS']
        
        self.dt_qt_leitos_sus_nsus = pd.merge(qt_sus, qt_nsus, how = 'inner', on = 'COMPETEN')
    
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
        
    
    # Funções para contexto geográfico	
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
    
    def get_dados_lat_lon_goias(self):
        '''Função para retornar os dados de latitude e longitude de todos os municípios de Goiás'''
        if self.dados_lat_lon_goias is None:
            self.dados_lat_lon_goias = self.dados_municipios[self.dados_municipios['codigo_uf']==52]
        return self.dados_lat_lon_goias
    
    def transform_codigoibge_7to6_digits(self):
        '''Função para transformar o código do IBGE de 7 dígitos para 6 dígitos'''
        self.dados_lat_lon_goias['codigo_ibge'] = self.dados_lat_lon_goias['codigo_ibge'].astype(str)
        # Aplica lambda para transformar o código do IBGE de 7 dígitos para 6 dígitos
        self.dados_lat_lon_goias['codigo_ibge'] = self.dados_lat_lon_goias['codigo_ibge'].map(lambda num: num[:6])
        self.dados_lat_lon_goias['codigo_ibge'] = self.dados_lat_lon_goias['codigo_ibge'].astype(int)
        return self.dados_lat_lon_goias
    
    def merge_df_lt_dados_lat_lon_goias(self):
        '''Função para fazer o merge entre o dataframe de leitos e o dataframe de latitude e longitude dos municípios de Goiás'''
        self.df_lt_municipios_goias = pd.merge(self.df_lt, self.dados_lat_lon_goias, how='left', left_on=['CODUFMUN'], right_on=['codigo_ibge'])
        return self.df_lt_municipios_goias 