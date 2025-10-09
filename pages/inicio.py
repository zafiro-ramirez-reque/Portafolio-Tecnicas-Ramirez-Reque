import dash
from dash import html, dcc
import plotly.graph_objects as go

dash.register_page(__name__, path="/", name="Inicio")

layout = html.Div(children=[
    # Título principal
    html.Div(children=[
        html.H1("PORTFOLIO DIGITAL", className='main-title'),
        html.Hr(className='title-divider')
    ], className='title-container'),
    
    # Contenedor principal
    html.Div(children=[
        # Sección izquierda
        html.Div(children=[
            html.Div(children=[
                html.Div(children=[
                    html.Div(children=[
                        html.H2("INFORMACIÓN DEL ESTUDIANTE", className='section-header'),
                        html.Div(children=[
                            html.Div(children=[
                                html.Strong("Nombre:", className='label'),
                                html.Span("Zafiro Diokiar Elly Ramirez Reque", className='value')
                            ], className='data-row'),
                            html.Div(children=[
                                html.Strong("Código:", className='label'),
                                html.Span("23140386", className='value')
                            ], className='data-row'),
                            html.Div(children=[
                                html.Strong("Año Académico:", className='label'),
                                html.Span("2025", className='value')
                            ], className='data-row'),
                            html.Div(children=[
                                html.Strong("Ciclo:", className='label'),
                                html.Span("6to Ciclo", className='value')
                            ], className='data-row'),
                            html.Div(children=[
                                html.Strong("Carrera:", className='label'),
                                html.Span("Computación Científica", className='value')
                            ], className='data-row'),
                            html.Div(children=[
                                html.Strong("Universidad:", className='label'),
                                html.Span("Universidad Nacional Mayor de San Marcos", className='value')
                            ], className='data-row')
                        ], className='data-container')
                    ], className='personal-info-card')
                ], className='personal-info')
            ], className='student-section'),
            
            html.Div(children=[
                html.H2("DESCRIPCIÓN DEL PROYECTO", className='section-header'),
                html.Div(children=[
                    html.P("""
                        En este portafolio digital voy a presentar el desarrollo de la parte práctica 
                        del curso de Técnicas de Modelamiento Matemático. Aquí se mostrarán los diferentes 
                        modelos matemáticos implementados y analizados durante el desarrollo del curso.
                    """, className='description-text'),
                    html.P("""
                        Mediante el uso de herramientas computacionales para el análisis 
                        y visualización de resultados.
                    """, className='description-text')
                ], className='description-content')
            ], className='description-section')
        ], className='left-column'),  

        # Sección derecha
        html.Div(children=[
            html.Div(children=[
                html.Div(children=[
                    html.H2("INFORMACIÓN DEL CURSO", className='section-header'),
                    html.Div(children=[
                        html.H3("Profesores", className='professors-title'),
                        html.Div(children=[
                            html.Div(children=[
                                html.H4("Teoría", className='theory-label'),
                                html.P("Jhelly Reynaluz Perez Nuñez", className='professor-name'),
                                html.Div(className='professor-divider')
                            ], className='professor-card theory-card'),
                            
                            html.Div(children=[
                                html.H4("Práctica", className='practice-label'),
                                html.P("Yefri Ander Vidal Vega", className='professor-name'),
                                html.Div(className='professor-divider')
                            ], className='professor-card practice-card')
                        ], className='professors-container')
                    ], className='course-info-content')
                ], className='course-section')
            ], className='right-column-content')
        ], className='right-column')  
    ], className='main-container')  
], className='page-container')  