from __future__ import annotations

from sqlalchemy import text
from infra.db.engine import get_engine
from infra.loaders.excel_fields import get_excel_schema

TABLE = "dbo.funcoes"


def ensure_table_exists() -> None:
    schema = get_excel_schema()

    # separa id e restantes
    id_field = next((f for f in schema if f["name"].lower() == "id"), None)
    other_fields = [f for f in schema if f["name"].lower() != "id"]

    # id default caso não exista no excel
    id_sql = "INT IDENTITY(1,1) NOT NULL PRIMARY KEY"
    if id_field and id_field.get("sql"):
        # usa exatamente como está no Excel, mas garantindo NOT NULL
        id_sql = id_field["sql"]
        # se o usuário colocou "PRIMARY KEY" já está ok

    col_defs = ",\n".join([f"    [{f['name']}] {f['sql']}" for f in other_fields])

    ddl = f"""
IF OBJECT_ID(N'{TABLE}', N'U') IS NULL
BEGIN
    CREATE TABLE {TABLE} (
        [id] {id_sql}{"," if col_defs else ""}
{col_defs}
    );
END
"""
    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(text(ddl))


def list_funcoes():
    ensure_table_exists()
    engine = get_engine()
    q = f"SELECT TOP 200 * FROM {TABLE} ORDER BY id DESC"
    with engine.begin() as conn:
        rows = conn.execute(text(q)).mappings().all()
    return [dict(r) for r in rows]


def get_funcao(func_id: int):
    ensure_table_exists()
    engine = get_engine()
    q = f"SELECT * FROM {TABLE} WHERE id = :id"
    with engine.begin() as conn:
        row = conn.execute(text(q), {"id": func_id}).mappings().first()
    return dict(row) if row else None


def insert_funcao(payload: dict) -> int:
    ensure_table_exists()
    engine = get_engine()

    payload = {k: v for k, v in payload.items() if k.lower() != "id"}
    cols = list(payload.keys())
    if not cols:
        raise ValueError("Payload vazio para insert")

    col_sql = ", ".join([f"[{c}]" for c in cols])
    val_sql = ", ".join([f":{_p(c)}" for c in cols])
    params = {_p(k): payload[k] for k in cols}

    q = text(f"INSERT INTO {TABLE} ({col_sql}) VALUES ({val_sql}); SELECT SCOPE_IDENTITY() AS new_id;")
    with engine.begin() as conn:
        new_id = conn.execute(q, params).scalar()

    return int(new_id)


def update_funcao(func_id: int, payload: dict) -> None:
    ensure_table_exists()
    engine = get_engine()

    payload = {k: v for k, v in payload.items() if k.lower() != "id"}
    cols = list(payload.keys())
    if not cols:
        raise ValueError("Payload vazio para update")

    set_sql = ", ".join([f"[{c}] = :{_p(c)}" for c in cols])
    params = {_p(k): payload[k] for k in cols}
    params["id"] = func_id

    q = text(f"UPDATE {TABLE} SET {set_sql} WHERE id = :id;")
    with engine.begin() as conn:
        conn.execute(q, params)


def _p(col: str) -> str:
    return "p_" + "".join(ch if ch.isalnum() else "_" for ch in col)