from app.config import config

# NB: do not add imports here!

from pathlib import Path
import os

# ...and here!!

if Path(__file__).parent == Path(os.getcwd()):
    config.root_dir = "."

# You can add imports from here...

from fastapi import FastAPI
from app.routers import frontend

from app.routers import events  # importiamo il router degli eventi
from app.routers import users   # importiamo il router degli utenti
from app.routers import registrations  # importiamo il router delle registrazioni



from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from app.data.db import init_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    # on start
    init_database()
    yield
    # on close



app = FastAPI(lifespan=lifespan)
app.mount(
    "/static",
    StaticFiles(directory=config.root_dir / "static"),
    name="static"
)
app.include_router(frontend.router)

app.include_router(events.router)  # colleghiamo le API degli eventi
app.include_router(users.router)  # colleghiamo le API degli utenti
app.include_router(registrations.router)  # colleghiamo le API delle registrazioni
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)
