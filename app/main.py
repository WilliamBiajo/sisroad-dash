import dash
import dash_bootstrap_components as dbc
from dash import html, dcc

from app.layout.shell import shell
from app.pages.home import layout as home_layout
from app.pages.funcoes import layout as funcoes_layout
from app.callbacks.funcoes_cb import register_funcoes_callbacks


def create_app() -> dash.Dash:
    app = dash.Dash(
        __name__,
        external_stylesheets=[dbc.themes.BOOTSTRAP],
        suppress_callback_exceptions=True,
    )
    app.title = 'SISROAD'

    app.layout = html.Div([
        dcc.Location(id='url'),
        dcc.Store(id='store-selected-id'),
        shell(html.Div(id='page-container')),
    ])

    register_funcoes_callbacks(app)

    @app.callback(
        dash.Output('page-container', 'children'),
        dash.Input('url', 'pathname'),
    )
    def router(pathname: str):
        if pathname in (None, '/', '/home'):
            return home_layout()
        if pathname == '/funcoes':
            return funcoes_layout()
        return html.Div([html.H3('404'), html.P(f'Rota não encontrada: {pathname}')])

    return app
