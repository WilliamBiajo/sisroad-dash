import dash_bootstrap_components as dbc
from dash import html


def sidebar():
    return html.Div([
        html.Div('SISROAD', className='sidebar-title'),
        html.Hr(),
        dbc.Nav([
            dbc.NavLink('Home', href='/', active='exact'),
            dbc.NavLink('Funções (M.O.)', href='/funcoes', active='exact'),
        ], vertical=True, pills=True),
    ], className='sidebar')
