import pytest
from fastapi.testclient import TestClient

from shortlink import models  # noqa: F401  (registers tables on Base.metadata)
from shortlink.db import Base
from shortlink.main import create_app


@pytest.fixture
def client() -> TestClient:
    app = create_app("sqlite://")
    Base.metadata.create_all(app.state.engine)
    with TestClient(app, follow_redirects=False) as c:
        yield c
