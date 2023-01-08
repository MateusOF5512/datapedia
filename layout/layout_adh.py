from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report

from plots.plots_adh import *


config={"displayModeBar": True,
        "displaylogo": False,
        'modeBarButtonsToRemove': ['zoom2d', 'toggleSpikelines',
                                   'pan2d', 'select2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d',
                                   'hoverClosestCartesian', 'hoverCompareCartesian']}



def atlas_municipio(df_atlas, atlas_tabela):
    if atlas_tabela == "📊 Dashboard":
        st.dataframe(df_atlas)

    elif atlas_tabela == "‍🔬 Laboratório":
        st.markdown("<h1 style='font-size:200%; text-align: center; color: #5B51D8; padding: 0px 0px;'" +
                    ">Tabela Interativa e Dinâmica</h1>",
                    unsafe_allow_html=True)
        st.text("")
        st.text("")

        selected_rows = agg_tabela(df_atlas, use_checkbox=True)

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
                                    options=["ano", "nome", "capital_uf", "nome_microrregiao",
                                             "nome_regiao","sigla_uf", "nome_uf"], index=4)
            with col2:
                df_x_bolha = df_atlas
                varx = st.selectbox('Coluna pro Eixo X:',
                                    df_x_bolha.columns.unique(), index=4, key=81)
            with col3:
                df_y_bolha = df_atlas
                vary = st.selectbox('Coluna pro Eixo Y:',
                                    df_y_bolha.columns.unique(), index=90, key=82)
            with col4:
                tipo1 = st.radio("Formato do Eixo Y:", options=["Total", "Média"], index=1, horizontal=True, key=3)

            fig2 = plot_bolha(df_atlas, tipo1, varx, vary, varz)
            st.plotly_chart(fig2, use_container_width=True)

            # DOWNLOAD E VISUALIZAÇÃO DOS DADOS SELECIONADOS ------------------------------------------------
            with st.expander("🔎️   Dados - Análise de Disperção"):
                if tipo1 == "Total":
                    df_bolha = df_atlas.groupby([varx])[vary].agg('sum').reset_index().sort_values(varx, ascending=True)
                    df_bolha.loc[:, vary] = df_bolha[vary].map('{:,.0f}'.format)
                elif tipo1 == "Média":
                    df_bolha = df_atlas.groupby([varx])[vary].agg('mean').reset_index().sort_values(varx, ascending=True)
                    df_bolha.loc[:, vary] = df_bolha[vary].map('{:,.0f}'.format)

                checkdf = st.checkbox('Visualizar Dados', key=70)
                if checkdf:
                    df_bolha = df_bolha[[varx, vary]]

                    st.markdown("<h3 style='font-size:150%; text-align: center; color: #5B51D8;'" +
                                "><i>" + tipo1 + "</i> de <i>" + vary + "</i> e <i>" + varx + "</i> por "+varz+" - TABELA RESUMIDA</h3>",
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
                df_x = df_atlas[["ano", "nome", "capital_uf", "nome_microrregiao","nome_regiao","sigla_uf", "nome_uf"]]
                var1 = st.selectbox('coluna pro Eixo X:', df_x.columns.unique(), index=0, key=78)
            with col2:
                df_y = df_atlas
                var2 = st.selectbox('Coluna paro Eixo Y:', df_y.columns.unique(), index=4, key=79)

            with col3:
                tipo = st.radio("Formato do Eixo Y:",
                                options=["Total dos Valores", "Média dos Valores"], horizontal=True, key=2)

            fig1 = bar_plot(df_atlas, var1, var2, tipo)
            st.plotly_chart(fig1, use_container_width=True)

            # DOWNLOAD E VISUALIZAÇÃO DOS DADOS SELECIONADOS ------------------------------------------------
            with st.expander("🔎️   Dados - Análise Comparativa"):
                if tipo == "Total dos Valores":
                    df_barra = df_atlas.groupby([var1])[var2].agg('sum').reset_index().sort_values(var1, ascending=True)
                    df_barra.loc[:, var2] = df_barra[var2].map('{:,.0f}'.format)
                elif tipo == "Média dos Valores":
                    df_barra = df_atlas.groupby([var1])[var2].agg('mean').reset_index().sort_values(var1, ascending=True)
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

    elif atlas_tabela == "🔎 Relatórios":

        text = """Para gerar os Relatórios utilizamos o pandas-profiling, que entrega todas as ferramentas necessárias para 
                uma análise profunda, rápida e simples dos dados. Gerando automaticamente relatórios personalizados para 
                cada variável no conjunto de dados, com estatística, gráficos, alertas, correlações e mais. 
                Para gerar esses Relatórios pode demorar uns segundos, dependendo da Tabela até minutos, 
                mas a demora vale a pena pela riqueza de informações, enquanto espera leia sobre suas funcionalidades:"""

        st.info(text)

        report = st.checkbox("Carregar Relatório dos Dados 🔎", key=76)

        if report:
            profile = ProfileReport(df_atlas, title="Relatório dos Dados", explorative=True)
            st_profile_report(profile)


    return None