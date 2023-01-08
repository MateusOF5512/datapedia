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

def atlas():
    st.markdown("<h2 style='font-size:200%; text-align: center; color: #5B51D8; padding: 0px 0px;'" +
                ">Atlas do Desenvolvimento Humano - ADH</h2>",
                unsafe_allow_html=True)
    st.text("")
    st.text("")

    col1, col2, col3 = st.columns([20, 1, 20])
    with col1:
        atlas_tabela = st.radio("Tabelas da Base de Dados:",
                                options=["Início", "Municípios e Regiões", "Brasil"],
                                key=37, horizontal=True)
    with col2:
        st.text("")
    with col3:
        atlas_analise = st.radio("Tipo da analise:",
                                 options=["📊 Dashboard", "‍🔬 Laboratório", "🔎 Relatórios"], key=36, horizontal=True)
    st.markdown('---')
    st.text("")
    st.text("")

    return atlas_tabela, atlas_analise


def inicio_atlas():
    col1, col2, col3 = st.columns([1, 20, 1])
    with col1:
        st.text("")
    with col2:
        st.markdown("""
                        O Atlas do Desenvolvimento Humano no Brasil é um site que traz o Índice de 
                        Desenvolvimento Humano Municipal (IDHM) e outros 200 indicadores de demografia, 
                        educação, renda, trabalho, habitação e vulnerabilidade para os municípios brasileiros.
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
        st.markdown("Organização das Nações Unidas (ONU)")
    with col2:
        st.text("")
    with col3:
        st.markdown("<h3 style='font-size:130%; text-align: left; color: #5B51D8; padding: 0px 0px;'" +
                    ">Cobertura temporal:</h3>",
                    unsafe_allow_html=True)
        st.markdown("1991 - 2010")




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























