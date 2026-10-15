from fastapi import FastAPI
from sqlalchemy.orm import sessionmaker

from . import __version__
from .api import health_router, links_router, redirect_router
from .config import get_settings
from .db import make_engine
from .metrics import install_metrics


def create_app(database_url: str | None = None) -> FastAPI:
    """App factory. Run with: uvicorn --factory shortlink.main:create_app"""
    settings = get_settings()
    engine = make_engine(database_url or settings.database_url)

    app = FastAPI(title="Shortlink", version=__version__)
    app.state.settings = settings
    app.state.engine = engine
    app.state.session_factory = sessionmaker(bind=engine, expire_on_commit=False)

    app.include_router(health_router)
    app.include_router(links_router)
    install_metrics(app)
    # Must be registered last: "/{code}" would otherwise shadow the fixed routes above.
    app.include_router(redirect_router)
    return app
