from PIL import Image

# CAMINHO PARA OS DADOS ----------------------------------------------------------------

path_posts = "data/df150-folhadespaulo-tratado.csv"
#path_comentarios = "instagram_allcomments.csv"

path_globo = "data/df150-globo-tratado.csv"

path_estadao = "data/df150-estadao-tratado.csv"

path_uol = "data/df150-uol-tratado.csv"

path_cnn = "data/df150-cnn-tratado.csv"

path_choquei = "data/df150-choquei-tratado.csv"
path_todos = "data/portais_dados.csv"

# - TOPO E RODAPÉ ------------------------------------------------------------------------
html_title1="""
<h1 style="font-size:200%; color:#5B51D8; font-family:sans-serif; text-align:center"
>Data App - Instagram Monitore<br>
 <h2 style="font-size:150%; color:#5B51D8;font-family:sans-serif; text-align:center; "
 >Publicações dos maiores Instagrans de Notícias do Brasil</h2><br>
 <hr style= "display: block;
  margin-top: 0.5em;
  margin-bottom: 0.5em;
  margin-left: auto;
  margin-right: auto;
  border-style: inset;
  border-width: 1.5px;"></h1>
"""

html_title2="""
<h1 style="font-size:250%; color:#5B51D8; font-family:sans-serif;
            text-align:center; ">Data App - Monitor Desenvolvido</h1>
<h2 style="font-size:150%; color:#5B51D8; font-family:sans-serif;
            text-align:center; ">Dados: Publicações dos 10 maiores Instagrans de Notícias</h2>
"""

html_rodape1="""
<hr style= "display: block;
  margin-top: 0.5em;
  margin-bottom: 0.5em;
  margin-left: auto;
  margin-right: auto;
  border-style: inset;
  border-width: 1.5px;">
  <p style="color:Gainsboro; text-align: center;">Versão Beta 0.0.4</p>
"""


html_rodape2="""
<hr style= "display: block;
  margin-top: 0.5em;
  margin-bottom: 0.5em;
  margin-left: auto;
  margin-right: auto;
  border-style: inset;
  border-width: 1.5px;">
  <p style="color:Gainsboro; text-align: center;">Última Atualização dos Dados: 29/11/2022 - 22:00</p>
"""


# - PARTE 1 ------------------------------------------------------------------
## 1.1 - Número de Doses & Vacinas Aplicadas:
html_subheader_11="""
<div class="card">
  <div class="card-body" style="border-radius: 50px 50px 50px 50px; background: #5B51D8; 
                                border:solid; border-color: black; border-width: 2px 2px 2px 2px;
                                padding-top: 1px; padding-right: 25px; padding-bottom: 1px; padding-left: 25px; 
                                width: 100%; height: 60px;">
    <h3 class="card-title" style="background-color:#5B51D8; color:#F5F5F5; 
                                  font-family:sans-serif; text-align: center; 
                                  padding-top: 20px; padding-right: 1px; padding-bottom: 0px; padding-left: 1px;
                                  font-size:150%;" 
                                  >Monitoramento das Publicações</h3>
  </div>
"""

html_header_10="""
<div class="card">
  <div class="card-body">
    <h2 class="card-title" style="color:#5B51D8; font-family:sans-serif; 
                                  text-align: center; padding: 10px 0; font-size:220%;"
                                  >Monitoramento das Publicações</h2>
  </div>
</div>
"""

html_card_header_AA1="""
<div class="card">
  <div class="card-body" style="border-radius: 15px 15px 0px 0px; background: #5B51D8;  
                                border:solid; border-color: black; border-width: 1px 1px 1px 1px;
                                padding-top: 1px; padding-right: 20px; padding-bottom: 1px; padding-left: 20px; 
                                width: 100%; height: 40px;">
    <h5 class="card-title" style="background-color:#5B51D8; color:#F5F5F5; font-family:sans-serif;
                                  padding-top: 7px; padding-right: 1px; padding-bottom: 1px; padding-left: 1px; 
                                  text-align: center;font-size: 120%;" 
                                  >Indicadores Chaves</h5>
  </div>
</div>
"""

