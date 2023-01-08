
import streamlit as st
import pandas as pd
import numpy as np

from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from wordcloud import STOPWORDS


from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode


# CARREGANDO OS DADOS:

@st.cache(allow_output_mutation=True)
def read_csv(path):
    df = pd.read_csv(path)
    return df


def tratamento(df):
    df = df.drop(['1'], axis=1)

    conditions = [(df['anos_escolares'] == 'iniciais (1-5)'),
                  (df['anos_escolares'] == 'finais (6-9)'),
                  (df['anos_escolares'] == 'todos (1-4)')]
    values = ['fundamental1', 'fundamental2', 'Médio']
    df['ensino'] = np.select(conditions, values)

    return df



def intro():
    st.markdown("<h2 style='font-size:150%; text-align: center; color: #5B51D8; padding: 0px 0px;'" +
                ">Sua primeira vez aqui? Conheça mais sobre o Datapédia!</h2>",
                unsafe_allow_html=True)
    st.text("")
    st.text("")
    st.markdown("""
            Você já ouviu falar no termo democratização de dados? Esse é um conceito inovador, 
            que defende que a população deve ter capacidade de acessar as informações sobre si. 
            Seu objetivo é permitir que qualquer um, por menos especialista que seja, possa coletar e analisar 
            dados sem precisar da ajuda de terceiros. 

            É um movimento que vem ganhando força a partir de 2010 e diversos Governos e Empresas 
            começam aderir, mas não de forma simplificada e unificada, hoje em dia é possível encontrar 
            sem muita dificuldade diversas bases de dados, públicos e privados, mas apesar dos dados 
            estarem disponíveis na Web para sua coleta e análise, a maioria dos arquivos estão em formatos complexos e
            tamanhos gigantescos, tornando-os inacessíveis para população na pratica.


            Com isso surge a Datapédia, aplicação para Analise Exploratória de Base de Dados, 
            """)

    return None


def ideb():

    col1, col2, col3 = st.columns([20, 1, 20])
    with col1:
        ideb_tabela = st.radio("Selecione Tabelas da Base de Dados:",
                               options=["Início", "Brasil", "Escolas", "Municipios e Regiões"], key=40,
                               horizontal=True)
    with col2:
        st.text("")
    with col3:
        ideb_analise = st.radio("Selecione o Tipo da Analise:",
                                options=["📊 Dashboard", "‍🔬 Laboratório", "🔎 Relatórios"], key=39, horizontal=True)

    st.markdown('---')
    st.markdown("<h2 style='font-size:200%; text-align: center; color: #5B51D8; padding: 0px 0px;'" +
                ">Índice de Desenvolvimento da Educação Básica - IDEB</h2>",
                unsafe_allow_html=True)

    st.markdown('---')
    st.text("")

    return ideb_tabela, ideb_analise

def inicio_ideb():
    col1, col2, col3 = st.columns([1, 20, 1])
    with col1:
        st.text("")
    with col2:
        st.markdown("""
                    O Índice de Desenvolvimento da Educação Básica (Ideb) foi criado em 2007 e reúne, 
                    em um só indicador, os resultados de dois conceitos igualmente importantes para a 
                    qualidade da educação: o fluxo escolar e as médias de desempenho nas avaliações.
                     O Ideb agrega ao enfoque pedagógico dos resultados das avaliações em larga escala 
                    do Inep a possibilidade de resultados sintéticos, facilmente assimiláveis, 
                    e que permitem traçar metas de qualidade educacional para os sistemas. 
                     """)

    with col3:
        st.text("")

    st.text("")
    st.text("")

    col1, col2, col3 = st.columns([20, 1, 20])
    with col1:
        st.markdown("<h3 style='font-size:130%; text-align: left; color: #5B51D8; padding: 0px 0px;'" +
                    ">Organização:</h3>",
                    unsafe_allow_html=True)
        st.markdown("Instituto Nacional de Estudos e Pesquisas Educacionais (Inep)")
    with col2:
        st.text("")
    with col3:
        st.markdown("<h3 style='font-size:130%; text-align: left; color: #5B51D8; padding: 0px 0px;'" +
                    ">Cobertura temporal:</h3>",
                    unsafe_allow_html=True)
        st.markdown("2005 - 2021")

    return None



