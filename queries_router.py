import couchdb
from fastapi import APIRouter, Depends, Query
from deps import get_db
from queries import (
    lista_de_nomes_de_paises,
    total_desastres_por_pais,
    total_desastres_por_pais_ano,
    top_5_desastres_mais_mortais,
    total_pessoas_afetadas,
    total_danos_economicos,
    desastres_por_tipo,
    desastres_por_grupo,
    tendencia_historica,
    lista_desastres_filtrada,
    exportar_dados_json
)

router = APIRouter(prefix="/queries")

@router.get("/")
def lista_de_nomes_de_paises_route(db: couchdb.Database = Depends(get_db)):
    return lista_de_nomes_de_paises(db)

@router.get("/total-desastres-por-pais")
def total_desastres_por_pais_route(pais: str = Query(...), db: couchdb.Database = Depends(get_db)):
    """Consulta 1: Conta quantos desastres existem para o país."""
    return total_desastres_por_pais(pais, db)

@router.get("/total-desastres-por-pais-ano")
def total_desastres_por_pais_ano_route(pais: str = Query(...), ano: int = Query(...), db: couchdb.Database = Depends(get_db)):
    """Consulta 2: Conta desastres no país em determinado ano."""
    return total_desastres_por_pais_ano(pais, ano, db)

@router.get("/top-5-desastres-mais-mortais")
def top_5_desastres_mais_mortais_route(pais: str = Query(...), db: couchdb.Database = Depends(get_db)):
    """Consulta 3: Retorna os 5 desastres com mais mortes no país."""
    return top_5_desastres_mais_mortais(pais, db)

@router.get("/total-pessoas-afetadas")
def total_pessoas_afetadas_route(pais: str = Query(...), db: couchdb.Database = Depends(get_db)):
    """Consulta 4: Soma o total de pessoas afetadas no país."""
    return total_pessoas_afetadas(pais, db)

@router.get("/total-danos-economicos")
def total_danos_economicos_route(pais: str = Query(...), db: couchdb.Database = Depends(get_db)):
    """Consulta 5: Soma o total de danos econômicos no país."""
    return total_danos_economicos(pais, db)

@router.get("/desastres-por-tipo")
def desastres_por_tipo_route(pais: str = Query(...), db: couchdb.Database = Depends(get_db)):
    """Consulta 6: Retorna dicionário {tipo: quantidade} de desastres no país."""
    return desastres_por_tipo(pais, db)

@router.get("/desastres-por-grupo")
def desastres_por_grupo_route(pais: str = Query(...), db: couchdb.Database = Depends(get_db)):
    """Consulta 7: Retorna dicionário {grupo: quantidade} de desastres no país."""
    return desastres_por_grupo(pais, db)

@router.get("/tendencia-historica")
def tendencia_historica_route(pais: str = Query(...), db: couchdb.Database = Depends(get_db)):
    """Consulta 8: Retorna dict {ano: total de desastres} para o país (ordem crescente ano)."""
    return tendencia_historica(pais, db)

@router.get("/lista-desastres-filtrada")
def lista_desastres_filtrada_route(
    pais: str = Query(...),
    grupo: str | None = Query(None),
    tipo: str | None = Query(None),
    ano: int | None = Query(None),
    db: couchdb.Database = Depends(get_db)
):
    """Consulta 9: Retorna lista de documentos filtrados por país, grupo, tipo e ano (opcionais)."""
    return lista_desastres_filtrada(pais, grupo, tipo, ano, db)

@router.get("/exportar-dados-json")
def exportar_dados_json_route(pais: str = Query(...), db: couchdb.Database = Depends(get_db)):
    """Consulta 10: Retorna lista de docs para exportar em JSON (apenas do país)."""
    return exportar_dados_json(pais, db)