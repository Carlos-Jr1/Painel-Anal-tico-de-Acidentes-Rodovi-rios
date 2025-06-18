import dash
from dash import dcc, html, Input, Output, dash_table
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import dash_bootstrap_components as dbc
import os

# Caminho dos arquivos CSV
upload_path = "upload"

# Carregar os dados de acidentes
try:
    df_acidentes = pd.read_csv(
        os.path.join(upload_path, "acidentes2025_todas_causas_tipos.csv"),
        sep=";",
        encoding="latin1"
    )
except FileNotFoundError:
    print("Arquivo de acidentes não encontrado!")
    df_acidentes = pd.DataFrame()

# Carregar os dados de frota (IBGE)
try:
    df_frotas = pd.read_csv(
        os.path.join(upload_path, "ibge_agregados_list.csv"),
        sep=";",
        encoding="utf-8"
    )
except FileNotFoundError:
    print("Arquivo de frota (IBGE) não encontrado!")
    df_frotas = pd.DataFrame()

# Limpeza e padronização básica
if not df_acidentes.empty:
    df_acidentes.columns = df_acidentes.columns.str.lower()

    # Converter datas
    if "data_inversa" in df_acidentes.columns:
        df_acidentes["data_inversa"] = pd.to_datetime(df_acidentes["data_inversa"], errors="coerce")
        df_acidentes["ano"] = df_acidentes["data_inversa"].dt.year
        df_acidentes["mes"] = df_acidentes["data_inversa"].dt.month
        df_acidentes["dia_semana"] = df_acidentes["data_inversa"].dt.day_name()

    # Tratar colunas numéricas
    for col in ["km", "pessoas", "mortos", "feridos", "veiculos"]:
        if col in df_acidentes.columns:
            df_acidentes[col] = pd.to_numeric(df_acidentes[col], errors="coerce").fillna(0)

    # Latitude e Longitude
    if "latitude" in df_acidentes.columns and "longitude" in df_acidentes.columns:
        df_acidentes["latitude"] = df_acidentes["latitude"].astype(str).str.replace(",", ".").astype(float)
        df_acidentes["longitude"] = df_acidentes["longitude"].astype(str).str.replace(",", ".").astype(float)

    # Padronizar rodovia (opcional)
    if 'rodovia' in df_acidentes.columns:
        df_acidentes['rodovia'] = df_acidentes['rodovia'].astype(str).str.strip().str.upper()

# Dados para os cards resumo
total_acidentes = len(df_acidentes)
total_municipios = df_acidentes['municipio'].nunique() if "municipio" in df_acidentes.columns else 0
total_frota = df_frotas['quantidade'].sum() if "quantidade" in df_frotas.columns else 0

# Preparar dados de correlação
if "municipio" in df_acidentes.columns and "municipio" in df_frotas.columns:
    acidentes_por_municipio = df_acidentes.groupby("municipio").size().reset_index(name="total_acidentes")
    frota_por_municipio = df_frotas.groupby("municipio")["quantidade"].sum().reset_index(name="total_frota")
    df_correlacao = pd.merge(acidentes_por_municipio, frota_por_municipio, on="municipio", how="inner")
else:
    df_correlacao = pd.DataFrame()

# Criar a app Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

