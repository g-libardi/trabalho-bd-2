from fastapi import Depends, FastAPI, HTTPException
from contextlib import asynccontextmanager
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import plotly.graph_objs as go
import plotly.io as pio
import couchdb
from startup.db_initialization import start_db, stop_db
from startup.data_initialization import load_data
from queries_router import router
from map_router import router as map_router


# lifespan hook for app
@asynccontextmanager
async def lifespan(app: FastAPI):
    config = start_db()
    load_data(config)
    db = couchdb.Server(str(config.url))
    db.resource.credentials = (config.admin_user, config.admin_password)
    if config.db_name not in db:
        db = db.create(config.db_name)
    else:
        db = db[config.db_name]
    # add db to app state
    app.state.db = db
    yield
    stop_db()


app = FastAPI(lifespan=lifespan)

# Configurar arquivos estáticos
app.mount("/static", StaticFiles(directory="templates/static"), name="static")

app.include_router(router)
app.include_router(map_router)

# @app.get("/plot", response_class=HTMLResponse)
# def plot_example(db: couchdb.Database = Depends(get_db)):
#     # Exemplo de dados
#     x = [1, 2, 3, 4, 5]
#     y = [10, 14, 18, 24, 30]
#     fig = go.Figure(data=go.Scatter(x=x, y=y, mode='lines+markers'))
#     fig.update_layout(title="Exemplo de Gráfico Plotly")
#     html = pio.to_html(fig, full_html=False)
#     return html