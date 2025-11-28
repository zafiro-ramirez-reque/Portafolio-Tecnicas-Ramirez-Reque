import dash
from dash import html, dcc, callback, Input, Output, State
import numpy as np
import plotly.graph_objects as go
from scipy.integrate import odeint

dash.register_page(__name__, path="/pagina4", name="Modelo SEIR")

layout = html.Div(children=[
    html.Div([
        html.H2("Modelo SEIR - Epidemiología", className='title'),

        html.Div([
            html.Label("Población Total (N):"),
            dcc.Input(id="input-N", type='number', value=1000, className='input-field')
        ], className="input-group"),

        html.Div([
            html.Label("Tasa de transmisión (β):"),
            dcc.Input(id="input-beta", type='number', value=0.3, className='input-field')
        ], className="input-group"),

        html.Div([
            html.Label("Tasa de incubación (σ):"),
            dcc.Input(id="input-sigma", type='number', value=0.1, step=0.01, className='input-field')
        ], className="input-group"),

        html.Div([
            html.Label("Tasa de recuperación (γ):"),
            dcc.Input(id="input-gamma", type='number', value=0.1, step=0.01, className='input-field')
        ], className="input-group"),

        html.Div([
            html.Label("Infectados iniciales (I0):"),
            dcc.Input(id="input-I0", type='number', value=1, className='input-field')
        ], className="input-group"),

        html.Div([
            html.Label("Tiempo de simulación:"),
            dcc.Input(id="input-tiempo", type='number', value=100, className='input-field')
        ], className="input-group"),

        html.Button("Simular Epidemia", id="btn-simular", className="btn-generar"),
    ], className="content left"),

    html.Div([
        html.H2("Evolución de la Epidemia SEIR", className="title"),
        dcc.Graph(id="grafica-seir", style={"height": "450px",'width':'100%'}),
    ], className="content right")
], className="page-container")


# Modelo SEIR
def modelo_seir(y, t, beta, sigma, gamma, N):
    S, E, I, R = y

    dS_dt = -beta * S * I / N
    dE_dt = beta * S * I / N - sigma * E
    dI_dt = sigma * E - gamma * I
    dR_dt = gamma * I

    return dS_dt, dE_dt, dI_dt, dR_dt

# Callback para actualizar la gráfica
@callback(
    Output("grafica-seir", "figure"),
    Input("btn-simular", "n_clicks"),
    State("input-N", "value"),
    State("input-beta", "value"),
    State("input-sigma", "value"),
    State("input-gamma", "value"),
    State("input-I0", "value"),
    State("input-tiempo", "value"),
    prevent_initial_call=False
)

def simular_seir(n_clicks, N, beta, sigma, gamma, I0, tiempo_max):
    S0 = N - I0
    E0 = 0
    R0 = 0
    y0 = [S0, E0, I0, R0]

    t = np.linspace(0, tiempo_max, 200)

    try:
        solucion = odeint(modelo_seir, y0, t, args=(beta, sigma, gamma, N))
        S, E, I, R = solucion.T
    except Exception as e:
        S = np.full_like(t, S0)
        E = np.full_like(t, E0)
        I = np.full_like(t, I0)
        R = np.full_like(t, R0)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=t, y=S, 
        mode='lines', 
        name='Susceptibles', 
        line=dict(color='green', width=2),
        hovertemplate='Día: %{x:.0f}<br>Susceptibles: %{y:.0f}<extra></extra>'
    ))

    fig.add_trace(go.Scatter(
        x=t, y=E, 
        mode='lines', 
        name='Expuestos', 
        line=dict(color='orange', width=2),
        hovertemplate='Día: %{x:.0f}<br>Expuestos: %{y:.0f}<extra></extra>'
    ))

    fig.add_trace(go.Scatter(
        x=t, y=I, 
        mode='lines', 
        name='Infectados', 
        line=dict(color='red', width=2),
        hovertemplate='Día: %{x:.0f}<br>Infectados: %{y:.0f}<extra></extra>'
    ))

    fig.add_trace(go.Scatter(
        x=t, y=R, 
        mode='lines', 
        name='Recuperados', 
        line=dict(color='blue', width=2),
        hovertemplate='Día: %{x:.0f}<br>Recuperados: %{y:.0f}<extra></extra>'
    ))

    fig.update_layout(
        title=dict(
            text='<b>Evolución del Modelo SEIR</b>',
            x=0.5, font=dict(size=16, color='darkblue')
        ),
        xaxis_title='Tiempo (días)',
        yaxis_title='Número de personas',
        paper_bgcolor='lightcyan',
        plot_bgcolor='white',
        font=dict(family='Outfit', size=12),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=0.5
        ),
        margin=dict(l=40, r=40, t=60, b=40)
    )

    fig.update_xaxes(
        showgrid=True, gridwidth=1, gridcolor='lightpink',
        zeroline=True, zerolinewidth=2, zerolinecolor='black'
    )

    fig.update_yaxes(
        showgrid=True, gridwidth=1, gridcolor='lightpink',
        zeroline=True, zerolinewidth=2, zerolinecolor='black'
    )

    return fig