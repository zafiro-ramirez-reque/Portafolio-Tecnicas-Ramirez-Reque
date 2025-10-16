import numpy as np
import plotly.graph_objects as go

def funcion_graficas_ecu_log(p0, r, k, t_max):
    # Generar los valores de tiempo
    t = np.linspace(0, t_max, 20)

    # Ecuacion
    P = (p0 * k * np.exp(r * t)) /((k - p0) + p0 * np.exp(r * t))

    # Crear gráfico de la poblacion
    trace_poblacion = go.Scatter(
        x=t,
        y=P,
        mode='lines+markers',
        name='Población P(t)',
        line=dict(
            color='black',
            width=2
        ),
        marker=dict(
            color='blue', 
            size=6, 
            symbol='circle'
        ),
        hovertemplate='t: %{x:.2f}<br>P(t): %{y:.2f}<extra></extra>'
    )

    # Crear gráfico de la capacidad de carga
    trace_capacidad = go.Scatter(
        x=[0, t_max],
        y=[k, k],
        mode='lines',
        name='Capacidad de carga K',
        line=dict(
            color='red',
            width=2,
            dash='dot'
        ),
        hovertemplate='K: %{y:.2f}<extra></extra>'
    )

    fig= go.Figure(data=[trace_poblacion, trace_capacidad])

    fig.update_layout(
        title=dict(
            text='<b>Modelo Logístico de crecimiento poblacional</b>',
            font=dict(
                size=20,
                color='green'
            ),
            x=0.5, 
            y=0.93
        ),
        xaxis_title='Tiempo (t)',
        yaxis_title='Población P(t)',
        margin=dict(l=40, r=40, t=70, b=40),
        paper_bgcolor='lightyellow',
        plot_bgcolor='white',
        font=dict(
            family='Outfit',
            size=11,
            color='black'
        ),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
        )
    )


    fig.update_xaxes(
        showgrid=True, gridwidth=1, gridcolor='lightpink',
        zeroline=True, zerolinewidth=2, zerolinecolor='red',
        showline=True, linecolor='black', linewidth=2, mirror=True,
        range=[0, t_max]
    )

    fig.update_yaxes(
        showgrid=True, gridwidth=1, gridcolor='lightpink',
        zeroline=True, zerolinewidth=2, zerolinecolor='red',
        showline=True, linecolor='black', linewidth=2, mirror=True,
        range=[0, k + k*0.1]
    )

    return fig
