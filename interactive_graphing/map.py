import pandas as pd
import numpy as np
import json
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import datetime as dt
import locale

locale.setlocale(locale.LC_ALL, 'es-ES')

token = 'pk.eyJ1Ijoicml0bWFuZG90cHkiLCJhIjoiY2s3ZHJidGt0MDFjNzNmbGh5aDh4dTZ0OSJ9.-SROtN91ZvqtFpO1nGPFeg'

#loading comunas
with open('geojson/comunas.geojson') as json_file:
    geojson_comunas = json.load(json_file)

activos_df = pd.read_csv("https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/input/InformeEpidemiologico/CasosActualesPorComuna.csv")
confirmados_df =  pd.read_csv("https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/input/InformeEpidemiologico/CasosAcumuladosPorComuna.csv")
confirmados_df = confirmados_df.loc[:,list(activos_df.columns)]
#melting
activos = activos_df.melt(id_vars=["Region","Codigo region", "Comuna","Codigo comuna", "Poblacion"],
                          var_name="Fecha",
                          value_name="Activos")

confirmados = confirmados_df.melt(id_vars=["Region","Codigo region", "Comuna","Codigo comuna", "Poblacion"],
                                  var_name="Fecha",
                                  value_name="Confirmados")
df = confirmados.merge(activos).dropna()
df["Fecha"] = pd.to_datetime(df["Fecha"])
#transform every unique date to a number
numdate= [x for x in range(len(df['Fecha'].unique()))]
dates = df['Fecha'].unique()

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

app.layout=dbc.Container(
    [
        dbc.Row(
            dcc.RadioItems(
                options = [{'label':v, 'value':v} for v in ["Lineal", "Log"]],
                value = "Lineal",
                labelStyle={'display':'inline-block'},
                id = "radio"
            )
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                        id="scatter-graph",
                        hoverData={'points':[{"customdata": "Santiago"}]},
                        style={'height':'80vh'}
                    )
                ),
                dbc.Col(
                    [
                        dcc.Graph(id="graph-confirmados", style={'height':'40vh'}),
                        dcc.Graph(id='graph-activos', style={'height':'40vh'})
                    ]
                )
            ]
        ),
        html.Div(
            [
                html.Label("Filtrar por fecha:"),
                dcc.Slider(
                    id="slider",
                    min=numdate[0],
                    max=numdate[-1],
                    value=numdate[-1],
                    marks={numd:date.strftime('%d/%m') for numd,date in zip(numdate, df['Fecha'].dt.date.unique())},
                    step=1
                    )
            ]
        )
    ]
)

#slider + scatter callback
@app.callback(
    Output("scatter-graph","figure"),
    [Input("slider", "value")]
)
def update_scatter(fecha):
    dff = df[df["Fecha"]==dates[fecha]]
    day = pd.to_datetime(dates[fecha]).strftime("%d")
    month = pd.to_datetime(dates[fecha]).strftime("%B")
    fig = go.Figure(go.Choroplethmapbox(geojson=geojson_comunas, locations=dff.Comuna, z=dff["Confirmados"],
                                        colorscale="Reds", zmin=0, zmax=200, showscale = False, customdata=dff.Comuna,
                                        marker_opacity=0.9, marker_line_width=0.01, featureidkey='properties.comuna'))
    fig.update_layout(mapbox_style="light", mapbox_accesstoken=token, autosize = True)
    fig.update_layout(margin={"r":0,"t":45,"l":0,"b":0}, title_text = f"Casos confirmados acumulados al {day} de {month}")
    fig.update_layout(mapbox_zoom=3, mapbox_center = {"lat": -37.0902, "lon": -72.7129})

    return fig

def time_series(dff, mode, title, y):
    return {
        'data': [dict(
            x=dff["Fecha"],
            y=dff[y],
            mode='lines+markers'
        )],
        'layout': {
            'xaxis': {'showgrid':False},
            'yaxis': {'type': 'linear' if mode == 'Lineal' else 'log'},
            'title':title,
            'margin':{"r":0,"t":30,"l":40,"b":30}
            #'annotations':[ {'text':title}]
        }
    }

@app.callback(
        [Output('graph-confirmados', 'figure'), Output('graph-activos', 'figure')],
        [Input('scatter-graph', 'hoverData'), Input('radio', 'value')]
)

def update_time_series(hoverData, mode):
    comuna = hoverData['points'][0]['customdata']
    dff = df[df['Comuna'] == comuna]
    title1 = '<b>{}</b><br> Confirmados'.format(comuna)
    title2 = '<b>{}</b><br> Activos'.format(comuna)

    return [
        time_series(dff, mode, title1, "Confirmados"),
        time_series(dff, mode, title2, "Activos")
            ]

if __name__ == "__main__":
    app.run_server(debug=True)