def bar_plot(df, var1, var2, tipo):

    if tipo == 'Total dos Valores':
        df = df.groupby(var1).agg('sum').reset_index()

    elif tipo == 'Média dos Valores':
        df = df.groupby(var1).agg('mean').reset_index()

    values = df[var1].unique()
    y = df[var2]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=values, y=y, name=tipo,
        hovertemplate="</br><b>"+var1+":</b> %{x}" +
                      "</br><b>"+var2+":</b> %{y:,.0f}",
        textposition='none', marker_color='#E1306C'))
    fig.update_layout(
        paper_bgcolor="#F8F8FF", plot_bgcolor="#F8F8FF", font={'color': "#000000", 'family': "sans-serif"},
        height=300, margin=dict(l=20, r=20, b=20, t=20), autosize=False, hovermode="x")
    fig.update_yaxes(
        title_text="Eixo Y: "+var2, title_font=dict(family='Sans-serif', size=18),
        tickfont=dict(family='Sans-serif', size=12), nticks=7, showgrid=True, gridwidth=0.5, gridcolor='#D3D3D3')

    fig.update_xaxes(
        title_text="Eixo X: "+var1, title_font=dict(family='Sans-serif', size=18),
        tickfont=dict(family='Sans-serif', size=12), nticks=20, showgrid=False)

    return fig


def agg_tabela(df, use_checkbox):

    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination(enabled=True)
    gb.configure_default_column(groupable=True, value=True, enableRowGroup=True,
                                    aggFunc="sum", editable=True)
    gb.configure_selection(use_checkbox=use_checkbox, selection_mode='multiple')
    gb.configure_side_bar()
    gridoptions = gb.build()
    df_grid = AgGrid(df, gridOptions=gridoptions, enable_enterprise_modules=True,
                     update_mode=GridUpdateMode.SELECTION_CHANGED, height=300, width='100%')
    selected_rows = df_grid["selected_rows"]
    selected_rows = pd.DataFrame(selected_rows)

    return selected_rows


def plot_bolha(df, tipo, varx, vary, varz):

    fig = go.Figure()
    if tipo == "Total":
        df_gp = df.groupby(varz).agg('sum').reset_index()
        fig.add_trace(go.Scatter(x=df_gp[varx], y=df_gp[vary], customdata=df_gp[varz],
                                 mode='markers', name='',
                                 hovertemplate="</br><b>"+varz+"</b> %{customdata}" +
                                               "</br><b>"+varx+":</b> %{x:,.0f}" +
                                               "</br><b>"+vary+":</b> %{y:,.0f}",
                                 marker=dict(
                                     size=50,
                                     color=(df_gp[vary] + df_gp[varx] / 2),
                                     colorscale='Portland',
                                     showscale=True)
                                 ))
    elif tipo == "Média":
        df_gp = df.groupby(varz).agg('mean').reset_index()
        fig.add_trace(go.Scatter(x=df_gp[varx], y=df_gp[vary], customdata=df_gp[varz],
                                 mode='markers', name='',
                                 hovertemplate="</br><b>Agrupamento:</b> %{customdata}" +
                                               "</br><b>Eixo X:</b> %{x:,.0f}" +
                                               "</br><b>Eixo Y:</b> %{y:,.0f}",
                                 marker=dict(
                                     size=50,
                                     color=(df_gp[vary] + df_gp[varx] / 2),
                                     colorscale='Portland',
                                     showscale=True)
                                 ))


    fig.update_layout(
        paper_bgcolor="#F8F8FF", plot_bgcolor="#F8F8FF", font={'color': "#000000", 'family': "sans-serif"},
        height=300, margin=dict(l=20, r=20, b=20, t=20))
    fig.update_xaxes(
        title_text="Eixo X: "+varx, title_font=dict(family='Sans-serif', size=18), zeroline=False,
        tickfont=dict(family='Sans-serif', size=12), nticks=7, showgrid=True, gridwidth=0.8, gridcolor='#D3D3D3')
    fig.update_yaxes(
        title_text="Eixo Y: "+vary, title_font=dict(family='Sans-serif', size=18), zeroline=False,
        tickfont=dict(family='Sans-serif', size=12), nticks=7, showgrid=True, gridwidth=0.8, gridcolor='#D3D3D3')

    return fig

