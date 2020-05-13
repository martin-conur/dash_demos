import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly
import plotly.graph_objs as go

import pandas as pd
import numpy as np
import time


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container(
    [
        html.H1("Aprendiendo a usar dash-bootstrap-components"),
        html.Hr(),
        html.H3("Alertas"),
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
        html.H3("Botones"),
        #badges
        dbc.Button(["Click me!", dbc.Badge("4", color="light", className="ml-1", id="badge-button")],
                    color="primary", id="button", className="mt-auto"),
        dbc.Row(
            [
                dbc.Button("Regular", color="primary", className="mr-1"),
                dbc.Button("Active", color="primary", active=True, className="mr-1"),
                dbc.Button("Disabled", color="primary", disabled=True)

            ], align="center", justify="center", className="mt-auto"
        ),
        html.Hr(),
        html.H3("Grupo de botones (BottonGroup)"),
        dbc.Row(
            [
                dbc.ButtonGroup(
                    [
                        dbc.Button("First"),
                        dbc.Button("Second"),
                        dbc.Button("Third"),
                        dbc.Button("This Button is long"),
                        dbc.Button("This is also long"),
                        dbc.Button("another long???"),
                        dbc.DropdownMenu(
                            [
                                dbc.DropdownMenuItem("Item 1"),
                                dbc.DropdownMenuItem("Item 2"),
                                dbc.DropdownMenuItem("Item 3"),
                                dbc.DropdownMenuItem("This Item is long"),
                                dbc.DropdownMenuItem("This is also long"),
                                dbc.DropdownMenuItem("another long???")
                            ],
                            label="Menu",
                            group=True
                        )
                    ]
                )
            ], align="center", justify="center"
        ),
        html.Hr(),
        html.H3("Cards and CardDecks"),
        dbc.CardDeck(
            [
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H5("Card 1"),
                            html.P(
                                "This is some text inside a card...",
                                className="card-text"
                            ),
                            dbc.Button("Click me!", color="warning",className="mt-auto")
                        ]
                    )
                ),
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H5(" 2nd Card"),
                            html.P(
                                "More text on another card, the number 2",
                                className="card-text"
                            ),
                            dbc.Button("Click Here", color="success", className="mt-auto")
                        ]
                    )
                ),
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H5("Card number three"),
                            html.P(
                                "This is the last text of the last card, finally!",
                                className="card-text"
                            ),
                            dbc.Button("Don't Click me!", color="primary", className="mt-auto")

                        ]
                    )
                )
            ]
        ),
        html.Hr(),
        html.H3("Collapse"),
        dbc.Row(
            dbc.Col(
                [
                    dbc.Button(
                        "Collapse",
                        color="primary",
                        className="mb-3",
                        id="collapse-button"
                    ),
                    dbc.Collapse(
                        dbc.Card(
                            dbc.CardBody("This collapse content is hidden!!!")
                        ),
                        id="collapse"
                    )
                ]
            ), justify="center", align="center"
        ),
        html.Hr(),
        html.Div(
            [
                html.H3("Modals"),
                dbc.Row(
                    [
                        dbc.Button("Open modal", id="open"),
                        dbc.Modal(
                            [
                                dbc.ModalHeader("Modal Header"),
                                dbc.ModalBody("This is a modal, it has a header, a body (like this one) and a footer"),
                                dbc.ModalFooter(dbc.Button("Close", id="close", className="ml-auto"))
                            ], id="modal", centered=True
                        )
                    ],align="center", justify="center"
                )
            ], style={"textAlign":"center"}
        ),
        html.Hr(),

        html.Div(
            [
                html.H3("Navigation Bars"),
                html.H5("NavbarSimple"),
                dbc.NavbarSimple(
                    [
                        dbc.NavItem(dbc.Button("Button 1", color="primary")),
                        dbc.NavItem(dbc.Button("Button 2", color="primary")),
                        dbc.NavItem(dbc.Button("Button 3", color="primary")),
                        dbc.NavItem(dbc.Button("Button 3", color="primary")),
                        dbc.DropdownMenu(
                            [
                                dbc.DropdownMenuItem("Dropdown", header=True),
                                dbc.DropdownMenuItem("First item"),
                                dbc.DropdownMenuItem("Second Item"),
                                dbc.DropdownMenuItem("Third Item")

                            ],
                            nav=True,
                            in_navbar=True,
                            label="more"
                        )
                    ],
                    brand="covidatos.info",
                    brand_href="https://www.covidatos.info",
                    color="primary",
                    dark=True

                )
            ]
        ),
        html.Hr(),
        html.Div(
            [
                html.H3("Loading component"),
                dbc.Row(
                    dbc.Col(
                        [
                            dbc.Button("Loading Button", id="loading-button"),
                            dbc.Spinner(html.Div(id="loading-output"))
                        ]
                    )
                )
            ]
        ),

        html.Footer("This is a footer")


    ], fluid=True

)

@app.callback(
    Output("button", "children"),
    [Input("button", "n_clicks"),
    Input("badge-button","children")]
)
def update_badge(click, children):
    child = str(int(children)+1)
    return ["Click me!", dbc.Badge(child, color="light", className="ml-1", id="badge-button")]

@app.callback(
    Output("collapse","is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")]
)
def toggle_collapse(n_clicks,state):
    if n_clicks:
        return not state

@app.callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"),
    Input("close","n_clicks")],
    [State("modal","is_open")]
)

def modal_behavior(n1,n2,ms):
    if n1 or n2:
        return not ms

@app.callback(
    Output("loading-output", "children"),
    [Input("loading-button", "n_clicks")]
)
def loading(n):
    if n:
        time.sleep(2)
    return f"loaded {n} times!"

if __name__ == "__main__":
    app.run_server(debug=True)
