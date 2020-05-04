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
dirname = os.path.dirname(__file__)
#path_d = os.path.join(dirname, 'diagnostics/')
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
                    dbc.Col(html.Img(src=app.get_asset_url('branding.png'), height='40px')),
                    dbc.Col(
                        dbc.NavbarBrand('Dash Storyboard', className='ml-2')
                    ),
                ],
                align='center',
                no_gutters=True,
            ),
        )
    ],
    color='primary',
    dark=True,
    sticky='top',
)



STORYBOARD_NAV = dbc.CardDeck(
    [
        dbc.Card(
            [
                dbc.Button(
                    children=[
                        html.H5('Solar Installations have increased in the last 4 years', className='card-title'),
                        html.P(
                            'This card has some text content, which is a little '
                            'bit longer than the second card.',
                            className='card-text',
                        )
                    ], style={'height': '100%' }, color = 'primary'
                )
            ]
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5('Penetration is largely focused in the midwest region', className='card-title'),
                    html.P(
                        'This card has some text content.',
                        className='card-text',
                    ),
                    dbc.Button(
                        'Click here', color='warning', className='mt-auto'
                    ),
                ]
            )
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5('Card 3', className='card-title'),
                    html.P(
                        'This card has some text content, which is longer '
                        'than both of the other two cards, in order to '
                        'demonstrate the equal height property of cards in a '
                        'card group.',
                        className='card-text',
                    ),
                    dbc.Button(
                        'Click here', color='danger', className='mt-auto'
                    ),
                ]
            )
        ),
    ]
)

STORYBOARD_CONTENT = [
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
                dbc.Col(dbc.Card(STORYBOARD_NAV)),
            ],
            style={'marginTop': 30},
        ),
        dbc.Row(
            [
                dbc.Col(dbc.Card(STORYBOARD_CONTENT))
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