def plot_line(df, varx, vary, tipo):
    fig = go.Figure()
    if tipo == "Total dos Valores":
        df_temp = df.groupby([varx]).agg('sum').reset_index()

        fig.add_trace(go.Scatter(
            x=df_temp[varx], y=df_temp[vary],
            mode='lines', hovertemplate=None, line=dict(width=3, color='#C13584')))

    elif tipo == "Média dos Valores":
        df_temp = df.groupby([varx]).agg('mean').reset_index()

        fig.add_trace(go.Scatter(
            x=df_temp[varx], y=df_temp[vary],
            mode='lines', hovertemplate=None, line=dict(width=3, color='#F56040')))

    fig.update_layout(
        paper_bgcolor="#F8F8FF", plot_bgcolor="#F8F8FF", font={'color': "#000000", 'family': "sans-serif"},
        height=300, hovermode="x unified", margin=dict(l=10, r=10, b=20, t=20))
    fig.update_xaxes(
        title_text="Eixo X: "+varx, title_font=dict(family='Sans-serif', size=18),
        tickfont=dict(family='Sans-serif', size=12),  showgrid=False, rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=5, label="5D", step="day", stepmode="backward"),
                dict(count=15, label="15D", step="day", stepmode="backward"),
                dict(count=1, label="1M", step="month", stepmode="backward"),
                dict(count=2, label="2M", step="month", stepmode="backward"),
                dict(label="TUDO", step="all")
            ])
        )
    )
    fig.update_yaxes(
        title_text="Eixo Y: "+vary, title_font=dict(family='Sans-serif', size=18),
        tickfont=dict(family='Sans-serif', size=12), nticks=7, showgrid=True, gridwidth=0.5, gridcolor='#D3D3D3')

    return fig



##################################################################################################


def barra_rede(df, var1):
    df = df.groupby('rede').agg('sum').reset_index().sort_values(by=var1, ascending=False)

    x = df['rede'].unique()
    y = df[var1]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name='', x=x, y=y,
        hovertemplate="</br><b>Rede:</b> %{x}" +
                      "</br><b>Indicador:</b> %{y}",
        textposition='none', marker_color='#E1306C'
    ))

    fig.update_layout(
        paper_bgcolor="#F8F8FF", plot_bgcolor="#F8F8FF", font={'color': "#000000", 'family': "sans-serif"},
        legend=dict(font_size=11, orientation="h", yanchor="top", y=1.20, xanchor="center", x=0.5),
        height=220, barmode='stack', margin=dict(l=1, r=10, b=25, t=10), autosize=True, hovermode="x")
    fig.update_yaxes(
        title_text=var1, title_font=dict(family='Sans-serif', size=12),
        tickfont=dict(family='Sans-serif', size=9), nticks=7, showgrid=True, gridwidth=0.5, gridcolor='#D3D3D3')

    fig.update_xaxes(
        tickfont=dict(family='Sans-serif', size=9), nticks=20, showgrid=False)

    return fig


