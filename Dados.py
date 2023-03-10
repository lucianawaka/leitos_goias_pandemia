# Bibliotecas
# Processamento dos dados - Pandas
import pandas as pd
# Extrair dados web - requests
import requests
# Visualização de mapas
import folium


class Dados:
    
    def __init__(self):
        # Carrega os dados de leitos sus e não sus
        self.df_lt = pd.read_csv('csv/df_lt.csv', encoding = "ISO-8859-1", low_memory=False, index_col=None)
        self.dt_qt_leitos_sus_nsus = pd.read_csv('csv/df_leitos_sus_nsus_goias.csv', encoding = "ISO-8859-1", low_memory=False, index_col=None)
        # Carrega os dados de malha do estado de Goiás
        self.malha_goias = requests.get('https://servicodados.ibge.gov.br/api/v3/malhas/estados/GO?formato=application/vnd.geo+json')
        
    # Introdução - contexto geral do projeto - Estado de Goiás
    def mapa_estado_goias(self):
        '''Função para gerar um mapa do estado de Goiás'''
        json_goias_malha = self.malha_goias.json()
        
        mapa_goias = folium.Map(
            location=[-14.4086569,-51.31668],
            tiles="cartodbpositron",
            zoom_start=5,
        )

        folium.GeoJson(json_goias_malha, name="geojson").add_to(mapa_goias)
        
        folium.LayerControl().add_to(mapa_goias)
        
        return mapa_goias            
        
    def index_to_dt_qt_leitos_sus_nsus(self):
        self.dt_qt_leitos_sus_nsus.set_index('COMPETEN', inplace = True)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        #########################################
        # A IMPLEMENTAR
        # self.dados_municipios = pd.read_csv('csv/municipios.csv', encoding='utf-8', low_memory=False, index_col=None)
        # self.dados_lat_lon_goias = None
        # self.df_lt_municipios_goias = None
        