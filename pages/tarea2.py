import dash
from dash import html, dcc, Input, Output, State, callback
import numpy as np
import plotly.graph_objects as go
from utils.funciones import funcion_graficas_ecu_log

dash.register_page(__name__, path="/tarea2", name="Tarea 2")

#### Layout ###

layout = html.Div(children=[
    # contenedor izquierdo
    html.Div([ 
        html.H2("Parámetros del modelo", className='title'),
        
        html.Div([
            html.Label("Poblacion inicial P(0):"),
            dcc.Input(id="input-p0", type="number", value=200, className='input-field')
        ], className="input-group"),

        html.Div([
            html.Label("Tasa de crecimiento (r):"),
            dcc.Input(id="input-r", type="number", value=0.04, className="input-field")
        ], className="input-group"),

        html.Div([
            html.Label("Capacidad de carga (K):"),
            dcc.Input(id="input-K", type="number", value=750, className='input-field')
        ], className="input-group"),

        html.Div([
            html.Label("Tiempo máximo (t):"),
            dcc.Input(id="input-t", type="number", value=100, className="input-field")
        ], className="input-group"),

        html.Button("Generar gráfica", id="btn-generar", className="btn-generar")
    ], className="content left"),

    #Contenedor derecho
    html.Div([ 
        html.H2("Gráfica", className="title"),

        dcc.Graph(
            id="grafica-poblacion",
            style={"height": "350px",'width':'100%'},
        ),
    ], className="content right")
], className="page-container") 


#### Callbacks ####
@callback(
    Output('grafica-poblacion', 'figure'),
    Input('btn-generar', 'n_clicks'),
    State('input-p0', 'value'),
    State('input-r','value'),
    State('input-K','value'),
    State('input-t','value'),
    prevent_initial_call=False
)

def actualizar_grafica(n_clicks, p0, r, k, t_max):
    fig = funcion_graficas_ecu_log(p0, r, k, t_max)

    return fig