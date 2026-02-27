from dash import html
from app.layout.sidebar import sidebar


def shell(content):
    return html.Div([
        sidebar(),
        html.Div(content, className='content'),
    ], className='app-shell')
