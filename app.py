# Bibliotecas
# Streamlit app para o projeto de leitos em Goiás
import streamlit as st
from streamlit_folium import st_folium
# Dados class
from Dados import Dados

import plotly.express as px

def main():
    options = ['Projeto leitos Goiás', 'Referências']
    page_options = st.sidebar.selectbox('Escolha uma opção', options)
    
    if page_options == 'Projeto leitos Goiás':
        projeto()
    if page_options == 'Referências':
        referencias()

                
def referencias():
    st.markdown('''### Referências utilizadas para o projeto.''')

    st.markdown('''
                Dados:  
                [Dados de leitos cadastrados no subsistema LT do sistema CNES](https://datasus.saude.gov.br/transferencia-de-arquivos)  
                
                [Dados de Latitude e Longitude de todos os municípios brasileiros](https://github.com/kelvins/Municipios-Brasileiros)  
                
                [Malha de Goiás](https://servicodados.ibge.gov.br/api/v3/malhas/estados/GO?formato=application/vnd.geo+json)  
                
                
                Referências:  
                [Folium Heatmaps](https://blog.jovian.ai/interesting-heatmaps-using-python-folium-ee41b118a996)  
                
                [Notícia Governo de Goiás mantem leitos instalados no periodo critico da pandemia](https://www.saude.go.gov.br/noticias/16950-governo-de-goias-mantem-leitos-instalados-no-periodo-critico-da-pandemia)   
                
                [Cenário dos Hospitais no Brasil 2021-2022](http://cnsaude.org.br/wp-content/uploads/2022/07/CNSAUDE-FBH-CENARIOS-2022.pdf)  
                
                [Sobre Goiás - IBGE](https://www.ibge.gov.br/cidades-e-estados/go.html)

                ''')
    
def projeto():
    
    st.markdown('''## A evolução da capacidade hospitalar durante a pandemia de Covid-19 em Goiás''')
    st.markdown('''Governo de Goiás mantém **leitos instalados** no período crítico da pandemia?''')
    
    # Instanciando a classe Dados
    dados = Dados()

    #Métricas de Goiás Área e População
    st.subheader('Dados do Estado de Goiás [IBGE-2021]')

    col1, col2 = st.columns(2)
    with col1:
         st.metric('Área Territorial', '340.242,856 km²')
    with col2:
        st.metric('População estimada', '7.206.589 pessoas')
   
    # Mapa de Goiás
    st_folium(dados.mapa_estado_goias(), width=700, height=400)

    st.markdown('''### O início da pândemia por COVID-19 no Brasil foi dia 11 de março de 2020 (segundo a OMS)''')
    st.markdown('''Ainda não houve declaração pela OMS quanto ao fim da pândemia.''')
    st.subheader(' Leitos SUS e não SUS no tempo')

    # Line chart    
    
    # setando o index
    dados.dt_qt_leitos_sus_nsus.set_index('COMPETEN', inplace = True)           
    dados.dt_qt_leitos_sus_nsus.rename(columns={'QT_SUS': 'Leitos SUS', 'QT_NSUS': 'Leitos NÃO SUS'}, inplace=True)
    options = ["Leitos SUS", "Leitos NÃO SUS"]
    options_selected = st.multiselect("Selecione o tipo de leito", options,default= ["Leitos SUS", "Leitos NÃO SUS"])

    fig = px.line(dados.dt_qt_leitos_sus_nsus, y=options_selected)
    fig.update_layout(
        xaxis_title=' ',

        yaxis_title=' '
    )
    st.plotly_chart(fig, use_container_width=True)

if __name__ == '__main__':
    main()
