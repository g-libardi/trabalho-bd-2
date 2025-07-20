import couchdb
from fastapi import APIRouter, Depends, Request
from deps import get_db
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import pandas as pd
import plotly.express as px
import os

# Configurar templates e arquivos estáticos
templates = Jinja2Templates(directory="templates")

router = APIRouter(prefix="/maps")

@router.get("/desastres-por-pais", response_class=HTMLResponse)
def mapa_desastres_por_pais(request: Request, db: couchdb.Database = Depends(get_db)):
    """Retorna um mapa choropleth interativo mostrando o número de desastres por país."""
    # Buscar dados de desastres por país
    result = db.view('desastres/por_pais', group=True)
    
    # Transformar os dados em DataFrame
    data = [{"Country": row.key, "Disaster_Count": row.value} for row in result]
    df = pd.DataFrame(data)
    
    # Criar o mapa choropleth
    fig = px.choropleth(
        df,
        locations="Country",
        locationmode="country names",
        color="Disaster_Count",
        color_continuous_scale="Reds",
        title="Número de Desastres Naturais por País",
        labels={"Disaster_Count": "Número de Desastres", "Country": "País"}
    )
    
    # Configurar o layout do mapa
    fig.update_layout(
        title_x=0.5,
        title_font_size=20,
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='equirectangular'
        )
    )
    
    # Gerar HTML do Plotly
    plotly_html = fig.to_html(include_plotlyjs=True, full_html=False, div_id="plotly-div")
    
    # Renderizar template com os dados
    return templates.TemplateResponse("map.html", {
        "request": request,
        "plotly_html": plotly_html
    }) 