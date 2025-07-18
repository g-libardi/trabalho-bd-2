from pydoc import cli
import docker
import time
import requests
from docker.models.containers import Container
from docker.client import DockerClient
from docker.errors import NotFound, APIError
from pydantic import BaseModel, computed_field
from yarl import URL

class CouchDBConfig(BaseModel):
    image: str = "couchdb:latest"
    container_name: str = "fastapi-couchdb"
    port: int = 5984
    admin_user: str = "admin"
    admin_password: str = "password"
    db_name: str = "desastres"
    host: str = "localhost"

    @computed_field
    @property
    def url(self) -> URL:
        return URL(f'http://{self.host}:{self.port}')

    class Config:
        arbitrary_types_allowed = True


# --- Configuration ---
_config = CouchDBConfig()

client = DockerClient.from_env()
container = None

def start_db() -> CouchDBConfig:
    global container, _config
    # 1. Check for and remove any existing container with the same name
    print(f"🔎 Checking for existing container named '{_config.container_name}'...")
    try:
        existing_container = client.containers.get(_config.container_name)
        print("❗️ Found existing container. Forcibly removing it...")
        existing_container.remove(force=True)
    except NotFound:
        print("✅ No existing container found.")
        pass

    # 2. Start the new CouchDB container
    print(f"🚀 Starting new CouchDB container '{_config.container_name}'...")
    container = client.containers.run(
        image=_config.image,
        name=_config.container_name,
        ports={f'5984/tcp': _config.port},
        environment=[f"COUCHDB_USER={_config.admin_user}", f"COUCHDB_PASSWORD={_config.admin_password}"],
        detach=True,
        auto_remove=True,
    )

    # 3. Wait for the container's health check to pass
    print("⏳ Waiting for CouchDB to be accessible...")
    start_time = time.time()
    while time.time() - start_time < 30:  # 30-second timeout
        try:
            response = requests.get(f"http://127.0.0.1:{_config.port}/")
            if response.status_code == 200:
                print("✅ CouchDB is up and running!")
                return _config
        except requests.exceptions.ConnectionError:
            time.sleep(1) # Wait a second before retrying
            
    # If the loop finishes without returning, it timed out
    raise RuntimeError("CouchDB container did not start in time.")


def stop_db():
    global container
    if not container:
        print("⚠️ No container object found to stop.")
        return
        
    print(f"🛑 Stopping container '{container.name}'...")
    try:
        container.stop()
        print("✅ Container stopped successfully.")
    except APIError as e:
        print(f"🚨 Error stopping container: {e}")