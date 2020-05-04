'''

Dash Storyboard Tempalte
Tony Du


Storyboard template for Dash web app

To-Do


'''






import pathlib
import os
import glob


import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import pandas as pd
import numpy as np
import json
import plotly.graph_objects as go
import plotly.express as px




# global vars
dir_absolute = 'C:/Users/tdu/python/python-diagnostics-dashboard/diagnostics/'
dirname = os.path.dirname(__file__)
path_d = os.path.join(dirname, 'diagnostics/')
#lst_rel = [f for f in os.listdir(relative_path) if f.endswith('.xlsx')]
#lst_rel = os.listdir(relative_path)
lst_baa = ['FG', 'DUK', 'ALGAMS']
lst_periods = ['S_SP1', 'S_SP2', 'S_P', 'S_OP', 'W_SP', 'W_P', 'W_OP', 'H_SP', 'H_P', 'H_OP']





app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server  # for Heroku deployment


NAVBAR = dbc.Navbar(
    children=[
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(html.Img(src=app.get_asset_url('cra-logo.png'), height='30px')),
                    dbc.Col(
                        dbc.NavbarBrand('Dash Storyboard', className='ml-2')
                    ),
                ],
                align='center',
                no_gutters=True,
            ),
        )
    ],
    color='light',
    #dark=True,
    sticky='top',
)

LEFT_COLUMN = dbc.Jumbotron(
    [
        dcc.Loading(
            id = 'loading-inputs',
            children = [
                html.Div(id='store-df', style={'display' : 'none'}),
                dbc.Container(
                    [
                        html.H4(children='Inputs', className='display-5', style = {'fontSize': 36}),
                        html.Hr(className='my-2'),
                        html.Label('Select diagnostics file', className='lead'),
                        dcc.Dropdown(
                            id='file-drop', clearable=False, style = {'marginBottom': 10, 'fontSize': 14},
                            #options=[{'label':i, 'value':i} for i in os.listdir(dir_diagnostics)]
                            options=[{'label':i, 'value':i} for i in [f for f in os.listdir(path_d) if f.endswith('.xlsx')]]
                        ),
                        dbc.Button('Import', id = 'import-btn', color = 'primary', className = 'mr-1', n_clicks = 0, disabled = True),
                        html.Div(style = {'marginBottom':25}),
                        html.Label('Select BAA', className='lead'),
                        dcc.Dropdown(
                            id ='baa-drop', clearable = False, style={'marginBottom': 25}, disabled = True
                        ),
                        html.Label('Select Period', className='lead'),
                        dcc.Dropdown(
                            id ='period-drop', clearable = False, style={'marginBottom': 0}, disabled = True,
                            options = [{'label':i, 'value':i} for i in lst_periods]
                        )
                    ], fluid = True
                )
            ]

        )
    ],fluid = True
)


MMSUMMARY_PLOT = [
    dbc.CardHeader(html.H5('Mmfile Summary')),
    dbc.CardBody(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dcc.Tabs(
                                id='top-tabs',
                                children=[
                                    dcc.Tab(
                                        label='Generation',
                                        children=[
                                            dcc.Loading(
                                                id='loading-gen',
                                                children=[
                                                    dbc.Row(
                                                        children=[
                                                            dbc.Col(html.P(children='Utilities to include'), md = 1),
                                                            dbc.Col(
                                                                dbc.InputGroup(
                                                                    children=[
                                                                        dbc.Input(id='gen-input', type='number', min='1', max='20', value=5),
                                                                        dbc.InputGroupAddon(
                                                                            dbc.Button(id='gen-submit-btn', children='Update', color='primary'),
                                                                            addon_type='append'
                                                                        )
                                                                    ]
                                                                ), md=2
                                                            ),
                                                        ]
                                                    ),
                                                    dbc.Row(
                                                        dbc.Col(children=[dcc.Graph(id='gen-graph')], md=12)
                                                    )
                                                    #dcc.Graph(id='gen-graph')
                                                ], 
                                                type='default',
                                            )
                                        ],
                                    ),
                                    dcc.Tab(
                                        label='Load',
                                        children=[
                                            dcc.Loading(
                                                id='loading-load',
                                                children=[dcc.Graph(id='load-graph')],
                                                type='default',
                                            )
                                        ],
                                    ),
                                    dcc.Tab(
                                        label='Transmission',
                                        children=[
                                            dcc.Loading(
                                                id ='loading-transmission',
                                                children = [dcc.Graph(id='tx-graph')],
                                                type = 'default',
                                            )
                                        ],
                                    ),
                                ],
                            )
                        ],
                        #md=12,
                    ),
                ]
            )
        ]
    ),
]