html_card_header_ABB="""
<div class="card">
  <div class="card-body" style="border-radius: 15px 15px 0px 0px; background: #5B51D8;  
                                border:solid; border-color: black; border-width: 1px 1px 1px 1px;
                                padding-top: 1px; padding-right: 20px; padding-bottom: 1px; padding-left: 20px; 
                                width: 100%; height: 40px;">
    <h5 class="card-title" style="background-color:#5B51D8; color:#F5F5F5; font-family:sans-serif;
                                  padding-top: 7px; padding-right: 15px; padding-bottom: 1px; padding-left: 15px; 
                                  text-align: center;font-size: 110%;" 
                                  >Indicadores por Tipo de Publicação</h5>
  </div>
</div>
"""

html_card_header_AB="""
<div class="card">
  <div class="card-body" style="border-radius: 15px 15px 0px 0px; background: #4169E1;  
                                border:solid; border-color: black; border-width: 1px 1px 1px 1px;
                                padding-top: 1px; padding-right: 20px; padding-bottom: 1px; padding-left: 20px; 
                                width: 100%; height: 40px;">
    <h5 class="card-title" style="background-color:#4169E1; color:#F5F5F5; font-family:sans-serif;
                                  padding-top: 7px; padding-right: 15px; padding-bottom: 1px; padding-left: 15px; 
                                  text-align: center;font-size: 120%;" 
                                  >Interações por Tipo de Publicação</h5>
  </div>
</div>
"""


html_card_header_BA="""
<div class="card">
  <div class="card-body" style="border-radius: 15px 15px 0px 0px; background: #4169E1;  
                                border:solid; border-color: black; border-width: 1px 1px 1px 1px;
                                padding-top: 1px; padding-right: 20px; padding-bottom: 1px; padding-left: 20px; 
                                width: 100%; height: 40px;">
    <h5 class="card-title" style="background-color:#4169E1; color:#F5F5F5; font-family:sans-serif;
                                  padding-top: 7px; padding-right: 15px; padding-bottom: 1px; padding-left: 15px; 
                                  text-align: center;font-size: 120%;" 
                                  >Média de Interações por Dia da Semana</h5>
  </div>
</div>
"""

html_card_header_BB="""
<div class="card">
  <div class="card-body" style="border-radius: 15px 15px 0px 0px; background: #4169E1;  
                                border:solid; border-color: black; border-width: 1px 1px 1px 1px;
                                padding-top: 1px; padding-right: 20px; padding-bottom: 1px; padding-left: 20px; 
                                width: 100%; height: 40px;">
    <h5 class="card-title" style="background-color:#4169E1; color:#F5F5F5; font-family:sans-serif;
                                  padding-top: 7px; padding-right: 15px; padding-bottom: 1px; padding-left: 15px; 
                                  text-align: center;font-size: 120%;" 
                                  >Variação de Interações por Dia</h5>
  </div>
</div>
"""


html_card_header_CA="""
<div class="card">
  <div class="card-body" style="border-radius: 15px 15px 0px 0px; background: #4169E1;  
                                border:solid; border-color: black; border-width: 1px 1px 1px 1px;
                                padding-top: 1px; padding-right: 20px; padding-bottom: 1px; padding-left: 20px; 
                                width: 100%; height: 40px;">
    <h5 class="card-title" style="background-color:#4169E1; color:#F5F5F5; font-family:sans-serif;
                                  padding-top: 7px; padding-right: 15px; padding-bottom: 1px; padding-left: 15px; 
                                  text-align: center;font-size: 120%;" 
                                  >Tabela com Dados das Publicações</h5>
  </div>
</div>
"""
html_card_header_1D2="""
<div class="card">
  <div class="card-body" style="border-radius: 15px 15px 0px 0px; background: #4169E1;  
                                border:solid; border-color: black; border-width: 1px 1px 1px 1px;
                                padding-top: 1px; padding-right: 20px; padding-bottom: 1px; padding-left: 20px; 
                                width: 100%; height: 40px;">
    <h5 class="card-title" style="background-color:#4169E1; color:#F5F5F5; font-family:sans-serif;
                                  padding-top: 7px; padding-right: 15px; padding-bottom: 1px; padding-left: 15px; 
                                  text-align: center;font-size: 100%;" 
                                  >Palavras mais frequêntes nas Descrições</h5>
  </div>
</div>
"""