def barra_ensino(df, var1):
    df = df.groupby('ensino').agg('sum').reset_index().sort_values(by=var1, ascending=False)

    x = df['ensino'].unique()
    y = df[var1]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name='', x=x, y=y,
        hovertemplate="</br><b>Ensino:</b> %{x}" +
                      "</br><b>Indicador:</b> %{y}",
        textposition='none', marker_color='#E1306C'
    ))

    fig.update_layout(
        paper_bgcolor="#F8F8FF", plot_bgcolor="#F8F8FF", font={'color': "#000000", 'family': "sans-serif"},
        legend=dict(font_size=11, orientation="h", yanchor="top", y=1.20, xanchor="center", x=0.5),
        height=220, barmode='stack', margin=dict(l=1, r=10, b=25, t=10), autosize=True, hovermode="x")
    fig.update_yaxes(
        title_text=var1, title_font=dict(family='Sans-serif', size=12),
        tickfont=dict(family='Sans-serif', size=9), nticks=7, showgrid=True, gridwidth=0.5, gridcolor='#D3D3D3')

    fig.update_xaxes(
        tickfont=dict(family='Sans-serif', size=9), nticks=20, showgrid=False)

    return fig


def linha_rede(df, var1):
    df = df.groupby(['ano', 'rede']).agg('sum').reset_index()
    x = df.groupby('ano').agg('sum').reset_index()
    y_pr = df[df['rede'] == 'privada']
    y_pu = df[df['rede'] == 'publica']
    y_es = df[df['rede'] == 'estadual']
    y_mu = df[df['rede'] == 'municipal']

    figB2 = go.Figure()
    figB2.add_trace(go.Scatter(
        x=x['ano'], y=y_pr[var1],
        name='privada', mode='lines', hovertemplate=None,
        line=dict(width=2, color='#e22c2c')))

    figB2.add_trace(go.Scatter(
        x=x['ano'], y=y_es[var1],
        name='estadual', mode='lines', hovertemplate=None,
        line=dict(width=2, color='#2ce22c')))

    figB2.add_trace(go.Scatter(
        x=x['ano'], y=y_pu[var1],
        name='publica', mode='lines', hovertemplate=None,
        line=dict(width=2, color='#8a2be2')))

    figB2.add_trace(go.Scatter(
        x=x['ano'], y=y_mu[var1],
        name='municipal', mode='lines', hovertemplate=None,
        line=dict(width=2, color='#e2872c')))

    figB2.update_layout(
        paper_bgcolor="#F8F8FF", plot_bgcolor="#F8F8FF", font={'color': "#000000", 'family': "sans-serif"},
        legend=dict(font_size=12, orientation="h", yanchor="top", y=1.40, xanchor="left", x=0.06),
        height=220, hovermode="x unified", margin=dict(l=1, r=1, b=1, t=1))
    figB2.update_xaxes(
        rangeslider_visible=False, showgrid=False, nticks=13)
    figB2.update_yaxes(
        title_text="Número de Interações", title_font=dict(family='Sans-serif', size=12),
        tickfont=dict(family='Sans-serif', size=9), nticks=7, showgrid=True, gridwidth=0.5, gridcolor='#D3D3D3')

    return figB2


def linha_ensino(df, var1):
    df = df.groupby(['ano', 'ensino']).agg('sum').reset_index()
    x = df.groupby('ano').agg('sum').reset_index()
    y_f1 = df[df['ensino'] == 'fundamental1']
    y_f2 = df[df['ensino'] == 'fundamental2']
    y_md = df[df['ensino'] == 'Médio']

    figB2 = go.Figure()
    figB2.add_trace(go.Scatter(
        x=x['ano'], y=y_f1[var1],
        name='Fundamental1', mode='lines', hovertemplate=None,
        line=dict(width=2, color='#e22c2c')))

    figB2.add_trace(go.Scatter(
        x=x['ano'], y=y_f2[var1],
        name='Fundamental2', mode='lines', hovertemplate=None,
        line=dict(width=2, color='#2ce22c')))

    figB2.add_trace(go.Scatter(
        x=x['ano'], y=y_md[var1],
        name='Médio', mode='lines', hovertemplate=None,
        line=dict(width=2, color='#e2872c')))

    figB2.update_layout(
        paper_bgcolor="#F8F8FF", plot_bgcolor="#F8F8FF", font={'color': "#000000", 'family': "sans-serif"},
        legend=dict(font_size=12, orientation="h", yanchor="top", y=1.40, xanchor="left", x=0.06),
        height=220, hovermode="x unified", margin=dict(l=1, r=1, b=1, t=1))
    figB2.update_xaxes(
        rangeslider_visible=False, showgrid=False, nticks=13)
    figB2.update_yaxes(
        title_text="Número de Interações", title_font=dict(family='Sans-serif', size=12),
        tickfont=dict(family='Sans-serif', size=9), nticks=7, showgrid=True, gridwidth=0.5, gridcolor='#D3D3D3')

    return figB2