BOTTOM_PLOTS = [
    dbc.CardHeader(html.H5('Additional Diagnostics')),
    dbc.CardBody(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dcc.Tabs(
                                id='bottom-tabs',
                                children=[
                                    dcc.Tab(
                                        label='Top Players',
                                        children=[
                                            dcc.Loading(
                                                id='loading-hhi',
                                                children=[
                                                    dbc.Row(
                                                        children=[
                                                            dbc.Col(html.P(children='Top players to include'), md = 1),
                                                            dbc.Col(
                                                                dbc.InputGroup(
                                                                    children=[
                                                                        dbc.Input(id='hhi-input', type='number', min='1', max='20', value=10),
                                                                        dbc.InputGroupAddon(
                                                                            dbc.Button(id='hhi-submit-btn', children='Update', color='primary'),
                                                                            addon_type='append'
                                                                        )
                                                                    ]
                                                                ), md=2
                                                            ),
                                                        ],style = {'marginTop' : 10}
                                                    ),
                                                    dbc.Row(
                                                        children=[
                                                            dbc.Col(dcc.Graph(id='hhi-bar'), md=6),
                                                            dbc.Col(dcc.Graph(id='hhi-pie'), md=6)
                                                        ]

                                                    )
                                                ], 
                                                type='default',
                                            )
                                        ],
                                    ),
                                    dcc.Tab(
                                        label='Supply Curve',
                                        children=[
                                            dcc.Loading(
                                                id='loading-supply',
                                                children=[
                                                    dbc.Row(
                                                        children=[
                                                            dbc.Col(dcc.Dropdown(id='supply-owner-drop', clearable=False), md=4)
                                                        ]
                                                    ),
                                                    dbc.Row(
                                                        children=[
                                                            dbc.Col(dcc.Graph(id='supply-graph'))
                                                        ]

                                                    )
                                                ]
                                            )
                                        ], 
                                    ),
                                    dcc.Tab(
                                        label='Phase3X4X',
                                        children=[
                                            dcc.Loading(
                                                id='loading-phase',
                                                children=[
                                                    dbc.Row(
                                                        children=[
                                                            dbc.Col(dcc.Dropdown(id='phase-utility-drop', clearable=False), md=4)
                                                        ]
                                                    ),
                                                    dbc.Row(
                                                        children=[
                                                            dbc.Col(dcc.Graph(id='phase-graph'))
                                                        ]
                                                    )
                                                ]
                                            )

                                        ], 
                                    ),
                                ],
                            )
                        ],
                    ),
                ]
            )
        ]
    ),
]


BODY = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(LEFT_COLUMN, md=3, align='center'),
                dbc.Col(dbc.Card(MMSUMMARY_PLOT), md=9),
            ],
            style={'marginTop': 30},
        ),
        dbc.Row(
            [
                dbc.Col(dbc.Card(BOTTOM_PLOTS))
            ],
            style={'marginTop': 30},
        ),
    ],
    className='mt-12', fluid = True
)


app.title = 'Diagnostics Dashboard'
app.layout = html.Div(children=[NAVBAR, BODY])
if __name__ == '__main__':
    app.run_server(host='127.0.0.1', port='8050', debug=True)