# Layout do app
app.layout = dbc.Container([

    # Banner
    dbc.Row([
        dbc.Col(html.Div([
            html.H1("📊 Painel Analítico de Acidentes Rodoviários", className="text-white text-center"),
            html.H5("Análise descritiva baseada em dados reais da PRF e IBGE", className="text-white text-center")
        ], style={"backgroundColor": "#0d6efd", "padding": "20px", "borderRadius": "10px"}))
    ], className="mb-4"),

    # Cards Resumo
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Total de Acidentes", className="card-title"),
                html.H3(f"{total_acidentes:,}", className="card-text text-danger")
            ])
        ], color="light", inverse=False, className="shadow"), width=4),

        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Municípios Atingidos", className="card-title"),
                html.H3(f"{total_municipios:,}", className="card-text text-primary")
            ])
        ], color="light", inverse=False, className="shadow"), width=4),

        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Total de Veículos na Frota", className="card-title"),
                html.H3(f"{total_frota:,}", className="card-text text-success")
            ])
        ], color="light", inverse=False, className="shadow"), width=4),
    ], className="mb-4"),

    html.Hr(),

    # Filtros (sem rodovia, faixa de horário ou trecho crítico)
    dbc.Row([
        dbc.Col([
            html.Label("Estado (UF):"),
            dcc.Dropdown(
                id='filtro-estado',
                options=[{'label': 'Todos', 'value': 'todos'}] + [{'label': uf, 'value': uf} for uf in sorted(df_acidentes['uf'].dropna().unique())] if 'uf' in df_acidentes.columns else [],
                value='todos'
            )
        ], width=4),
        dbc.Col([
            html.Label("Tipo de Acidente:"),
            dcc.Dropdown(
                id='filtro-tipo-acidente',
                options=[{'label': 'Todos', 'value': 'todos'}] + [{'label': tipo, 'value': tipo} for tipo in sorted(df_acidentes['tipo_acidente'].dropna().unique())] if 'tipo_acidente' in df_acidentes.columns else [],
                value='todos'
            )
        ], width=4),
    ], className="mb-4"),

    html.Hr(),

    # Linha de gráficos principais
    dbc.Row([
        dbc.Col(dcc.Graph(id='mapa-acidentes'), width=6),
        dbc.Col(dcc.Graph(id='grafico-tipo-acidente'), width=6)
    ], className="mb-4"),

    dbc.Row([
        dbc.Col(dcc.Graph(id='grafico-dia-semana'), width=6),
        dbc.Col(dcc.Graph(id='grafico-correlacao'), width=6),
    ], className="mb-4"),

], fluid=True)

# Callback para atualizar os gráficos de acordo com os filtros
@app.callback(
    [
        Output('mapa-acidentes', 'figure'),
        Output('grafico-tipo-acidente', 'figure'),
        Output('grafico-dia-semana', 'figure'),
        Output('grafico-correlacao', 'figure'),
    ],
    [
        Input('filtro-estado', 'value'),
        Input('filtro-tipo-acidente', 'value'),
    ]
)
def update_graphs(estado, tipo_acidente):
    df_filtered = df_acidentes.copy()

    if estado != 'todos' and 'uf' in df_filtered.columns:
        df_filtered = df_filtered[df_filtered['uf'] == estado]

    if tipo_acidente != 'todos' and 'tipo_acidente' in df_filtered.columns:
        df_filtered = df_filtered[df_filtered['tipo_acidente'] == tipo_acidente]

    # Mapa de Acidentes
    fig_mapa = px.scatter_mapbox(
        df_filtered,
        lat="latitude",
        lon="longitude",
        hover_name="municipio" if "municipio" in df_filtered.columns else None,
        hover_data=["rodovia", "tipo_acidente"] if all(col in df_filtered.columns for col in ["rodovia", "tipo_acidente"]) else None,
        color="tipo_acidente" if "tipo_acidente" in df_filtered.columns else None,
        zoom=5,
        mapbox_style="open-street-map",
        title="📍 Mapa dos Acidentes"
    ) if not df_filtered.empty else go.Figure()

    # Tipo de Acidente - gráfico pizza
    tipo_counts = df_filtered['tipo_acidente'].value_counts() if 'tipo_acidente' in df_filtered.columns else pd.Series()
    fig_tipo = px.pie(values=tipo_counts.values, names=tipo_counts.index, title="🔎 Tipos de Acidente") if not tipo_counts.empty else go.Figure()

    # Dia da Semana (com tradução)
    dias_semana_traducao = {
        'Monday': 'Segunda',
        'Tuesday': 'Terça',
        'Wednesday': 'Quarta',
        'Thursday': 'Quinta',
        'Friday': 'Sexta',
        'Saturday': 'Sábado',
        'Sunday': 'Domingo'
    }
    dia_counts = df_filtered['dia_semana'].value_counts().sort_index() if 'dia_semana' in df_filtered.columns else pd.Series()
    dia_counts.index = dia_counts.index.map(lambda x: dias_semana_traducao.get(x, x)) if not dia_counts.empty else []
    fig_dia = px.bar(x=dia_counts.index, y=dia_counts.values, title="📅 Acidentes por Dia da Semana") if not dia_counts.empty else go.Figure()

    # Correlação entre Frota e Acidentes
    fig_correlacao = px.scatter(
        df_correlacao,
        x="total_frota",
        y="total_acidentes",
        hover_name="municipio",
        title="⚖️ Correlação entre Frota e Acidentes"
    ) if not df_correlacao.empty else go.Figure()

    return fig_mapa, fig_tipo, fig_dia, fig_correlacao

# Rodar o servidor Dash
import os

port = int(os.environ.get('PORT', 8050))
app.run_server(host='0.0.0.0', port=port)

