import pytest


def _create(client, url="https://example.com/some/page"):
    resp = client.post("/links", json={"target_url": url})
    assert resp.status_code == 201, resp.text
    return resp.json()


def test_health_and_readiness(client):
    assert client.get("/healthz").json() == {"status": "ok"}
    assert client.get("/readyz").json() == {"status": "ready"}


def test_create_link_returns_code_and_short_url(client):
    body = _create(client)
    assert len(body["code"]) == 7
    assert body["short_url"].endswith("/" + body["code"])
    assert body["target_url"] == "https://example.com/some/page"


def test_redirect_follows_target(client):
    code = _create(client)["code"]
    resp = client.get(f"/{code}")
    assert resp.status_code == 302
    assert resp.headers["location"] == "https://example.com/some/page"


def test_unknown_code_is_404(client):
    assert client.get("/doesnotexist").status_code == 404
    assert client.get("/links/doesnotexist/stats").status_code == 404


def test_stats_count_clicks(client):
    code = _create(client)["code"]
    for _ in range(3):
        client.get(f"/{code}")
    stats = client.get(f"/links/{code}/stats").json()
    assert stats["total_clicks"] == 3
    assert len(stats["daily"]) == 1
    assert stats["daily"][0]["clicks"] == 3


def test_stats_for_unclicked_link_is_zero(client):
    code = _create(client)["code"]
    stats = client.get(f"/links/{code}/stats").json()
    assert stats == {
        "code": code,
        "target_url": "https://example.com/some/page",
        "total_clicks": 0,
        "daily": [],
    }


@pytest.mark.parametrize(
    "bad", ["not a url", "ftp://example.com/file", "javascript:alert(1)", "", "https://"]
)
def test_rejects_invalid_urls(client, bad):
    assert client.post("/links", json={"target_url": bad}).status_code == 422


def test_rejects_overlong_urls(client):
    long_url = "https://example.com/" + "a" * 2100
    assert client.post("/links", json={"target_url": long_url}).status_code == 422


def test_metrics_endpoint_exposed(client):
    _create(client)
    resp = client.get("/metrics")
    assert resp.status_code == 200
    assert "http_requests_total" in resp.text
