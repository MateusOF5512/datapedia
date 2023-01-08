# BIBLIOTECAS USADAS
from layout.ideb_brasil import *
from layout.layout_adh import *
from plots.ideb_brasil import *
from plots.plots_adh import *
import streamlit as st


# CONFIGURAÇÕES DE VISUALIZAÇÃO DO STREAMLIT ----------------------------------------------
st.set_page_config(page_title="AEDA", layout="wide")

st.markdown(""" <style>
        footer {visibility: hidden;}
        </style> """, unsafe_allow_html=True)

# CARREGANDO BASE DE DADOS -----------------------------------------------------------------
path1 = 'data/brasil.csv.csv'
path2 = 'data/IDEB_BRASIL_TRATADO.csv'

path3 = 'data/ideb-escolas.csv'

path4 = 'data/ADH.csv'

df = read_csv(path1)
df_limpo = read_csv(path2)
df_escolas = read_csv(path3)
df_atlas = read_csv(path4)


df_limpo = tratamento(df_limpo)
#df_escolas_ = tratamento(df_escolas)

# APLICAÇÃO ------------------------------------------------------------------------------
st.markdown("<h1 style='font-size:250%; text-align: center; color: #5B51D8; padding: 0px 0px;'" +
                ">Datapédia</h1>",
                unsafe_allow_html=True)
st.markdown("<h2 style='font-size:200%; text-align: center; color: #5B51D8; padding: 0px 0px;'" +
                ">Sua Análise Exploratória de Base de Dados</h2>",
                unsafe_allow_html=True)

st.text("")
st.text("")
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs([
    "🐣 Introdução",
    "🎓 Educação", "🌱 Meio Ambiente", "👩‍🌾 Agropecuária",
    "🏳️‍🌈 Diversidade e Inclusão", "💲 Economia", "⚡️Energia",
    "⚽️Esportes", "Governo", "👩‍💻 Técnologia e Inovação"])


with tab1:
    st.text("")
    st.text("")
    col1, col2, col3 = st.columns([1, 20, 1])
    with col1:
        st.text("")
    with col2:
        intro()
    with col3:
        st.text("")

with tab2:
    educacao = st.selectbox('Selecione a Base de Dados:',
                            ["Índice de Desenvolvimento da Educação Básica - IDEB",
                             "Atlas do Desenvolvimento Humano (ADH)",
                             "Censo Escolar - INEP"])
    st.markdown('---')
    if educacao == "Índice de Desenvolvimento da Educação Básica - IDEB":

        ideb_tabela, ideb_analise = ideb()

        if ideb_tabela == 'Início':
            #inicio_ideb(ideb_analise)
            st.text("")

        elif ideb_tabela == 'Brasil':
            ideb_brasil(df, df_limpo, ideb_analise)

        elif ideb_tabela == 'Escolas':
            ideb_escolas(df_escolas, ideb_analise)

        elif ideb_tabela == 'Municipios e Regiões':
            st.text("Ainda nada...")

with tab3:
    meioambiente = st.selectbox('Selecione a Base de Dados:',
                            ["Banco de Dados de Queimadas",
                             "MapBiomas Estatísticas",
                             "Emissões de gases de efeito estufa no Brasil"])
    st.markdown("""---""")

with tab4:
    agropecuaria = st.selectbox('Selecione a Base de Dados:',
                                ["Censo Agropecuário - MAPA",
                                 "AGROFIT - MAPA",
                                 "Comércio Exterior do Agronegócio Brasileiro - IBGE"])
    st.markdown("""---""")

with tab5:
    diversidade = st.selectbox('Selecione a Base de Dados:',
                                ["Terras Indígenas - Sistema Indigenista de Informações - FUNAI",
                                 "Relatório LGBTQI - Grupo Gay da Bahia",
                                 "Pesquisa Online Sobre a Comunidade LGBT - FRA"])
    st.markdown("""---""")

with tab6:
    economia = st.selectbox('Selecione a Base de Dados:',
                               ["Atlas do Desenvolvimento Humano - ONU",
                                "Relação Anual de Informações Sociais - ME",
                                "Cadastro Geral de Empregados e Desempregados - ME"])
    st.markdown("""---""")
    if economia == "Atlas do Desenvolvimento Humano - ONU":

        atlas_tabela, atlas_analise = atlas()

        if atlas_tabela == 'Início':
            inicio_atlas()

        elif atlas_tabela == 'Municípios e Regiões':
            atlas_municipio(df_atlas, atlas_analise)

        elif atlas_tabela == 'Brasil':
            st.text("Ainda pouco...")


with tab7:
    energia = st.selectbox('Selecione a Base de Dados:',
                            ["Global Atlas for Renewable Energy - IRENA"])
    st.markdown("""---""")

with tab8:
    esportes = st.selectbox('Selecione a Base de Dados:',
                            ["Dados históricos das Olimpíadas - Kaggle",
                             "Futebol Brasileiro - CBF"])
    st.markdown("""---""")

with tab9:
    economia = st.selectbox('Selecione a Base de Dados:',
                            ["Cargos comissionados e funções gratificadas - ME",
                             "Pesquisa de Informações Básicas Estaduais - IBGE",
                             "Auxílio Emergencial - MC"])
    st.markdown("""---""")

with tab10:
    economia = st.selectbox('Selecione a Base de Dados:',
                            ["Censo Escolar - INEP",
                             "Bolsas - Coordenação de Aperfeiçoamento de Pessoal de Nível Superior - CAPES)",
                             "Acessos de banda larga fixa no Brasil - Anatel"])
    st.markdown("""---""")




