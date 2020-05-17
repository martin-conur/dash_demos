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
    [Input("slider", "value"),
    Input("radio", "value")]
)
def update_scatter(fecha, mode):
    dff = df[df["Fecha"]==dates[fecha]]

    return {
        "data":[
            dict(
            x=dff["Confirmados"],
            y=dff["Activos"],
            text=dff["Comuna"],
            customdata=dff["Comuna"],
            mode="markers",
            z=dff["Region"],
            marker=dict(
                size=15,
                opacity=0.7,
                line={'width':0.5, 'color':'white'},
                color=dff["Codigo region"]
            )
            )
        ],
        "layout":dict(
            xaxis={
                'title':'Casos Confirmados',
                'type': 'linear' if mode == 'Lineal' else 'log'
            },
            yaxis={
                'title': 'Casos Activos',
                'type': 'linear' if mode == 'Lineal'else 'log'
            },
            hovermode = 'closest',
            #margin = {"r":30,"t":40,"l":40,"b":40}

        )
    }
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
