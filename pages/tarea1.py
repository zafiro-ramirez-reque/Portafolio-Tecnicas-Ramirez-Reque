import dash
from dash import html, dcc
import plotly.graph_objects as go
import numpy as np

#############################
# Modelo de Crecimiento con Capacidad de Carga (Logístico)

P0 = 100  # Población inicial
r = 0.03  # Tasa de crecimiento
K = 1000  # Capacidad de carga
t = np.linspace(0, 300, 100)  # Tiempo

# Función de crecimiento logístico (modelo con capacidad de carga)
P = (K * P0 * np.exp(r * t)) / (K + P0 * (np.exp(r * t) - 1))

# Crear un scatter plot
trace_logistic = go.Scatter(
    x=t,
    y=P,
    mode='lines+markers',
    line=dict(
        color='red',
        width=3
    ),
    marker=dict(
        color='darkred',
        symbol='circle',
        size=6
    ),
    name='Modelo Logístico',
    hovertemplate='t: %{x:.1f}<br>P(t): %{y:.1f}<extra></extra>'
)

# Línea de capacidad de carga
trace_capacity = go.Scatter(
    x=t,
    y=[K] * len(t),
    mode='lines',
    line=dict(
        color='green',
        width=2,
        dash='dash'
    ),
    name=f'Capacidad de carga K = {K}',
    hovertemplate='Capacidad de carga: %{y}<extra></extra>'
)

# Crear la figura
fig_logistic = go.Figure(data=[trace_logistic, trace_capacity])
fig_logistic.update_layout(
    title=dict(
        text='<b>Crecimiento Poblacional con Capacidad de Carga</b>',
        font=dict(
            size=20,
            color='darkblue'
        ),
        x=0.5,
        y=0.93
    ),
    xaxis_title='Tiempo (t)',
    yaxis_title='Población P(t)',
    margin=dict(l=40, r=40, t=50, b=40),
    paper_bgcolor='lightyellow',
    plot_bgcolor='white',
    font=dict(
        family='Outfit',
        size=11,
        color='black'
    ),
    legend=dict(
        x=0.02,
        y=0.98,
        bgcolor='rgba(255,255,255,0.8)',
        bordercolor='black',
        borderwidth=1
    )
)
fig_logistic.update_xaxes(
    showgrid=True, gridwidth=1, gridcolor='lightgray',
    zeroline=True, zerolinewidth=1, zerolinecolor='black',
    showline=True, linecolor='black', linewidth=2, mirror=True,
)
fig_logistic.update_yaxes(
    showgrid=True, gridwidth=1, gridcolor='lightgray',
    zeroline=True, zerolinewidth=1, zerolinecolor='black',
    showline=True, linecolor='black', linewidth=2, mirror=True,
    range=[0, K * 1.1]  
)

############################

dash.register_page(__name__, path="/modelo-con-carga", name="Tarea 1")

layout = html.Div(children=[
    # Contenedor izquierdo
    html.Div(children=[
        html.H2("Crecimiento Poblacional con Capacidad de Carga"),
        dcc.Markdown("""
        El modelo de crecimiento exponencial es útil para describir el crecimiento poblacional 
        en condiciones ideales, pero en la realidad, los recursos son limitados. Para modelar 
        esta situación, utilizamos el **modelo logístico** que incorpora la **capacidad de carga** $K$.
        """, mathjax=True),

        dcc.Markdown("""
        La ecuación diferencial del modelo logístico es:

        $$\\frac{dP}{dt} = rP \\left(1 - \\frac{P}{K}\\right)$$

        donde:
        - $P(t)$ es la población en el tiempo $t$
        - $r$ es la tasa de crecimiento intrínseco
        - $K$ es la capacidad de carga (población máxima que el ambiente puede sostener)
        """, mathjax=True),

        dcc.Markdown("""
        La solución de esta ecuación diferencial es:

        $$P(t) = \\frac{K P_0 e^{rt}}{K + P_0 (e^{rt} - 1)}$$

        En este modelo:
        - $P_0 = 100$ (población inicial)
        - $r = 0.03$ (tasa de crecimiento)
        - $K = 1000$ (capacidad de carga)
        """, mathjax=True),

        dcc.Markdown("""
        **Características del modelo logístico:**
        - Crecimiento inicial similar al exponencial
        - Desaceleración del crecimiento cuando $P$ se aproxima a $K$
        - Estabilización en la capacidad de carga $K$
        - Comportamiento más realista que el modelo exponencial
        """, mathjax=True),
    ], className='content left'),

    # Contenedor derecho
    html.Div(children=[
        html.H2("Gráfica", className="title"),

        dcc.Graph(
            figure=fig_logistic,
            style={'height': '400px', 'width': '100%'},
        ),
    ], className='content right'),
], className='page-container')