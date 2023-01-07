# Importação de Bibliotecas:
import streamlit as st
from outros.variaveis_folha import *
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode
from PIL import Image

from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report

from plots.ideb_brasil import *



def rodape1():
    st.markdown(html_rodape1, unsafe_allow_html=True)
    return None


config={"displayModeBar": True,
        "displaylogo": False,
        'modeBarButtonsToRemove': ['zoom2d', 'toggleSpikelines',
                                   'pan2d', 'select2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d',
                                   'hoverClosestCartesian', 'hoverCompareCartesian']}


def ideb_brasil(df, df_limpo, tab1A, tab2A, tab3A):

    with tab1A:
        col1, col2, col3 = st.columns([20, 1, 20])
        with col1:
            with st.expander("⚙️ Configurar Dados"):
                rede = df_limpo.rede.unique().tolist()
                selected_rede = st.multiselect("Filtre por Rede de Ensino:",
                                                options=rede, default=rede)

                ensino = df_limpo.ensino.unique().tolist()
                selected_ensino = st.multiselect("Filtre por Fase do Ensino:",
                                                options=ensino, default=ensino)

                slider1, slider2 = st.slider('Filtre por Ano', 2005, 2019, [2005, 2019], 2)
                mask_ano = (df_limpo['ano'] >= slider1) & (df_limpo['ano'] <= slider2)
        with col2:
            st.text("")
        with col3:
            with st.expander("⚙️ Configurar Dashbords"):
                st.text("opee")

        var1 = 'taxa_aprovacao'

        df_limpo = df_limpo[df_limpo.rede.isin(selected_rede)]
        df_limpo = df_limpo[df_limpo.ensino.isin(selected_ensino)]
        df_limpo = df_limpo.loc[mask_ano]

        fig_rede = barra_rede(df_limpo, var1)
        fig_ensino = barra_ensino(df_limpo, var1)
        fig_linha_rede = linha_rede(df_limpo, var1)
        fig_linha_ensino = linha_ensino(df_limpo, var1)
        fig_bolha_ensino = bolha_rede(df_limpo, var1)

        col1, col2, col3 = st.columns([20, 1, 20])
        with col1:
            st.markdown("<h3 style='font-size:150%; text-align: center; color: #5B51D8; padding: 10px 10px;'" +
                        ">Rede de Ensino por <i>"+var1+"</i> - Total</h3>",
                        unsafe_allow_html=True)
            st.plotly_chart(fig_rede, use_container_width=True)
        with col2:
            st.text("")
        with col3:
            st.markdown("<h3 style='font-size:150%; text-align: center; color: #5B51D8; padding: 10px 10px;'" +
                        ">Rede de Ensino por <i>"+var1+"</i> - Anual</h3>",
                        unsafe_allow_html=True)
            st.plotly_chart(fig_linha_rede, use_container_width=True)



        col1, col2, col3 = st.columns([20, 1, 20])
        with col1:
            st.markdown("<h3 style='font-size:150%; text-align: center; color: #5B51D8; padding: 10px 10px;'" +
                        ">Fase do Ensino por <i>"+var1+"</i> - Total</h3>",
                        unsafe_allow_html=True)
            st.plotly_chart(fig_ensino, use_container_width=True)
        with col2:
            st.text("")
        with col3:
            st.markdown("<h3 style='font-size:150%; text-align: center; color: #5B51D8; padding: 10px 10px;'" +
                        ">Fase do Ensino por <i>"+var1+"</i> - Anual</h3>",
                        unsafe_allow_html=True)
            st.plotly_chart(fig_linha_ensino, use_container_width=True)

        col1, col2, col3 = st.columns([20, 1, 20])
        with col1:
            st.markdown("<h3 style='font-size:150%; text-align: center; color: #5B51D8; padding: 10px 10px;'" +
                        ">Fase do Ensino por ideb e <i>" + var1 + "</i></h3>",
                        unsafe_allow_html=True)
            st.plotly_chart(fig_bolha_ensino, use_container_width=True)
        with col2:
            st.text("")
        with col3:
            st.markdown("<h3 style='font-size:150%; text-align: center; color: #5B51D8; padding: 10px 10px;'" +
                        ">Base de Dados</h3>",
                        unsafe_allow_html=True)
            agg_tabela(df_limpo, use_checkbox=False)


    with tab2A:
        st.markdown("<h1 style='font-size:200%; text-align: center; color: #5B51D8; padding: 0px 0px;'" +
                    ">Tabela Interativa e Dinâmica</h1>",
                    unsafe_allow_html=True)
        st.text("")
        st.text("")

        selected_rows = agg_tabela(df, use_checkbox=True)

        if len(selected_rows) == 0:
            # GRÁFICO DE BOLHO - ANÁLSIE DE DISPERÇÃO - PARTE 1 ----------------------------------------
            st.markdown("<h1 style='font-size:200%; text-align: center; color: #5B51D8;'" +
                        ">Análise de Disperção -  Gráfico de Bolha</h1>",
                        unsafe_allow_html=True)
            st.text("")
            st.text("")

            # CONFIGURAÇÃO PARA ANÁLISE E EXPLORAÇÃO
            col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
            with col1:
                varz = st.selectbox("Agrupamento dos dados:",
                                    options=["ano", "rede", 'ensino', 'anos_escolares'], index=1)
            with col2:
                df_x_bolha = df[['taxa_aprovacao', 'indicador_rendimento', 'nota_saeb_matematica',
                                 'nota_saeb_lingua_portuguesa', 'nota_saeb_media_padronizada',
                                 'ideb', 'projecao']]
                varx = st.selectbox('Coluna pro Eixo X:',
                                    df_x_bolha.columns.unique(), index=5, key=31)
            with col3:
                df_y_bolha = df[['taxa_aprovacao', 'indicador_rendimento', 'nota_saeb_matematica',
                                 'nota_saeb_lingua_portuguesa', 'nota_saeb_media_padronizada',
                                 'ideb', 'projecao']]
                vary = st.selectbox('Coluna pro Eixo Y:',
                                    df_y_bolha.columns.unique(), index=0, key=32)
            with col4:
                tipo = st.radio("Formato do Eixo Y:",
                                options=["Total", "Média"], key=33, horizontal=True)

            fig2 = plot_bolha(df, tipo, varx, vary, varz)
            st.plotly_chart(fig2, use_container_width=True)

            # DOWNLOAD E VISUALIZAÇÃO DOS DADOS SELECIONADOS ------------------------------------------------
            with st.expander("🔎️   Dados - Análise de Disperção"):
                if tipo == "Total":
                    df_bolha = df.groupby([varx])[vary].agg('sum').reset_index().sort_values(varx, ascending=True)
                    df_bolha.loc[:, vary] = df_bolha[vary].map('{:,.0f}'.format)
                elif tipo == "Média":
                    df_bolha = df.groupby([varx])[vary].agg('mean').reset_index().sort_values(varx, ascending=True)
                    df_bolha[vary] = df_bolha[vary].astype(int)
                    df_bolha.loc[:, vary] = df_bolha[vary].map('{:,.0f}'.format)

                checkdf = st.checkbox('Visualizar Dados', key=54)
                if checkdf:
                    df_bolha = df_bolha[[varx, vary]]

                    st.markdown("<h3 style='font-size:150%; text-align: center; color: #5B51D8;'" +
                                "><i>" + tipo + "</i> de <i>" + vary + "</i> por <i>" + varx + "</i> - TABELA RESUMIDA</h3>",
                                unsafe_allow_html=True)
                    agg_tabela(df_bolha, use_checkbox=True)

                df_bolha = df_bolha.to_csv(index=False).encode('utf-8')
                st.download_button(label="Download Dados", data=df_bolha,
                                   file_name="DataApp.csv", mime='text/csv')


            # GRÁFICO DE BARRA ´ANÁLISE COMPARATIVA - PARTE 2 ------------------------------------------------
            st.markdown("<h1 style='font-size:200%; text-align: center; color: #5B51D8;'" +
                        ">Análise Comparativa -  Gráfico de Barra</h1>",
                        unsafe_allow_html=True)
            st.text("")
            st.text("")

            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                df_x = df[['ano', 'rede', 'ensino', 'anos_escolares']]
                var1 = st.selectbox('coluna pro Eixo X:', df_x.columns.unique(), index=0, key=12)
            with col2:
                df_y = df[['taxa_aprovacao', 'indicador_rendimento', 'ideb', 'projecao']]
                var2 = st.selectbox('Coluna paro Eixo Y:', df_y.columns.unique(), index=0, key=11)

            with col3:
                tipo = st.radio("Formato do Eixo Y:",
                                options=["Total dos Valores", "Média dos Valores"], horizontal=True)


            fig1 = bar_plot(df, var1, var2, tipo)
            st.plotly_chart(fig1, use_container_width=True)

            # DOWNLOAD E VISUALIZAÇÃO DOS DADOS SELECIONADOS ------------------------------------------------
            with st.expander("🔎️   Dados - Análise Comparativa"):
                if tipo == "Total dos Valores":
                    df_barra = df.groupby([var1])[var2].agg('sum').reset_index().sort_values(var1, ascending=True)
                    df_barra.loc[:, var2] = df_barra[var2].map('{:,.0f}'.format)
                elif tipo == "Média dos Valores":
                    df_barra = df.groupby([var1])[var2].agg('mean').reset_index().sort_values(var1, ascending=True)
                    df_barra.loc[:, var2] = df_barra[var2].map('{:,.0f}'.format)

                checkdf = st.checkbox('Visualizar Dados', key=52)
                if checkdf:
                    df_barra = df_barra[[var1, var2]]

                    st.markdown("<h3 style='font-size:150%; text-align: center; color: #5B51D8;'" +
                                "><i>" + tipo + "</i> de <i>" + var2 + "</i> por <i>" + var1 + "</i> - TABELA RESUMIDA</h3>",
                                unsafe_allow_html=True)
                    agg_tabela(df_barra, use_checkbox=True)

                df_barra = df_barra.to_csv(index=False).encode('utf-8')
                st.download_button(label="Download Dados", data=df_barra,
                                   file_name="DataApp.csv", mime='text/csv')


            # GRÁFICO DE LINHA - ANÁLSIE TEMPORAL - PARTE 3 ----------------------------------------
            st.markdown("<h1 style='font-size:200%; text-align: center; color: #5B51D8;'" +
                        ">Análise Temporal -  Gráfico de Linha</h1>",
                        unsafe_allow_html=True)
            st.text("")
            st.text("")

            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                df_x = df[['ano', 'rede', 'ensino', 'anos_escolares']]
                varx3 = st.selectbox('Coluna pro Eixo X:', df_x.columns.unique(), index=0, key=14)
            with col2:
                df_y = df[['taxa_aprovacao', 'indicador_rendimento', 'ideb', 'projecao']]
                vary3 = st.selectbox('Coluna pro Eixo Y:', df_y.columns.unique(), index=0, key=15)

            with col3:
                tipo3 = st.radio("Formato do Eixo Y:",
                                 options=["Total dos Valores", "Média dos Valores"], horizontal=True, index=1, key=16)

            fig3 = plot_line(df, varx3, vary3, tipo3)
            st.plotly_chart(fig3, use_container_width=True)

            # DOWNLOAD E VISUALIZAÇÃO DOS DADOS SELECIONADOS ------------------------------------------------
            with st.expander("🔎️   Dados - Análise de Disperção"):
                if tipo3 == "Total dos Valores":
                    df_linha = df.groupby([varx3])[vary3].agg('sum').reset_index().sort_values(varx3, ascending=True)
                    df_linha.loc[:, vary3] = df_linha[vary3].map('{:,.0f}'.format)
                elif tipo3 == "Média dos Valores":
                    df_linha = df.groupby([varx3])[vary3].agg('mean').reset_index().sort_values(varx3, ascending=True)
                    df_linha.loc[:, vary3] = df_linha[vary3].map('{:,.0f}'.format)

                checkdf = st.checkbox('Visualizar Dados', key=53)
                if checkdf:
                    df_linha = df_linha[[varx3, vary3]]

                    st.markdown("<h3 style='font-size:150%; text-align: center; color: #5B51D8;'" +
                                "><i>" + tipo3 + "</i> de <i>" + vary3 + "</i> por <i>" + varx3 + "</i> - TABELA RESUMIDA</h3>",
                                unsafe_allow_html=True)
                    agg_tabela(df_linha, use_checkbox=True)

                df_linha = df_linha.to_csv(index=False).encode('utf-8')
                st.download_button(label="Download Dados", data=df_linha,
                                   file_name="DataApp.csv", mime='text/csv')

        elif len(selected_rows) != 0:
            st.text("oi")



    with tab3A:
        st.markdown("oie3")

        report = st.checkbox("Carregar Relatório dos Dados 🔎")

        if report:
            profile = ProfileReport(df, title="Relatório dos Dados", explorative=True)
            st_profile_report(profile)

    return None


