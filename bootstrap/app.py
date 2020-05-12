import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly
import plotly.graph_objs as go

import pandas as pd
import numpy as np


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container(
    [
        #alerts
        html.Div(
            [
                dbc.Alert("This is a primary alert!", color="primary"),
                dbc.Alert("This is a secondar alert!", color="secondary"),
                dbc.Alert("This is a success alert! Hurray!", color="succees"),
                dbc.Alert("This is a Warning alert... be careful...", color="warning"),
                dbc.Alert("danger, danger, danger!!!", color="danger"),
                dbc.Alert("Info is very useful, so... Info Alert!!", color="info"),
                dbc.Alert("There is a light alert...", color="light"),
                dbc.Alert("... and a dark alert!", color="dark")
            ]
        ),
        html.Hr(),
        #badges
        dbc.Button(["Click me!", dbc.Badge("4", color="light", className="ml-1", id="badge-button")], color="primary", id="button")


    ]

)

@app.callback(
    Output("button", "children"),
    [Input("button", "n_clicks"),
    Input("badge-button","children")]
)
def update_badge(click, children):
    child = str(int(children)+1)
    return ["Click me!", dbc.Badge(child, color="light", className="ml-1", id="badge-button")]

if __name__ == "__main__":
    app.run_server(debug=True)
