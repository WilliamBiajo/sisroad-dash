from dash import Input, Output, State
import plotly.express as px
import pandas as pd


def register_callbacks(app):

    @app.callback(
        Output("save-msg", "children"),
        Output("chart-mock", "figure"),
        Input("btn-save", "n_clicks"),
        State("in-date", "value"),
        State("in-road", "value"),
        State("in-section", "value"),
        State("in-defect", "value"),
        State("in-sev", "value"),
        State("in-notes", "value"),
        prevent_initial_call=True,
    )
    def save(_, date, road, section, defect, sev, notes):
        df = pd.DataFrame([
            {
                "date": date or "",
                "road": road or "",
                "section": section or "",
                "defect_type": defect or "",
                "severity": int(sev) if sev is not None else 0,
                "notes": notes or "",
            }
        ])
        fig = px.bar(df, x="defect_type", y="severity", title="Mock • Severidade por tipo (1 registro)")
        return "OK (ainda sem banco)", fig
