import dash
import dash_bootstrap_components as dbc
from dash import html, Input, Output, State, ALL, ctx, no_update

from infra.services.funcoes_service import (
    list_funcoes_cards,
    get_funcao_detail,
    save_funcao,
)

from infra.loaders.excel_fields import get_excel_schema  # usa schema do Excel


def _render_card(row: dict):
    return dbc.Card(
        dbc.CardBody(
            [
                html.H5(row.get("descricao", "-"), className="mb-2"),
                html.Div(f"Salário: {row.get('salario', '-')}", className="text-muted"),
                html.Div(f"Início: {row.get('inicio', '-')}", className="text-muted"),
                html.Div(f"Fim: {row.get('fim', '-')}", className="text-muted"),
                html.Hr(),
                dbc.Button(
                    "Detalhe",
                    id={"type": "funcoes-btn-detalhes", "id": row.get("id")},
                    color="secondary",
                    className="w-100",
                ),
            ]
        ),
        className="mb-3",
    )


def _is_bit(sql_type: str) -> bool:
    return "BIT" in (sql_type or "").upper()


def _is_number(sql_type: str) -> bool:
    t = (sql_type or "").upper()
    return any(x in t for x in ["INT", "DECIMAL", "NUMERIC", "FLOAT", "REAL", "MONEY"])


def _is_date(sql_type: str) -> bool:
    t = (sql_type or "").upper()
    return "DATE" in t and "TIME" not in t


def _input(field_name: str, sql_type: str, value):
    # Checkbox para BIT
    if _is_bit(sql_type):
        checked = bool(value) if value not in ("", None) else False
        return dbc.Checkbox(
            id={"type": "funcoes-form-bool", "field": field_name},
            value=checked,
        )

    # Datas
    if _is_date(sql_type):
        # espera YYYY-MM-DD
        v = "" if value in (None, "") else str(value)[:10]
        return dbc.Input(
            id={"type": "funcoes-form", "field": field_name},
            type="date",
            value=v,
            placeholder=sql_type,
        )

    # Números
    if _is_number(sql_type):
        return dbc.Input(
            id={"type": "funcoes-form", "field": field_name},
            type="number",
            value="" if value is None else value,
            placeholder=sql_type,
        )

    # Texto
    return dbc.Input(
        id={"type": "funcoes-form", "field": field_name},
        type="text",
        value="" if value is None else value,
        placeholder=sql_type,
    )


def _build_form(schema: list[dict], data: dict | None):
    data = data or {}
    fields = [f for f in schema if f["name"].lower() != "id"]

    mid = (len(fields) + 1) // 2
    left = fields[:mid]
    right = fields[mid:]

    def col_block(items):
        blocks = []
        for f in items:
            name = f["name"]
            sql = f["sql"]
            val = data.get(name, "")

            blocks.append(
                dbc.Row(
                    [
                        dbc.Col(dbc.Label(name), width=5),
                        dbc.Col(_input(name, sql, val), width=7),
                    ],
                    className="mb-2",
                )
            )
        return blocks

    return dbc.Container(
        dbc.Row(
            [
                dbc.Col(col_block(left), width=6),
                dbc.Col(col_block(right), width=6),
            ],
            className="g-3",
        ),
        fluid=True,
    )


def register_funcoes_callbacks(app: dash.Dash):
    if getattr(app, "_sisroad_funcoes_callbacks_registered", False):
        return
    setattr(app, "_sisroad_funcoes_callbacks_registered", True)

    # 1) Carregar cards (inicial + buscar + após salvar)
    @app.callback(
        Output("funcoes-cards-container", "children"),
        Input("funcoes-btn-buscar", "n_clicks"),
        Input("funcoes-toast", "is_open"),
        prevent_initial_call=False,
    )
    def load_cards(_n_buscar, _toast_open):
        rows = list_funcoes_cards()
        if not rows:
            return dbc.Alert("Nenhum registro encontrado.", color="secondary")
        return [_render_card(r) for r in rows]

    # 2) Controller do modal (abre somente por clique)
    @app.callback(
        Output("funcoes-modal", "is_open"),
        Output("funcoes-modal-body", "children"),
        Output("funcoes-modal-title", "children"),
        Output("store-selected-id", "data"),
        Output("funcoes-toast", "is_open"),
        Output("funcoes-toast", "children"),
        Input("funcoes-btn-novo-top", "n_clicks"),
        Input({"type": "funcoes-btn-detalhes", "id": ALL}, "n_clicks"),
        Input("funcoes-btn-fechar", "n_clicks"),
        Input("funcoes-btn-salvar", "n_clicks"),
        State("funcoes-modal", "is_open"),
        State("store-selected-id", "data"),
        State({"type": "funcoes-form", "field": ALL}, "value"),
        State({"type": "funcoes-form", "field": ALL}, "id"),
        State({"type": "funcoes-form-bool", "field": ALL}, "value"),
        State({"type": "funcoes-form-bool", "field": ALL}, "id"),
        prevent_initial_call=True,
    )
    def modal_controller(
        _novo, _detalhes, _fechar, _salvar,
        is_open, selected_id,
        values, ids,
        bool_values, bool_ids
    ):
        trigger = ctx.triggered_id

        # FECHAR
        if trigger == "funcoes-btn-fechar":
            return False, no_update, no_update, no_update, no_update, no_update

        # NOVO (somente se clicou)
        if trigger == "funcoes-btn-novo-top":
            detail = get_funcao_detail(None)
            form = _build_form(detail["schema"], detail["data"])
            return True, form, detail["title"], None, no_update, no_update

        # DETALHE (somente se clicou)
        if isinstance(trigger, dict) and trigger.get("type") == "funcoes-btn-detalhes":
            func_id = trigger.get("id")
            detail = get_funcao_detail(func_id)
            form = _build_form(detail["schema"], detail["data"])
            return True, form, detail["title"], func_id, no_update, no_update

        # SALVAR
        if trigger == "funcoes-btn-salvar":
            try:
                payload = {}

                # campos normais
                for v, i in zip(values, ids):
                    payload[i["field"]] = v

                # campos booleanos (checkbox)
                for v, i in zip(bool_values, bool_ids):
                    payload[i["field"]] = 1 if v else 0

                saved_id = save_funcao(selected_id, payload)
                return False, no_update, no_update, saved_id, True, f"Salvo com sucesso (id={saved_id})."
            except Exception as e:
                return is_open, no_update, no_update, selected_id, True, f"Erro ao salvar: {e}"

        return is_open, no_update, no_update, selected_id, no_update, no_update