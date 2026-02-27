import dash_bootstrap_components as dbc
from dash import html, dcc


def layout():
    return html.Div(
        [
            # ===== Top bar =====
            dbc.Row(
                [
                    dbc.Col(
                        html.H2("Cadastro de Funções (Mão de Obra)", className="mb-0"),
                        width=9,
                    ),
                    dbc.Col(
                        dbc.Button(
                            "Adicionar",
                            id="funcoes-btn-novo-top",
                            color="success",
                            className="w-100",
                        ),
                        width=3,
                    ),
                ],
                className="align-items-center mb-3",
            ),

            # ===== Corpo (filtros + cards) =====
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5("Filtros", className="card-title"),
                                    dbc.Input(
                                        id="funcoes-filter-descricao",
                                        placeholder="Buscar por descrição...",
                                        type="text",
                                    ),
                                    html.Div(style={"height": "12px"}),
                                    dbc.Button(
                                        "Buscar",
                                        id="funcoes-btn-buscar",
                                        color="primary",
                                        className="w-100",
                                    ),
                                ]
                            )
                        ),
                        width=3,
                    ),
                    dbc.Col(
                        dcc.Loading(html.Div(id="funcoes-cards-container"), type="default"),
                        width=9,
                    ),
                ],
                className="g-3",
            ),

            # ===== Modal (só abre ao clicar em Adicionar/Detalhe) =====
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle(id="funcoes-modal-title")),
                    dbc.ModalBody(html.Div(id="funcoes-modal-body")),
                    dbc.ModalFooter(
                        [
                            dbc.Button("Salvar", id="funcoes-btn-salvar", color="primary"),
                            dbc.Button("Fechar", id="funcoes-btn-fechar", color="secondary"),
                        ]
                    ),
                ],
                id="funcoes-modal",
                is_open=False,
                size="xl",
                scrollable=True,
            ),

            # ===== Toast =====
            dbc.Toast(
                id="funcoes-toast",
                header="SISROAD",
                is_open=False,
                dismissable=True,
                icon="primary",
                duration=4000,
                style={"position": "fixed", "top": 20, "right": 20, "width": 350},
            ),
        ]
    )