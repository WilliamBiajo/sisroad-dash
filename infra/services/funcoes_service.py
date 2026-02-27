from __future__ import annotations

from infra.loaders.excel_fields import get_excel_schema
from infra.repositories.funcoes_repo import list_funcoes, get_funcao, insert_funcao, update_funcao


def list_funcoes_cards():
    rows = list_funcoes()
    cards = []
    for r in rows:
        cards.append(
            {
                "id": r.get("id"),
                "descricao": r.get("descricao", "-"),
                "salario": r.get("salario", "-"),
                "inicio": r.get("inicio", "-"),
                "fim": r.get("fim", "-"),
            }
        )
    return cards


def get_funcao_detail(func_id: int | None):
    schema = get_excel_schema()
    data = get_funcao(func_id) if func_id else {}
    title = "Nova Função" if not func_id else f"Editar Função #{func_id}"
    return {"schema": schema, "data": data, "title": title}


def save_funcao(func_id: int | None, payload: dict):
    if func_id:
        update_funcao(func_id, payload)
        return func_id
    return insert_funcao(payload)