from dash import html, dcc


def build_layout():
    return html.Div(
        style={"maxWidth": "1100px", "margin": "20px auto", "fontFamily": "Arial"},
        children=[
            html.H2("SISROAD • MVP"),

            html.Div(
                style={"display": "grid", "gridTemplateColumns": "repeat(3, 1fr)", "gap": "10px"},
                children=[
                    dcc.Input(id="in-date", placeholder="Data (YYYY-MM-DD)", type="text"),
                    dcc.Input(id="in-road", placeholder="Rodovia (ex: BR-116)", type="text"),
                    dcc.Input(id="in-section", placeholder="Trecho (ex: km 16-17)", type="text"),
                    dcc.Input(id="in-defect", placeholder="Defeito (ex: buraco)", type="text"),
                    dcc.Input(id="in-sev", placeholder="Severidade (1-5)", type="number"),
                    dcc.Input(id="in-notes", placeholder="Observações", type="text"),
                ],
            ),

            html.Button("Salvar (mock)", id="btn-save", style={"marginTop": "10px"}),
            html.Div(id="save-msg", style={"marginTop": "8px"}),

            html.Hr(),
            dcc.Graph(id="chart-mock"),
        ],
    )
