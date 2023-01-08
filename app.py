# Bibliotecas
# Streamlit app para o projeto de leitos em Goiás
import streamlit as st
# Dados class
from Dados import Dados


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
                
                
                Estudos:  
                [Folium Heatmaps](https://blog.jovian.ai/interesting-heatmaps-using-python-folium-ee41b118a996)  
                
                [Notícia Governo de Goiás mantem leitos instalados no periodo critico da pandemia](https://www.saude.go.gov.br/noticias/16950-governo-de-goias-mantem-leitos-instalados-no-periodo-critico-da-pandemia)   
                
                [Cenário dos Hospitais no Brasil 2021-2022](http://cnsaude.org.br/wp-content/uploads/2022/07/CNSAUDE-FBH-CENARIOS-2022.pdf)

                ''')
    
def projeto():
    
    st.markdown('''### A evolução da capacidade hospitalar durante a pandemia de Covid-19 em Goiás''')
    st.write('Governo de Goiás mantém leitos instalados no período crítico da pandemia?')
    ### Segundo a OMS o início da pândemia por COVID-19 no Brasil foi dia 11 de março de 2020
    ### Ainda não houve declaração pela OMS quanto ao fim da pândemia

    # Instanciando a classe Dados
    dados = Dados()
    
    # Transformando os dados
    dados.transform_competen_to_datetime()
    
    # Criar do dataframe com os dados de leitos
    dados.create_df_leitos_sus_nsus_goias()
    
    # Plotar os dados de leitos com lineplot do seaborn
    #dados.generate_lineplot_qt_leitos_sus_nsus()
    
    st.line_chart(dados.df_leitos_sus_nsus_goias)
    # Dados de leitos cadastrados no subsistema LT do sistema CNES - SUS e NÃO SUS
        
if __name__ == '__main__':
    main()
