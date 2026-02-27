from pathlib import Path

# ====== CONFIG DO SEU SQL SERVER (como você passou) ======
DB_HOST = "127.0.0.1"
DB_PORT = "1433"
DB_DATABASE = "master"
DB_USER = "dbeaver"
DB_PASSWORD = "NovaSenhaForte@123"
DB_DRIVER = "ODBC Driver 18 for SQL Server"
DB_TRUST_CERT = "yes"


def write_text(path: Path, content: str, overwrite: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if overwrite or not path.exists():
        path.write_text(content, encoding="utf-8")


def main() -> None:
    root = Path.cwd()

    # ========= Arquivos do projeto (sem triple-quote problem) =========
    files: dict[str, str] = {}

    # --- Root ---
    files["run.py"] = (
        "from app.main import create_app\n\n"
        "app = create_app()\n"
        "server = app.server\n\n"
        "if __name__ == '__main__':\n"
        "    app.run_server(host='0.0.0.0', port=8050, debug=True)\n"
    )

    files["requirements.txt"] = (
        "dash\n"
        "dash-bootstrap-components\n"
        "pandas\n"
        "openpyxl\n"
        "python-dotenv\n"
        "sqlalchemy\n"
        "pyodbc\n"
        "pydantic\n"
    )

    files[".gitignore"] = (
        ".venv/\n"
        ".env\n"
        "__pycache__/\n"
        "*.pyc\n"
        "*.log\n"
    )

    # README sem ``` para evitar qualquer confusão; depois você edita à vontade
    files["README.md"] = (
        "# SISROAD Dash\n\n"
        "## Rodar (Codespaces / Linux)\n\n"
        "1) Criar venv:\n"
        "   python -m venv .venv\n"
        "2) Ativar:\n"
        "   source .venv/bin/activate\n"
        "3) Instalar deps:\n"
        "   pip install -r requirements.txt\n"
        "4) Configurar env:\n"
        "   cp .env.example .env\n"
        "5) Rodar:\n"
        "   python run.py\n"
    )

    # --- App ---
    files["app/__init__.py"] = ""

    files["app/main.py"] = (
        "import dash\n"
        "import dash_bootstrap_components as dbc\n"
        "from dash import html, dcc\n\n"
        "from app.layout.shell import shell\n"
        "from app.pages.home import layout as home_layout\n"
        "from app.pages.funcoes import layout as funcoes_layout\n"
        "from app.callbacks.funcoes_cb import register_funcoes_callbacks\n\n\n"
        "def create_app() -> dash.Dash:\n"
        "    app = dash.Dash(\n"
        "        __name__,\n"
        "        external_stylesheets=[dbc.themes.BOOTSTRAP],\n"
        "        suppress_callback_exceptions=True,\n"
        "    )\n"
        "    app.title = 'SISROAD'\n\n"
        "    app.layout = html.Div([\n"
        "        dcc.Location(id='url'),\n"
        "        dcc.Store(id='store-selected-id'),\n"
        "        shell(html.Div(id='page-container')),\n"
        "    ])\n\n"
        "    register_funcoes_callbacks(app)\n\n"
        "    @app.callback(\n"
        "        dash.Output('page-container', 'children'),\n"
        "        dash.Input('url', 'pathname'),\n"
        "    )\n"
        "    def router(pathname: str):\n"
        "        if pathname in (None, '/', '/home'):\n"
        "            return home_layout()\n"
        "        if pathname == '/funcoes':\n"
        "            return funcoes_layout()\n"
        "        return html.Div([html.H3('404'), html.P(f'Rota não encontrada: {pathname}')])\n\n"
        "    return app\n"
    )

    # --- Layout ---
    files["app/layout/__init__.py"] = ""

    files["app/layout/shell.py"] = (
        "from dash import html\n"
        "from app.layout.sidebar import sidebar\n\n\n"
        "def shell(content):\n"
        "    return html.Div([\n"
        "        sidebar(),\n"
        "        html.Div(content, className='content'),\n"
        "    ], className='app-shell')\n"
    )

    files["app/layout/sidebar.py"] = (
        "import dash_bootstrap_components as dbc\n"
        "from dash import html\n\n\n"
        "def sidebar():\n"
        "    return html.Div([\n"
        "        html.Div('SISROAD', className='sidebar-title'),\n"
        "        html.Hr(),\n"
        "        dbc.Nav([\n"
        "            dbc.NavLink('Home', href='/', active='exact'),\n"
        "            dbc.NavLink('Funções (M.O.)', href='/funcoes', active='exact'),\n"
        "        ], vertical=True, pills=True),\n"
        "    ], className='sidebar')\n"
    )

    # --- Pages ---
    files["app/pages/__init__.py"] = ""

    files["app/pages/home.py"] = (
        "from dash import html\n\n\n"
        "def layout():\n"
        "    return html.Div([\n"
        "        html.H2('Home'),\n"
        "        html.P('Projeto reconstruído do zero. Próximo passo: CRUD de Funções (Mão de Obra).'),\n"
        "    ])\n"
    )

    files["app/pages/funcoes.py"] = (
        "import dash_bootstrap_components as dbc\n"
        "from dash import html, dcc\n\n\n"
        "def layout():\n"
        "    return html.Div([\n"
        "        html.H2('Cadastro de Funções (Mão de Obra)'),\n"
        "        dbc.Row([\n"
        "            dbc.Col(\n"
        "                dbc.Card(dbc.CardBody([\n"
        "                    html.H5('Filtros', className='card-title'),\n"
        "                    dbc.Input(id='funcoes-filter-descricao', placeholder='Buscar por descrição...', type='text'),\n"
        "                    html.Div(style={'height': '12px'}),\n"
        "                    dbc.Button('Buscar', id='funcoes-btn-buscar', color='primary', className='w-100'),\n"
        "                    html.Hr(),\n"
        "                    dbc.Button('Novo Registro', id='funcoes-btn-novo', color='success', className='w-100'),\n"
        "                ])),\n"
        "                width=3,\n"
        "            ),\n"
        "            dbc.Col(\n"
        "                html.Div([\n"
        "                    dcc.Loading(html.Div(id='funcoes-cards-container'), type='default')\n"
        "                ]),\n"
        "                width=9,\n"
        "            ),\n"
        "        ], className='g-3'),\n\n"
        "        dbc.Modal([\n"
        "            dbc.ModalHeader(dbc.ModalTitle('Detalhes da Função')),\n"
        "            dbc.ModalBody(html.Div(id='funcoes-modal-body')),\n"
        "            dbc.ModalFooter([\n"
        "                dbc.Button('Salvar', id='funcoes-btn-salvar', color='primary'),\n"
        "                dbc.Button('Excluir', id='funcoes-btn-excluir', color='danger'),\n"
        "                dbc.Button('Fechar', id='funcoes-btn-fechar', color='secondary'),\n"
        "            ]),\n"
        "        ], id='funcoes-modal', is_open=False, size='xl', scrollable=True),\n\n"
        "        dbc.Toast(\n"
        "            id='funcoes-toast',\n"
        "            header='SISROAD',\n"
        "            is_open=False,\n"
        "            dismissable=True,\n"
        "            icon='primary',\n"
        "            duration=4000,\n"
        "            style={'position': 'fixed', 'top': 20, 'right': 20, 'width': 350},\n"
        "        ),\n"
        "    ])\n"
    )

    # --- Callbacks ---
    files["app/callbacks/__init__.py"] = ""

    files["app/callbacks/funcoes_cb.py"] = (
        "import dash\n"
        "import dash_bootstrap_components as dbc\n"
        "from dash import html, Input, Output, State, ALL, ctx\n\n"
        "from infra.services.funcoes_service import (\n"
        "    list_funcoes_cards,\n"
        "    get_funcao_detail,\n"
        "    upsert_funcao,\n"
        "    delete_funcao,\n"
        ")\n\n\n"
        "def _render_card(row: dict):\n"
        "    return dbc.Card(\n"
        "        dbc.CardBody([\n"
        "            html.H5(row.get('descricao', '-'), className='mb-2'),\n"
        "            html.Div(f\"Salário: {row.get('salario', '-')}\" , className='text-muted'),\n"
        "            html.Div(f\"Início: {row.get('inicio', '-')}\" , className='text-muted'),\n"
        "            html.Div(f\"Fim: {row.get('fim', '-')}\" , className='text-muted'),\n"
        "            html.Hr(),\n"
        "            dbc.Button(\n"
        "                'Detalhes',\n"
        "                id={'type': 'funcoes-btn-detalhes', 'id': row.get('id')},\n"
        "                color='secondary',\n"
        "                className='w-100'\n"
        "            ),\n"
        "        ]),\n"
        "        className='mb-3',\n"
        "    )\n\n\n"
        "def register_funcoes_callbacks(app: dash.Dash):\n"
        "    @app.callback(\n"
        "        Output('funcoes-cards-container', 'children'),\n"
        "        Input('funcoes-btn-buscar', 'n_clicks'),\n"
        "        State('funcoes-filter-descricao', 'value'),\n"
        "        prevent_initial_call=False,\n"
        "    )\n"
        "    def load_cards(_n, descricao):\n"
        "        rows = list_funcoes_cards(descricao=descricao)\n"
        "        if not rows:\n"
        "            return dbc.Alert('Nenhum registro encontrado.', color='secondary')\n"
        "        return [_render_card(r) for r in rows]\n\n"
        "    @app.callback(\n"
        "        Output('funcoes-modal', 'is_open'),\n"
        "        Output('funcoes-modal-body', 'children'),\n"
        "        Output('store-selected-id', 'data'),\n"
        "        Input('funcoes-btn-novo', 'n_clicks'),\n"
        "        Input({'type': 'funcoes-btn-detalhes', 'id': ALL}, 'n_clicks'),\n"
        "        Input('funcoes-btn-fechar', 'n_clicks'),\n"
        "        State('funcoes-modal', 'is_open'),\n"
        "        prevent_initial_call=True,\n"
        "    )\n"
        "    def open_close_modal(_novo, _detalhes, _fechar, is_open):\n"
        "        trigger = ctx.triggered_id\n"
        "        if trigger == 'funcoes-btn-fechar':\n"
        "            return False, dash.no_update, None\n"
        "        if trigger == 'funcoes-btn-novo':\n"
        "            detail = get_funcao_detail(None)\n"
        "            return True, detail['form'], None\n"
        "        if isinstance(trigger, dict) and trigger.get('type') == 'funcoes-btn-detalhes':\n"
        "            func_id = trigger.get('id')\n"
        "            detail = get_funcao_detail(func_id)\n"
        "            return True, detail['form'], func_id\n"
        "        return is_open, dash.no_update, dash.no_update\n\n"
        "    @app.callback(\n"
        "        Output('funcoes-toast', 'is_open'),\n"
        "        Output('funcoes-toast', 'children'),\n"
        "        Input('funcoes-btn-salvar', 'n_clicks'),\n"
        "        State('store-selected-id', 'data'),\n"
        "        prevent_initial_call=True,\n"
        "    )\n"
        "    def save_funcao(_n, selected_id):\n"
        "        try:\n"
        "            upsert_funcao(selected_id, payload={})\n"
        "            return True, 'Salvo com sucesso (estrutura base).'\n"
        "        except Exception as e:\n"
        "            return True, f'Erro ao salvar: {e}'\n\n"
        "    @app.callback(\n"
        "        Output('funcoes-toast', 'is_open'),\n"
        "        Output('funcoes-toast', 'children'),\n"
        "        Output('funcoes-modal', 'is_open'),\n"
        "        Input('funcoes-btn-excluir', 'n_clicks'),\n"
        "        State('store-selected-id', 'data'),\n"
        "        prevent_initial_call=True,\n"
        "    )\n"
        "    def delete_funcao_cb(_n, selected_id):\n"
        "        try:\n"
        "            delete_funcao(selected_id)\n"
        "            return True, 'Excluído com sucesso.', False\n"
        "        except Exception as e:\n"
        "            return True, f'Erro ao excluir: {e}', dash.no_update\n"
    )

    # --- Assets ---
    files["app/assets/styles.css"] = (
        ".app-shell{ display:flex; min-height:100vh; }\n"
        ".sidebar{ width:260px; background:#2f6375; padding:18px; color:white; }\n"
        ".sidebar-title{ font-weight:700; letter-spacing:2px; margin-bottom:8px; }\n"
        ".content{ flex:1; background:#efefef; padding:22px; }\n"
    )

    # --- Domain ---
    files["domain/__init__.py"] = ""
    files["domain/models/__init__.py"] = ""
    files["domain/models/funcao.py"] = (
        "from pydantic import BaseModel, Field\n"
        "from typing import Optional\n"
        "from datetime import date\n\n\n"
        "class Funcao(BaseModel):\n"
        "    id: Optional[int] = None\n"
        "    descricao: str = Field(..., min_length=1)\n"
        "    salario: Optional[float] = None\n"
        "    inicio: Optional[date] = None\n"
        "    fim: Optional[date] = None\n"
        "    extras: dict = {}\n"
    )
    files["domain/schemas/__init__.py"] = ""
    files["domain/schemas/excel_mo_schema.py"] = "EXCEL_FILE = 'Campos_tabela_de_MO_otimizado.xlsx'\n"

    # --- Infra ---
    files["infra/__init__.py"] = ""
    files["infra/db/__init__.py"] = ""
    files["infra/db/engine.py"] = (
        "import os\n"
        "import urllib.parse\n"
        "from dotenv import load_dotenv\n"
        "from sqlalchemy import create_engine\n\n"
        "load_dotenv()\n\n\n"
        "def get_engine():\n"
        "    driver = os.getenv('SQLSERVER_DRIVER', 'ODBC Driver 18 for SQL Server')\n"
        "    server = os.getenv('SQLSERVER_HOST', '127.0.0.1')\n"
        "    port = os.getenv('SQLSERVER_PORT', '1433')\n"
        "    database = os.getenv('SQLSERVER_DATABASE', 'master')\n"
        "    user = os.getenv('SQLSERVER_USER', 'dbeaver')\n"
        "    password = os.getenv('SQLSERVER_PASSWORD', '')\n"
        "    trust_cert = os.getenv('SQLSERVER_TRUST_CERT', 'yes').lower() in ('1','true','yes')\n\n"
        "    odbc = (\n"
        "        f\"DRIVER={{{driver}}};\"\n"
        "        f\"SERVER={server},{port};\"\n"
        "        f\"DATABASE={database};\"\n"
        "        f\"UID={user};\"\n"
        "        f\"PWD={password};\"\n"
        "        f\"Encrypt=yes;\"\n"
        "        f\"TrustServerCertificate={'yes' if trust_cert else 'no'};\"\n"
        "    )\n"
        "    params = urllib.parse.quote_plus(odbc)\n"
        "    return create_engine(f\"mssql+pyodbc:///?odbc_connect={params}\", pool_pre_ping=True)\n"
    )

    files["infra/repositories/__init__.py"] = ""
    files["infra/repositories/funcoes_repo.py"] = (
        "from sqlalchemy import text\n"
        "from infra.db.engine import get_engine\n\n"
        "TABLE = 'dbo.funcoes'  # vamos criar depois a tabela baseada no Excel\n\n\n"
        "def list_funcoes(descricao: str | None = None):\n"
        "    engine = get_engine()\n"
        "    q = 'SELECT TOP 200 * FROM ' + TABLE\n"
        "    params = {}\n"
        "    if descricao:\n"
        "        q += ' WHERE descricao LIKE :desc'\n"
        "        params['desc'] = f\"%{descricao}%\"\n"
        "    q += ' ORDER BY descricao'\n"
        "    with engine.begin() as conn:\n"
        "        rows = conn.execute(text(q), params).mappings().all()\n"
        "    return [dict(r) for r in rows]\n\n\n"
        "def delete_funcao(func_id: int):\n"
        "    engine = get_engine()\n"
        "    q = 'DELETE FROM ' + TABLE + ' WHERE id = :id'\n"
        "    with engine.begin() as conn:\n"
        "        conn.execute(text(q), {'id': func_id})\n"
    )

    files["infra/services/__init__.py"] = ""
    files["infra/services/funcoes_service.py"] = (
        "from infra.repositories.funcoes_repo import list_funcoes, delete_funcao as repo_delete\n\n\n"
        "def list_funcoes_cards(descricao: str | None = None):\n"
        "    rows = list_funcoes(descricao=descricao)\n"
        "    cards = []\n"
        "    for r in rows:\n"
        "        cards.append({\n"
        "            'id': r.get('id'),\n"
        "            'descricao': r.get('descricao') or r.get('Descricao') or '-',\n"
        "            'salario': r.get('salario') or r.get('Salario') or '-',\n"
        "            'inicio': r.get('inicio') or r.get('Inicio') or '-',\n"
        "            'fim': r.get('fim') or r.get('Fim') or '-',\n"
        "        })\n"
        "    return cards\n\n\n"
        "def get_funcao_detail(func_id):\n"
        "    return {'form': 'Formulário será gerado pelo schema do Excel.'}\n\n\n"
        "def upsert_funcao(func_id, payload: dict):\n"
        "    return True\n\n\n"
        "def delete_funcao(func_id):\n"
        "    if not func_id:\n"
        "        raise ValueError('Nenhum ID selecionado')\n"
        "    repo_delete(func_id)\n"
    )

    # ========= .env.example e .env =========
    env_example = (
        f"SQLSERVER_HOST={DB_HOST}\n"
        f"SQLSERVER_PORT={DB_PORT}\n"
        f"SQLSERVER_DATABASE={DB_DATABASE}\n"
        f"SQLSERVER_USER={DB_USER}\n"
        "SQLSERVER_PASSWORD=__PUT_PASSWORD_HERE__\n"
        f"SQLSERVER_DRIVER={DB_DRIVER}\n"
        f"SQLSERVER_TRUST_CERT={DB_TRUST_CERT}\n"
    )

    env_real = (
        f"SQLSERVER_HOST={DB_HOST}\n"
        f"SQLSERVER_PORT={DB_PORT}\n"
        f"SQLSERVER_DATABASE={DB_DATABASE}\n"
        f"SQLSERVER_USER={DB_USER}\n"
        f"SQLSERVER_PASSWORD={DB_PASSWORD}\n"
        f"SQLSERVER_DRIVER={DB_DRIVER}\n"
        f"SQLSERVER_TRUST_CERT={DB_TRUST_CERT}\n"
    )

    # ========= Escrever tudo =========
    for rel, content in files.items():
        write_text(root / rel, content, overwrite=False)

    write_text(root / ".env.example", env_example, overwrite=True)
    write_text(root / ".env", env_real, overwrite=False)

    print("✅ Bootstrap concluído.")
    print("Próximos passos:")
    print("  1) python -m venv .venv")
    print("  2) source .venv/bin/activate")
    print("  3) pip install -r requirements.txt")
    print("  4) python bootstrap.py  (se precisar recriar)")
    print("  5) python run.py")


if __name__ == "__main__":
    main()