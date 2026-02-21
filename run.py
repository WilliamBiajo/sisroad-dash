from dash import Dash
from app.layout import build_layout
from app.callbacks import register_callbacks


def create_app():
    app = Dash(__name__)
    app.title = "SISROAD"
    app.layout = build_layout()
    register_callbacks(app)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=8050)
