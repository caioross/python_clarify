from flask import Flask, request, jsonify, render_template_string
import pandas as pd
import sqlite3
import os
import plotly.graph_objs as go
import dash
from dash import Dash, html, dcc
import numpy as np
import config
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

#   ____ _            _  __       
#  / ___| | __ _ _ __(_)/ _|_   _ 
# | |   | |/ _` | '__| | |_| | | |
# | |___| | (_| | |  | |  _| |_| |
#  \____|_|\__,_|_|  |_|_|  \__, |
#                           |___/ 
#
# AUTOR: Caio Comitre ROssi
# VERSÃO: 0.0.1 [Beta]
# LICENÇA: Creative Commons

app = Flask(__name__)
DB_PATH = config.DB_PATH

# Função para inicializar o banco de dados SQL
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS inadimplencia (
                mes TEXT PRIMARY KEY,
                inadimplencia REAL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS selic (
                mes TEXT PRIMARY KEY,
                selic REAL
            )
        ''')
        conn.commit()
vazio = 0

@app.route('/')
def index():
    return render_template_string('''
        <h1> Upload de Dados Economicos </h1>
        <form action='/upload' method='POST' enctype='multipart/form-data'>
            <label for='campo_inadimplencia'> Arquivo de Inadimplencia (CSV) </label>
            <input name='campo_inadimplencia' type='file' required><br><br>
            
            <label for='campo_selic'> Arquivo da Taxa Selic (CSV) </label>
            <input name='campo_selic' type='file' required><br><br>
            
            <input type='submit' value='Fazer Upload'>
        </form>
        <br><br><hr>
        <a href='/consultar'> Consultar dados Armazenados </a><br>
        <a href='/graficos'> Visualizar Graficos </a></br>  
        <a href='/editar_inadimplencia'> Editar dados de Inadimplencia </a></br>  
        <a href='/editar_selic'> Editar dados de selic </a></br>  
        <a href='/correlacao'> Analisar Correlação </a><br>
        <a href='/insights_3d'> Analisar Grafico 3D </a><br>
    ''')

@app.route('/upload', methods=['POST','GET'])
def upload():
    inad_file = request.files.get('campo_inadimplencia')
    selic_file = request.files.get('campo_selic')
    
    # Verificar se os arquivos foram devidamente enviados
    if not inad_file or not selic_file:
        return jsonify({"Erro":"Ambos os arquivos devem ser enviados"})
    
    inad_df = pd.read_csv(
        inad_file,
        sep = ";",
        names = ['data', 'inadimplencia'],
        header = 0
    )
    selic_df = pd.read_csv(
        selic_file,
        sep = ";",
        names = ['data', 'selic_diaria'],
        header = 0
    )
    inad_df['data'] = pd.to_datetime(inad_df['data'], format="%d/%m/%Y")
    selic_df['data'] = pd.to_datetime(selic_df['data'], format="%d/%m/%Y")
    
    inad_df['mes'] = inad_df['data'].dt.to_period('M').astype(str)
    selic_df['mes'] = selic_df['data'].dt.to_period('M').astype(str)
    
    inad_mensal = inad_df[['mes','inadimplencia']].drop_duplicates()
    selic_mensal = selic_df.groupby('mes')['selic_diaria'].mean().reset_index()
    
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS inadimplencia")
        cursor.execute("DROP TABLE IF EXISTS selic")
        
        inad_mensal.to_sql('inadimplencia', conn, if_exists='replace', index=False)
        selic_mensal.to_sql('selic', conn, if_exists='replace', index=False)
    return jsonify({"Mensagem":"Dados armazenados com sucesso no banco de dados"})

@app.route('/consultar', methods=['POST','GET'])
def consultar():
    
    if request.method == 'POST':
        tabela = request.form.get('campo_tabela')
        if tabela not in ['inadimplencia','selic']:
            return jsonify({"Erro":"Você ta tentando me invadir! Aqui não!!!"}),400
        with sqlite3.connect(DB_PATH) as conn:
            df = pd.read_sql_query(f"SELECT * FROM {tabela}", conn)
        return df.to_html(index=False)
    
    return render_template_string('''
        <h1> Consulta de Tabelas </h1>    
        <form method="POST">
            <label for="campo_tabela"> Escolha a tabela: </label>
            <select name="campo_tabela">
                <option value="inadimplencia"> Inadimplencia </option>
                <option value="selic"> Taxa Selic </option>
            </select>
            <input type="submit" value="Consultar">
        </form>    
        <br><a href='/'>Voltar</a>                             
    ''')
    
@app.route('/graficos')
def graficos():
    with sqlite3.connect(DB_PATH) as conn:
        inad_df = pd.read_sql_query("SELECT * FROM inadimplencia", conn)
        selic_df = pd.read_sql_query("SELECT * FROM selic", conn)
    
    fig1 = go.Figure()
    fig1.add_trace(
        go.Scatter(
            x = inad_df['mes'], 
            y = inad_df['inadimplencia'],
            mode = 'lines+markers',
            name = 'Inadimplência'            
        )
    )
    # Variação de templates: 'ggplot2','seaborn','simple_white','plotly','plotly_white','plotly_dark','presentation','xgridoff', 'ygridoff', 'gridon', 'none'
    fig1.update_layout(
        title = "Evolução da Inadimplencia",
        xaxis_title = "Mês",
        yaxis_title = "%",
        template = "plotly_dark"
    )
    
    fig2 = go.Figure()
    fig2.add_trace(
        go.Scatter(
            x = selic_df['mes'],
            y = selic_df['selic_diaria'],
            mode =  'lines+markers',
            name = 'Selic'
        )
    )
    fig2.update_layout(
        title = 'Media Mensal da Selic',
        xaxis_title = 'MÊs',
        yaxis_title = 'Taxa',
        template = 'plotly_dark'
    )
    
    graph_html_1 = fig1.to_html(full_html=False, include_plotlyjs='cdn')
    graph_html_2 = fig2.to_html(full_html=False, include_plotlyjs=False)
        
    return render_template_string('''
        <html>
            <head>
                <title> Graficos Economicos </title>
                <style>
                    .container{
                        display:flex;
                        justify-content:space-around;
                    }
                    .graph{
                        width: 48%;
                    }
                </style>
            </head>
            <body>
                <h1> Graficos Economicos </h1>
                <div class="container">
                    <div class="graph">{{ grafico01|safe }}</div>
                    <div class="graph">{{ grafico02|safe }}</div>
                </div>
            <br><a href='/'>Voltar</a> 
            </body>
        </html>                   
    ''', grafico01 = graph_html_1, grafico02 = graph_html_2)
    
@app.route('/editar_inadimplencia', methods=['POST','GET'])
def editar_inadimplencia():
    if request.method == 'POST':
        mes = request.form.get('campo_mes')
        novo_valor = request.form.get('campo_valor')
        try:
            novo_valor = float(novo_valor)
        except:
            return jsonify({"Erro":"Valor Invalido, tente novamente"})
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE inadimplencia SET inadimplencia = ? WHERE mes = ?', (novo_valor, mes))
            conn.commit()
        return jsonify({"mensagem":f"Valor atualizado para o mes {mes}"})

    return render_template_string('''
         <h1> Editar inadimplencia </h1>
         <form method="POST">
            <label for="campo_mes">Mês (AAAA-MM):</label>
            <input type="text" name="campo_mes"><br>
            <label for="campo_valor">Novo valor de Inadimplencia:</label>
            <input type="text" name="campo_valor"><br>
            <input type="submit" value="Atualizar dados">            
         </form>
         <br><a href='/'>Voltar</a>                     
    ''')
    
@app.route('/editar_selic', methods=['GET', 'POST'])
def editar_selic():
    if request.method == 'POST':
        mes = request.form.get('campo_mes')
        novo_valor = request.form.get('campo_valor')
        try:
            novo_valor = float(novo_valor)
        except:
            return jsonify({'mensagem': 'Valor inválido.'})
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE selic SET selic_diaria = ? WHERE mes = ?",(novo_valor, mes))
            conn.commit()
        return jsonify({'mensagem': f'SELIC atualizada para o mês {mes}'})

    return render_template_string('''
        <h1>Editar Taxa SELIC</h1>
        <form method="POST">
            <label for="campo_mes">Mês (AAAA-MM):</label>
            <input type="text" name="campo_mes" required><br><br>
            <label for="campo_valor">Nova Taxa SELIC:</label>
            <input type="text" name="campo_valor" required><br><br>
            <input type="submit" value="Atualizar Dados">
        </form>
        <br>
        <a href="/">Voltar</a>
    ''')
    
# https://dontpad.com/clarify_cursos

@app.route('/correlacao')
def correlacao():
    with sqlite3.connect(DB_PATH) as conn:
        inad_df = pd.read_sql_query("SELECT * FROM inadimplencia", conn)
        selic_df = pd.read_sql_query("SELECT * FROM selic", conn)
    
    merged = pd.merge(inad_df, selic_df, on='mes')
    correl = merged['inadimplencia'].corr(merged['selic_diaria'])
    
    x = merged['selic_diaria'] 
    y = merged['inadimplencia']

    m, b = np.polyfit(x, y, 1)
    # quem é m: é a inclinação da reta (coeficiente angular) -> diz o quão rapido Y cresce/decresce
    # quem é op b: onde a reta cruza com o eixo Y (coeficiente linear) -> o valor de y quando x = 0
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x = x,
        y = y,
        mode='markers',
        name='Inadimplencia X Selic',
        marker = dict(
            color = 'rgba(0, 123, 255, 0.8)',
            size = 12,
            line = dict(width=2, color='white'),
            symbol = 'circle'
        ),
        hovertemplate = 'SELIC: %{x:.2f}% <br> Inadimplencia %{y:.2f}%<extra></extra>'
    ))
    fig.add_trace(go.Scatter(
        x = x,
        y = m * x + b,
        mode = 'lines', 
        name = 'Linha de Tendência',
        line = dict(
            color = 'rgba(220, 53, 69, 1)',
            width = 4,
            dash = 'dot'
        )
    ))
    fig.update_layout(
        title = {
            'text' : f'<b>Correlação entre SELIC e Inadimplencia</b><br><span style="font-size:16px;">Coeficiente de Correlação: {correl:.2f}</span>',
            'y': 0.95,
            'x': 0.5,
            'xanchor' : 'center', # center, left, right
            'yanchor' : 'top' # top, bottom, middle
        },
        xaxis_title = dict(
            text = 'SELIC Média Mensal (%)',
            font = dict(
                size = 18,
                family = 'Arial',
                color = 'gray'
            )
        ),
        yaxis_title = dict(
            text = 'Inadimplencia (%)',
            font = dict(
                size = 18,
                family = 'Arial',
                color = 'gray'
            )
        ),
        xaxis = dict(
            tickfont = dict(
                size    = 14,
                family  = 'Tahoma',
                color   = 'lightgray'
            ),
            gridcolor = 'black'
        ),
        yaxis = dict(
            tickfont = dict(
                size    = 14,
                family  = 'Tahoma',
                color   = 'black'
            ),
            gridcolor = 'lightgray'
        ),
        plot_bgcolor = "#f8f9fa",
        paper_bgcolor = 'white',
        font = dict(
            size    = 14,
            family  = 'Arial',
            color   = 'black'
        ),
        legend = dict(
            orientation = 'h',
            borderwidth = 0,
            bgcolor = 'rgba(0,0,0,0)',
            y = 1.05,
            x = 0.5,
            yanchor = 'bottom',
            xanchor = 'center'
        ),
        margin = dict(
            l = 60,
            r = 60,
            t = 120,
            b = 60
        )
    )
    grafico_correlacao = fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    return render_template_string('''
        <html>
            <head>
                <title> Correlação Selic vs Inadimplencia </title>
                <style>
                    body {
                        font-family: Arial;
                        background-color: #ffffff;
                        color:  #333;  
                    }
                    h1 { 
                        margin-top: 40px;
                    }
                    a: {
                        text-decoration: none;
                        color: #007bff;
                    }
                    a:hover {
                        text-decoration: underline;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1> Correlação entre SELIC e Inadimplencia</h1>
                    <div> {{ grafico|safe }} </div>
                </div>
            <br><a href='/'>Voltar</a> 
            </body>
        </html>                              
    ''', grafico = grafico_correlacao)
    
@app.route('/insights_3d')
def insights3d():
    with sqlite3.connect(DB_PATH) as conn:
        inad_df = pd.read_sql_query("SELECT * FROM inadimplencia", conn)
        selic_df = pd.read_sql_query("SELECT * FROM selic", conn)
        
    # Merge
    merged = pd.merge(inad_df, selic_df, on='mes').sort_values('mes')
    merged['mes_idx'] = range(len(merged))
    
    # Tendencia de inadimplencia (diferença mes a mes)
    merged['tend_inad'] = merged['inadimplencia'].diff().fillna(0)
    trend_color = ['subiu' if x > 0 else 'caiu' if x < 0 else 'estavel' for x in merged['tend_inad']]
    merged['selic_diaria']
    # derivadas discretas
    # armazena o valor numerico da variação mensal de inadimplencia e selic 
    merged['var_inad'] = merged['inadimplencia'].diff().fillna(0)
    merged['var_selic'] = merged['selic_diaria'].diff().fillna(0)
    
    # isola as colunas de dados economicos que serao utilizadas na clusterização
    features = merged[['selic_diaria','inadimplencia']].copy()
    # Instanciamos o objeto do standart scaller para normalizar a escala
    scaler = StandardScaler()
    # Ajusta o scaler e transforma as features para terem a media 0 e desvio padrão 1
    scaled_features = scaler.fit_transform(features)
    
    #Configuramos o KMeans para agrupar os dados em 3 grupos, com semente fixa em 10 inicial
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    # Executa o codigo do algotimo que ja criamos e guarda o rotulo dos grupos  (0, 1 ou 2) no dataframe principal
    merged['cluster'] = kmeans.fit_predict(scaled_features)
    
    # Transformar as colunas preditoras (tempo e selic) em uma matriz usando o numpy bidimensional
    x = merged[['mes_idx', 'selic_diaria']].values
    y = merged['inadimplencia'].values
    # concatena uma coluna 1s à matriz para calcular o coeficiente linear (intercepto)
    a = np.c_[x, np.ones(x.shape[0])]
    #resolve a equação matricial por minimos quadrados para obter os coeficientes do plano 3d da tendencia
    coeffs, _, _, _ = np.linalg.lstsq(a, y, rcond=None) # z = a*x + b*y +c
    
    # criar 30 pontos linearmente espaçados entre o primeiro e o ultimo mês do historico
    xi = np.linspace(merged['mes_idx'].min(), merged['mes_idx'].max(), 30)
    # criar 30 pontos linearmente espaçados entre o menor e o maior valor historico da SELIC
    yi = np.linspace(merged['selic_diaria'].min(), merged['selic_diaria'].max(), 30)
    #transforma os vetores xi e yi em matrizes de coordenadas 2d para formar um grid
    xi, yi = np.meshgrid(xi, yi)
    # calcula os valores teoricos de Z (inadimplencia) para cada ponto do grid usando os coeficientes.
    zi = coeffs[0]*xi + coeffs[1]*yi + coeffs[2]
    
    scatter = go.Scatter3d(
        x = merged['mes_idx'],
        y = merged['selic_diaria'],
        z = merged['inadimplencia'],
        mode = 'markers',
        marker = dict(
          size=8,
          color=merged['cluster'],
          colorscale='Viridis',   
          opacity=0.9
        ),
        text = [
            f"Mês: {m}<br>Inadimplencia: {z:.2f}%<br>Var Inad: {vi:.2f}<br>Var Selic: {vs:.2f}<br>Tendencia: {t}"
            for m, z, y, vi, vs, t in zip(
                merged['mes'], merged['inadimplencia'], merged['selic_diaria'],
                merged['var_inad'], merged['var_selic'], trend_color
            )
            ],
        hovertemplate = '%{text}<extra></extra>'
    )
    surface = go.Surface(
        x = xi,
        y = yi,
        z = zi,
        showscale = False,
        colorscale = 'Reds',
        opacity = 0.5,
        name = 'Plano de Regressão'
    )
    
    fig = go.Figure(data=[scatter,surface])
    
    fig.update_layout(
        scene = dict(
            xaxis = dict(
                title = 'Tempo (Meses)', 
                tickvals = merged['mes_idx'], 
                ticktext = ['mes']
            ),
            yaxis = dict(title='SELIC (%)'),
            zaxis = dict(title='Inadimplencia (%)')
        ),
        title = 'Insights economicos 3D com Tendencia, Derivadas e Clusters',
        margin = dict(l=0, r=0, t= 50, b=0),
        height = 800
    )
    grafico3d = fig.to_html(full_html=False, include_plotlyjs='cdn')
    return render_template_string('''
        <html>
            <head>
                <title> Insights Economicos 3D </title>
                <style>
                    body {
                        font-family: Arial;
                        background-color: #ffffff;
                        color:  #333;  
                    }
                    h1 { 
                        margin-top: 40px;
                    }
                    a: {
                        text-decoration: none;
                        color: #007bff;
                    }
                    a:hover {
                        text-decoration: underline;
                    }
                    .container{
                        width: 95%;
                        margin: auto;                        
                    }
                </style>
            </head>
            <body>
                <div>
                    <h1> Grafico 3D com Insights Economicos </h1>
                    <p>Analise visual com clusters, tendencia e plano de regressão.</p>
                    <div> {{ grafico3d_fim|safe }} </div>
                </div>
            <br><a href='/'>Voltar ao</a> 
            </body>
        </html>                              
    ''', grafico3d_fim = grafico3d)
    
if __name__ == '__main__':
    init_db()
    app.run(debug=True)

