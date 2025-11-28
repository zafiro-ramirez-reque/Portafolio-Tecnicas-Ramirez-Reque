import dash
from dash import html, dcc, callback, Input, Output, State
import numpy as np
import plotly.graph_objects as go
import requests
import datetime

dash.register_page(__name__, path='/pagina5', name='covid-19')

layout = html.Div([
    html.Div([
        html.H2("Dashboard Covid-19", className="title"),

        html.Div([
            html.Label("Seleccione el país:"),
            dcc.Dropdown(
                id="dropdown-pais",
                options=[
                    {"label": "Perú", "value": "Peru"},
                    {"label": "México", "value": "Mexico"},
                    {"label": "Estados Unidos", "value": "USA"},
                    {"label": "Canadá", "value": "Canada"}
                ],
                value="Peru",
                className="input-field",
                style={"width": "100%"}
            )
        ], className="input-group"),  
        
        html.Div([
            html.Label("Días historico"),
            dcc.Dropdown(
                id="dropdown-dias-covid",
                options=[
                    {"label": "30 días", "value": 30},
                    {"label": "60 días", "value": 60},
                    {"label": "90 días", "value": 90},
                    {"label": "120 días", "value": 120},
                    {"label": "Todo el histórico", "value": "all"}
                ],
                value=30,
                className="input-field",
                style={"width": "100%"}
            )
        ], className="input-group"),

        html.Button("Actualizar Datos", id="btn-actualizar-covid", className="btn-generar"),

        html.Div(
        id="info-actualizado-covid"
        )

    ], className="content left"), 

    html.Div([
        html.H2("Estadísticas en tiempo real", className="title"),

        html.Div([
            html.Div([
                html.H4("Total Casos", style={'color': '#1976d2'}),
                html.H3(id="total-casos", style={'color': '#0b3661'})
            ],
            style={
                'backgroundColor': '#e3f2fd',
                'padding': '10px',
                'borderRadius': '10px',
                'textAlign': 'center',
                'margin': '5px'
            }),

            html.Div([
                html.H4("Casos nuevos", style={'color': '#eca23b'}),
                html.H3(id="casos-nuevos", style={'color': '#e18300'})
            ],
            style={
                'backgroundColor': '#e3f2fd',
                'padding': '10px',
                'borderRadius': '10px',
                'textAlign': 'center',
                'margin': '5px'
            }),

            html.Div([
                html.H4("Total muertes", style={'color': "#4d4545"}),
                html.H3(id="total-muertes", style={'color': '#212121'})
            ],
            style={
                'backgroundColor': '#e3f2fd',
                'padding': '10px',
                'borderRadius': '10px',
                'textAlign': 'center',
                'margin': '5px'
            }),

            html.Div([
                html.H4("Recuperados ", style={'color': '#458945'}),
                html.H3(id="total-recuperados", style={'color': '#0f470a'})
            ],
            style={
                'backgroundColor': '#e3f2fd',
                'padding': '10px',
                'borderRadius': '10px',
                'textAlign': 'center',
                'margin': '5px'
            }),
        ], style={'display': 'flex'}),

        dcc.Graph(id="grafica-covid", style={"height": "450", "width": "100%"})

    ], className="content right") 

], className="page-container") 

# funciones para conectar a la API
def obtener_datos_pais(pais):
    try:
        url = f"https://disease.sh/v3/covid-19/countries/{pais}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error al obtener datos del país {pais}: {e}")
        return None

def obtener_historico_pais(pais, dias):
    try:
        url = f"https://disease.sh/v3/covid-19/historical/{pais}"
        params = {"lastdays": dias}
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error al obtener histórico del país {pais}: (e)")
        return None

def formatear_numero(numero): # ej: 1567890 -> 1,567,890
    if numero is None:
        return "N/A"
    return f"{numero:,}"

# callback para actualizar datos y gráfica
@callback(
    Output("total-casos", "children"),
    Output("casos-nuevos", "children"),
    Output("total-muertes", "children"),
    Output("total-recuperados", "children"),
    Output("grafica-covid", "figure"),
    Output("info-actualizado-covid", "children"),
    Input("btn-actualizar-covid", "n_clicks"),
    State("dropdown-pais", "value"),
    State("dropdown-dias-covid", "value"),
    prevent_initial_call=False
)
def actualizar_dashboard_covid(n_clicks, pais, dias):
    datos_actuales = obtener_datos_pais(pais)
    historico = obtener_historico_pais(pais, dias)

    if not datos_actuales or not historico:
        fig = go.Figure()
        fig.add_annotation(
            text="Error al obtener datos",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=15, color="red")
        )
        fig.update_layout(
            paper_bgcolor="lightcyan",
            plot_bgcolor="white"
        )

        return "N/A", "N/A", "N/A", "N/A", fig, "No se pudieron actualizar los datos."

    total_casos = datos_actuales.get("cases", 0)
    casos_hoy = datos_actuales.get("todayCases", 0)
    total_muertes = datos_actuales.get("deaths", 0)
    total_recuperados = datos_actuales.get("recovered", 0)

    total_casos_texto = formatear_numero(total_casos)
    casos_hoy_texto = formatear_numero(casos_hoy)
    total_muertes_texto = formatear_numero(total_muertes)
    total_recuperados_texto = formatear_numero(total_recuperados)
    
    timeline = historico.get("timeline", {})
    casos_historicos = timeline.get("cases", {})
    muertes_historicas = timeline.get("deaths", {})

    fechas = list(casos_historicos.keys())
    valores_casos = list(casos_historicos.values())
    valores_muertes = list(muertes_historicas.values())

    fechas_dt = [datetime.datetime.strptime(fecha, "%m/%d/%y") for fecha in fechas]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=fechas_dt,
        y=valores_casos,
        mode='lines',
        fill='tozeroy',
        name='Casos Totales',
        line=dict(color='orange', width=2),
        yaxis='y2',
        hovertemplate='Fecha: %{x|%d %b %Y}<br>Casos: %{y:,}<extra></extra>'
    ))

    fig.add_trace(go.Scatter(
        x=fechas_dt,
        y=valores_muertes,
        mode='lines',
        name='Muertes Totales',
        line=dict(color='red', width=2),
        hovertemplate='Fecha: %{x|%d %b %Y}<br>Muertes: %{y:,}<extra></extra>'
    ))

    return (total_casos_texto, casos_hoy_texto, total_muertes_texto, total_recuperados_texto, fig,
            f"Datos actualizados para {pais}.")