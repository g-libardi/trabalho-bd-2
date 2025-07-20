import couchdb
from fastapi import Query
from fastapi.responses import JSONResponse

def lista_de_nomes_de_paises(db: couchdb.Database):
    """Retorna lista de nomes de países disponíveis."""
    result = db.view('desastres/por_pais', group=True)
    return {"paises": [row.key for row in result]}

def total_desastres_por_pais(pais: str, db: couchdb.Database):
    """Consulta 1: Conta quantos desastres existem para o país."""
    result = db.view('desastres/por_pais', key=pais, reduce=True)
    return {"total": list(result)[0].value if len(result) > 0 else 0}

def total_desastres_por_pais_ano(pais: str, ano: int, db: couchdb.Database):
    """Consulta 2: Conta desastres no país em determinado ano."""
    result = db.view('desastres/por_pais_ano', key=[pais, ano], reduce=True)
    return {"total": list(result)[0].value if len(result) > 0 else 0}

def top_5_desastres_mais_mortais(pais: str, db: couchdb.Database):
    """Consulta 3: Retorna os 5 desastres com mais mortes no país."""
    result = db.view('desastres/top_mortais', startkey=[pais, {}], endkey=[pais, 0], descending=True, limit=5)
    return {"top_5": [(row.value, row.key[1]) for row in result]}

def total_pessoas_afetadas(pais: str, db: couchdb.Database):
    """Consulta 4: Soma o total de pessoas afetadas no país."""
    result = db.view('desastres/total_afetados', key=pais, reduce=True)
    return {"total_afetados": list(result)[0].value if len(result) > 0 else 0}

def total_danos_economicos(pais: str, db: couchdb.Database):
    """Consulta 5: Soma o total de danos econômicos no país."""
    result = db.view('desastres/total_danos', key=pais, reduce=True)
    return {"total_danos": list(result)[0].value if len(result) > 0 else 0}

def desastres_por_tipo(pais: str, db: couchdb.Database):
    """Consulta 6: Retorna dicionário {tipo: quantidade} de desastres no país."""
    result = db.view('desastres/por_tipo', startkey=[pais, None], endkey=[pais, {}], group=True)
    return {row.key[1]: row.value for row in result}

def desastres_por_grupo(pais: str, db: couchdb.Database):
    """Consulta 7: Retorna dicionário {grupo: quantidade} de desastres no país."""
    result = db.view('desastres/por_grupo', startkey=[pais, None], endkey=[pais, {}], group=True)
    return {row.key[1]: row.value for row in result}

def tendencia_historica(pais: str, db: couchdb.Database):
    """Consulta 8: Retorna dict {ano: total de desastres} para o país (ordem crescente ano)."""
    result = db.view('desastres/por_ano', startkey=[pais, None], endkey=[pais, {}], group=True)
    return dict(sorted(((row.key[1], row.value) for row in result)))

def lista_desastres_filtrada(pais: str, grupo: str = None, tipo: str = None, ano: int = None, db: couchdb.Database = None):
    """Consulta 9: Retorna lista de documentos filtrados por país, grupo, tipo e ano (opcionais)."""
    resultados = []
    for row in db.view('_all_docs', include_docs=True):
        doc = row.doc
        if doc.get("Country") != pais:
            continue
        if grupo and doc.get("Disaster Group") != grupo:
            continue
        if tipo and doc.get("Disaster Type") != tipo:
            continue
        if ano and doc.get("Start Year") != ano:
            continue
        resultados.append(doc)
    return resultados

def exportar_dados_json(pais: str, db: couchdb.Database):
    """Consulta 10: Retorna lista de docs para exportar em JSON (apenas do país)."""
    resultados = []
    for row in db.view('_all_docs', include_docs=True):
        doc = row.doc
        if doc.get("Country") == pais:
            resultados.append(doc)
    return JSONResponse(content=resultados) 