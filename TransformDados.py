# Bibliotecas
# Processamento dos dados - Pandas
import pandas as pd
# Extrair dados de uma API
import json
import requests
# Visualização de mapas

class TransformDados:
    
    def __init__(self):
        # Carrega os dados leitos sus e não sus
        self.df_lt = pd.read_csv('data/cnes_LT.csv', encoding = "ISO-8859-1", sep = ';', low_memory=False, index_col=None)
        self.dt_qt_leitos_sus_nsus = None
        
        # Carrega os dados de malha do estado de Goiás e dados de municípios para visualização geográfica
        self.malha_goias = requests.get('https://servicodados.ibge.gov.br/api/v3/malhas/estados/GO?formato=application/vnd.geo+json')
        self.dados_municipios = pd.read_csv('csv/municipios.csv', encoding='utf-8', low_memory=False, index_col=None)
        self.dados_lat_lon_goias = None
        self.df_lt_municipios_goias = None
       
          
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
        qt_sus = self.df_lt.groupby(['COMPETEN','ANO'], as_index=False)['QT_SUS'].sum()
        qt_sus = qt_sus.groupby(['ANO'], as_index=False)['QT_SUS'].mean().round().astype(int)
        # Qt leitos NÃO SUS por Competência
        qt_nsus = self.df_lt.groupby(['COMPETEN','ANO'], as_index=False)['QT_NSUS'].sum()
        qt_nsus = qt_nsus.groupby(['ANO'], as_index=False)['QT_NSUS'].mean().round().astype(int)

        qt_sus.columns = ['Ano', 'Leitos_SUS']
        qt_nsus.columns = ['Ano', 'Leitos_N_SUS']
        
        self.dt_qt_leitos_sus_nsus = pd.merge(qt_sus, qt_nsus, how = 'inner', on = 'Ano')
      
    def to_csv_df_leitos_sus_nsus_goias(self):
        '''Função para salvar os dados de leitos SUS e não SUS de Goiás em um arquivo csv'''
        self.dt_qt_leitos_sus_nsus.to_csv('csv/df_leitos_sus_nsus_goias.csv', index = False)
        
    def to_csv_df_lt(self):
        '''Função para salvar o dataframe de leitos em um arquivo csv'''
        self.df_lt = self.df_lt[['CNES','CODUFMUN','QT_EXIST','QT_SUS', 'QT_NSUS', 'COMPETEN', 'ANO']]
        self.df_lt.to_csv('csv/df_lt.csv', index = False)
      
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
      
    
    #########################################
    # A IMPLEMENTAR
             
    # Funções para contexto geográfico  
    # def get_dados_lat_lon_goias(self):
    #     '''Função para retornar os dados de latitude e longitude de todos os municípios de Goiás'''
    #     if self.dados_lat_lon_goias is None:
    #         self.dados_lat_lon_goias = self.dados_municipios[self.dados_municipios['codigo_uf']==52]
    #     return self.dados_lat_lon_goias
    
    # def transform_codigoibge_7to6_digits(self):
    #     '''Função para transformar o código do IBGE de 7 dígitos para 6 dígitos'''
    #     self.dados_lat_lon_goias['codigo_ibge'] = self.dados_lat_lon_goias['codigo_ibge'].astype(str)
    #     # Aplica lambda para transformar o código do IBGE de 7 dígitos para 6 dígitos
    #     self.dados_lat_lon_goias['codigo_ibge'] = self.dados_lat_lon_goias['codigo_ibge'].map(lambda num: num[:6])
    #     self.dados_lat_lon_goias['codigo_ibge'] = self.dados_lat_lon_goias['codigo_ibge'].astype(int)
    #     return self.dados_lat_lon_goias
    
    # def merge_df_lt_dados_lat_lon_goias(self):
    #     '''Função para fazer o merge entre o dataframe de leitos e o dataframe de latitude e longitude dos municípios de Goiás'''
    #     self.df_lt_municipios_goias = pd.merge(self.df_lt, self.dados_lat_lon_goias, how='left', left_on=['CODUFMUN'], right_on=['codigo_ibge'])
    #     return self.df_lt_municipios_goias 
    