# Bibliotecas
# Streamlit app para o projeto de leitos em Goiás
import streamlit as st
# Processamento dos dados - Pandas
import pandas as pd
# Visualização dos dados - Matplotlib e Seaborn
import matplotlib.pyplot as plt
import seaborn as sns
# Extrair dados de uma API
import json
import requests
# Visualização de mapas
import folium


def main():
    options = ['Projeto leitos Goiás', 'Referências']
    page_options = st.sidebar.selectbox('Escolha uma opção', options)
    
    if page_options == 'Projeto leitos Goiás':
        projeto()
    if page_options == 'Referências':
        referencias()

                
def referencias():
    st.markdown('''### Referências de dados e estudos que foram utilizados para o projeto.''')

    st.markdown('''
                Dados:  
                [Dados de leitos cadastrados no subsistema LT do sistema CNES](https://datasus.saude.gov.br/transferencia-de-arquivos)  
                
                [Dados de Latitude e Longitude de todos os municípios brasileiros](https://github.com/kelvins/Municipios-Brasileiros)  
                
                Estudos:  
                [Folium Heatmaps](https://blog.jovian.ai/interesting-heatmaps-using-python-folium-ee41b118a996)

                ''')
    
def projeto():
    
    st.title('A evolução da capacidade hospitalar durante a pandemia de Covid-19 em Goiás')
    st.write('Governo de Goiás mantém leitos instalados no período crítico da pandemia?')
    ### Segundo a OMS o início da pândemia por COVID-19 no Brasil foi dia 11 de março de 2020
    ### Ainda não houve declaração pela OMS quanto ao fim da pândemia

        
if __name__ == '__main__':
    main()