def plot_line(df, varx, vary, tipo):
    fig = go.Figure()
    if tipo == "Total dos Valores":
        df_temp = df.groupby([varx]).agg('sum').reset_index()

        fig.add_trace(go.Scatter(
            x=df_temp[varx], y=df_temp[vary],
            mode='lines', hovertemplate=None, line=dict(width=3, color='#C13584')))

    elif tipo == "Média dos Valores":
        df_temp = df.groupby([varx]).agg('mean').reset_index()

        fig.add_trace(go.Scatter(
            x=df_temp[varx], y=df_temp[vary],
            mode='lines', hovertemplate=None, line=dict(width=3, color='#F56040')))

    fig.update_layout(
        paper_bgcolor="#F8F8FF", plot_bgcolor="#F8F8FF", font={'color': "#000000", 'family': "sans-serif"},
        height=300, hovermode="x unified", margin=dict(l=10, r=10, b=20, t=20))
    fig.update_xaxes(
        title_text="Eixo X: "+varx, title_font=dict(family='Sans-serif', size=18),
        tickfont=dict(family='Sans-serif', size=12),  showgrid=False, rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=5, label="5D", step="day", stepmode="backward"),
                dict(count=15, label="15D", step="day", stepmode="backward"),
                dict(count=1, label="1M", step="month", stepmode="backward"),
                dict(count=2, label="2M", step="month", stepmode="backward"),
                dict(label="TUDO", step="all")
            ])
        )
    )
    fig.update_yaxes(
        title_text="Eixo Y: "+vary, title_font=dict(family='Sans-serif', size=18),
        tickfont=dict(family='Sans-serif', size=12), nticks=7, showgrid=True, gridwidth=0.5, gridcolor='#D3D3D3')

    return fig



def bolha_rede(df, var1):

    fig = go.Figure()
    df_gp = df.groupby('rede').agg('sum').reset_index()
    fig.add_trace(go.Scatter(x=df_gp['ideb'], y=df_gp[var1], customdata=df_gp['rede'],
                             mode='markers', name='',
                             hovertemplate="</br><b>Agrupamento:</b> %{customdata}" +
                                           "</br><b>ideb:</b> %{x:,.0f}" +
                                           "</br><b>"+var1+":</b> %{y:,.0f}",
                             marker=dict(
                                 size=50,
                                 color=(df_gp[var1]),
                                 colorscale='Portland',
                                 showscale=True)
                             ))


    fig.update_layout(
        paper_bgcolor="#F8F8FF", plot_bgcolor="#F8F8FF", font={'color': "#000000", 'family': "sans-serif"},
        height=300, margin=dict(l=20, r=20, b=20, t=20))
    fig.update_xaxes(
        title_text="ideb", title_font=dict(family='Sans-serif', size=18), zeroline=False,
        tickfont=dict(family='Sans-serif', size=12), nticks=7, showgrid=True, gridwidth=0.8, gridcolor='#D3D3D3')
    fig.update_yaxes(
        title_text="taxa_aprovacao", title_font=dict(family='Sans-serif', size=18), zeroline=False,
        tickfont=dict(family='Sans-serif', size=12), nticks=7, showgrid=True, gridwidth=0.8, gridcolor='#D3D3D3')

    return fig