html_card_header_CC="""
<div class="card">
  <div class="card-body" style="border-radius: 15px 15px 0px 0px; background: #4169E1;  
                                border:solid; border-color: black; border-width: 1px 1px 1px 1px;
                                padding-top: 1px; padding-right: 20px; padding-bottom: 1px; padding-left: 20px; 
                                width: 100%; height: 40px;">
    <h5 class="card-title" style="background-color:#4169E1; color:#F5F5F5; font-family:sans-serif;
                                  padding-top: 7px; padding-right: 15px; padding-bottom: 1px; padding-left: 15px; 
                                  text-align: center;font-size: 120%;" 
                                  >Publicações por Turno e Dia da Semana</h5>
  </div>
</div>
"""



#-------------------------------------------------------------------------------------------------------
html_card_header_3A1="""
<div class="card">
  <div class="card-body" style="border-radius: 15px 15px 0px 0px; background: #4169E1;  
                                border:solid; border-color: black; border-width: 1px 1px 1px 1px;
                                padding-top: 1px; padding-right: 20px; padding-bottom: 1px; padding-left: 20px; 
                                width: 100%; height: 40px;">
    <h5 class="card-title" style="background-color:#4169E1; color:#F5F5F5; font-family:sans-serif;
                                  padding-top: 7px; padding-right: 15px; padding-bottom: 1px; padding-left: 15px; 
                                  text-align: center;font-size: 120%;" 
                                  >Tabela Interativa</h5>
  </div>
</div>
"""


#########################################################################################
#########################################################################################
#########################################################################################

html_title_sidebar="""
<h1 style="font-size:150%; color:#4169E1; font-family:sans-serif;
            text-align:center; ">Painel de Controle</h1>
"""

html_sub1_sidebar="""
<h5 class="card-title" style="color:#4169E1; font-family:sans-serif;
    text-align: center;font-size: 100%;">Selecione o Gráfico e seus Eixos:</h5>
"""


html_card_header_1AA="""
<div class="card">
  <div class="card-body" style="border-radius: 15px 15px 0px 0px; background: #5B51D8;  
                                border:solid; border-color: black; border-width: 1px 1px 1px 1px;
                                padding-top: 1px; padding-right: 20px; padding-bottom: 1px; padding-left: 20px; 
                                width: 100%; height: 40px;">
    <h5 class="card-title" style="background-color:#5B51D8; color:#F5F5F5; font-family:sans-serif;
                                  padding-top: 7px; padding-right: 15px; padding-bottom: 1px; padding-left: 15px; 
                                  text-align: center;font-size: 110%;" 
                                  >Gráfico de Barra</h5>
  </div>
</div>
"""






html_card_1="""
<div class="card" style="border-radius: 10px 10px 10px 10px; background: #F5F5F5; 
                         border:solid; border-color: black; border-width: 1px 1px 1px 1px;
                         width: 100%; height: 200px;
                         padding-top: 5px; padding-right: 20px; padding-bottom: 1px; padding-left: 20px;">
    <p class="card-title" style="background-color:#F5F5F5; color:#0d0d0d; 
                                  margin-top: 10px; margin-bottom: 10px; margin-left: 10px; margin-right: 10px;
                                  font-family:sans-serif; text-align: justify;
                                  font-size: 90%" > A base de dados deste Data App são as publicações do Instagram
                                  dos principais portais de notícias do Brasil, sendo possível observar diversas características
                                  e métricas dessas publicações, como número de likes, comentários, interações, data e horário,
                                  link, id único e mais. Todas essas características podem ser analisadas em
                                  Tabelas Dinâmicas e visualizadas em Dashboards Interativos.<br> 
                                  Além da análise e visualização dos dados é possível explorá-los, este Data App contém
                                  diversos recursos para configurar e filtrar os dados utilizados, assim como, configurar
                                  todos os gráficos com seus eixos e formatos. Para se aprofundar nas funcionalidades e 
                                  tutoriais deste app, clique abaixo. 👇
</p>
</div>
"""