def ideb_escolas(df_escolas, tab1A, tab2A, tab3A):
    with tab1A:
        st.dataframe(df_escolas)

    with tab2A:
        st.markdown("<h1 style='font-size:200%; text-align: center; color: #5B51D8; padding: 0px 0px;'" +
                    ">Tabela Interativa e Dinâmica</h1>",
                    unsafe_allow_html=True)
        st.text("")
        st.text("")

        selected_rows = agg_tabela(df_escolas, use_checkbox=True)

        if len(selected_rows) == 0:
            # GRÁFICO DE BOLHO - ANÁLSIE DE DISPERÇÃO - PARTE 1 ----------------------------------------
            st.markdown("<h1 style='font-size:200%; text-align: center; color: #5B51D8;'" +
                        ">Análise de Disperção -  Gráfico de Bolha</h1>",
                        unsafe_allow_html=True)
            st.text("")
            st.text("")

            # CONFIGURAÇÃO PARA ANÁLISE E EXPLORAÇÃO
            col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
            with col1:
                varz = st.selectbox("Agrupamento dos dados:",
                                    options=["ano", "sigla_uf", 'rede', 'ensino', 'anos_escolares'], index=1)
            with col2:
                df_x_bolha = df_escolas
                varx = st.selectbox('Coluna pro Eixo X:',
                                    df_x_bolha.columns.unique(), index=8, key=71)
            with col3:
                df_y_bolha = df_escolas
                vary = st.selectbox('Coluna pro Eixo Y:',
                                    df_y_bolha.columns.unique(), index=13, key=72)
            with col4:
                tipo = st.radio("Formato do Eixo Y:",
                                options=["Total", "Média"], key=73, horizontal=True)

            fig2 = plot_bolha(df_escolas, tipo, varx, vary, varz)
            st.plotly_chart(fig2, use_container_width=True)

            # DOWNLOAD E VISUALIZAÇÃO DOS DADOS SELECIONADOS ------------------------------------------------
            with st.expander("🔎️   Dados - Análise de Disperção"):
                if tipo == "Total":
                    df_bolha = df_escolas.groupby([varx])[vary].agg('sum').reset_index().sort_values(varx, ascending=True)
                    df_bolha.loc[:, vary] = df_bolha[vary].map('{:,.0f}'.format)
                elif tipo == "Média":
                    df_bolha = df_escolas.groupby([varx])[vary].agg('mean').reset_index().sort_values(varx, ascending=True)
                    df_bolha.loc[:, vary] = df_bolha[vary].map('{:,.0f}'.format)

                checkdf = st.checkbox('Visualizar Dados', key=70)
                if checkdf:
                    df_bolha = df_bolha[[varx, vary]]

                    st.markdown("<h3 style='font-size:150%; text-align: center; color: #5B51D8;'" +
                                "><i>" + tipo + "</i> de <i>" + vary + "</i> por <i>" + varx + "</i> - TABELA RESUMIDA</h3>",
                                unsafe_allow_html=True)
                    agg_tabela(df_bolha, use_checkbox=True)

                df_bolha = df_bolha.to_csv(index=False).encode('utf-8')
                st.download_button(label="Download Dados", data=df_bolha,
                                   file_name="DataApp.csv", mime='text/csv')


            # GRÁFICO DE BARRA ´ANÁLISE COMPARATIVA - PARTE 2 ------------------------------------------------
            st.markdown("<h1 style='font-size:200%; text-align: center; color: #5B51D8;'" +
                        ">Análise Comparativa -  Gráfico de Barra</h1>",
                        unsafe_allow_html=True)
            st.text("")
            st.text("")

            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                df_x = df_escolas
                var1 = st.selectbox('coluna pro Eixo X:', df_x.columns.unique(), index=2, key=78)
            with col2:
                df_y = df_escolas
                var2 = st.selectbox('Coluna paro Eixo Y:', df_y.columns.unique(), index=8, key=79)

            with col3:
                tipo = st.radio("Formato do Eixo Y:",
                                options=["Total dos Valores", "Média dos Valores"], horizontal=True)

            fig1 = bar_plot(df_escolas, var1, var2, tipo)
            st.plotly_chart(fig1, use_container_width=True)

            # DOWNLOAD E VISUALIZAÇÃO DOS DADOS SELECIONADOS ------------------------------------------------
            with st.expander("🔎️   Dados - Análise Comparativa"):
                if tipo == "Total dos Valores":
                    df_barra = df_escolas.groupby([var1])[var2].agg('sum').reset_index().sort_values(var1, ascending=True)
                    df_barra.loc[:, var2] = df_barra[var2].map('{:,.0f}'.format)
                elif tipo == "Média dos Valores":
                    df_barra = df_escolas.groupby([var1])[var2].agg('mean').reset_index().sort_values(var1, ascending=True)
                    df_barra.loc[:, var2] = df_barra[var2].map('{:,.0f}'.format)

                checkdf = st.checkbox('Visualizar Dados', key=58)
                if checkdf:
                    df_barra = df_barra[[var1, var2]]

                    st.markdown("<h3 style='font-size:150%; text-align: center; color: #5B51D8;'" +
                                "><i>" + tipo + "</i> de <i>" + var2 + "</i> por <i>" + var1 + "</i> - TABELA RESUMIDA</h3>",
                                unsafe_allow_html=True)
                    agg_tabela(df_barra, use_checkbox=True)

                df_barra = df_barra.to_csv(index=False).encode('utf-8')
                st.download_button(label="Download Dados", data=df_barra,
                                   file_name="DataApp.csv", mime='text/csv')

    with tab3A:
        report = st.checkbox("Carregar Relatório dos Dados 🔎", key=76)

        if report:
            profile = ProfileReport(df_escolas, title="Relatório dos Dados", explorative=True)
            st_profile_report(profile)


    return None
