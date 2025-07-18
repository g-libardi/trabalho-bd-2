import pandas as pd
import json
import numpy as np
import requests
from startup.db_initialization import CouchDBConfig
from pathlib import Path
import pickle as pkl

EXCEL_FILE = Path(__file__).parent.parent / "data" / "emdat.xlsx"
CACHE_FILE = Path(__file__).parent.parent / "data" / "emdat_docs.pkl"

def generate_docs():
    if CACHE_FILE.exists():
        print("Carregando documentos em cache...")
        with open(CACHE_FILE, "rb") as f:
            docs = pkl.load(f)
        return docs
    print("Cache não encontrado, gerando documentos...")
    df = pd.read_excel(EXCEL_FILE)
    df.columns = df.columns.str.strip()
    df = df.rename(columns={"DisNo.": "_id"})
    df["_id"] = df["_id"].astype(str).str.strip()
    df = df.replace({np.nan: None})
    docs = df.to_dict(orient="records")
    with open(CACHE_FILE, "wb") as f:
        print("Salvando documentos em cache...")
        pkl.dump(docs, f)
    print("Documentos gerados com sucesso!")
    return docs

def upload_design_doc(config: CouchDBConfig):
    design_doc = {
        "_id": "_design/desastres",
        "views": {
            "por_pais": {
                "map": "function(doc) { if (doc.Country) emit(doc.Country, 1); }",
                "reduce": "_count"
            },
            "por_pais_ano": {
                "map": "function(doc) { if (doc.Country && doc['Start Year']) emit([doc.Country, doc['Start Year']], 1); }",
                "reduce": "_count"
            },
            "top_mortais": {
                "map": "function(doc) { if (doc.Country && doc['Total Deaths']) emit([doc.Country, doc['Total Deaths']], doc['Event Name']); }"
            },
            "total_afetados": {
                "map": "function(doc) { if (doc.Country && doc['Total Affected']) emit(doc.Country, doc['Total Affected']); }",
                "reduce": "_sum"
            },
            "total_danos": {
                "map": "function(doc) { if (doc.Country && doc[\"Total Damage ('000 US$)\"]) emit(doc.Country, doc[\"Total Damage ('000 US$)\"]); }",
                "reduce": "_sum"
            },
            "por_tipo": {
                "map": "function(doc) { if (doc.Country && doc['Disaster Type']) emit([doc.Country, doc['Disaster Type']], 1); }",
                "reduce": "_count"
            },
            "por_grupo": {
                "map": "function(doc) { if (doc.Country && doc['Disaster Group']) emit([doc.Country, doc['Disaster Group']], 1); }",
                "reduce": "_count"
            },
            "por_ano": {
                "map": "function(doc) { if (doc.Country && doc['Start Year']) emit([doc.Country, doc['Start Year']], 1); }",
                "reduce": "_count"
            }
        }
    }
    url = config.url / config.db_name / design_doc["_id"]
    resp = requests.put(str(url), auth=(config.admin_user, config.admin_password), headers={"Content-Type": "application/json"}, data=json.dumps(design_doc))
    if resp.status_code not in (201, 202):
        print("Erro ao criar design doc:", resp.status_code, resp.text)
    else:
        print("Design document criado/atualizado com sucesso!")

def load_data(config: CouchDBConfig):
    print("Gerando documentos...")
    docs = generate_docs()

    print(f"Documentos gerados: {len(docs)}")
    print("Verificando se o banco de dados existe...")
    resp = requests.get(f"{config.url}/{config.db_name}", auth=(config.admin_user, config.admin_password), timeout=10)
    if resp.status_code == 404:
        print(f"Banco de dados não encontrado, criando banco de dados '{config.db_name}'...")
        resp_create = requests.put(f"{config.url}/{config.db_name}", auth=(config.admin_user, config.admin_password))
        if resp_create.status_code == 201:
            print("Banco criado com sucesso!")
        else:
            print("Erro ao criar banco:", resp_create.text)
            exit(1)
    else:
        print(f"Banco de dados '{config.db_name}' já existe, inserindo documentos...")

    # Upload design document (views)
    upload_design_doc(config)

    # Passo 7: Envia documentos em lote (_bulk_docs)
    payload = {"docs": docs}
    headers = {"Content-Type": "application/json"}

    print(f"Inserindo {len(docs)} documentos no banco de dados '{config.db_name}'...")

    docs_url = config.url / config.db_name / '_bulk_docs'

    response = requests.post(
        str(docs_url),
        auth=(config.admin_user, config.admin_password),
        headers=headers,
        data=json.dumps(payload)
    )

    if response.status_code == 201:
        print("Documentos inseridos com sucesso!")
    else:
        print("Erro ao inserir documentos:", response.status_code, response.text)
