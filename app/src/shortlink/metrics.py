import time

from fastapi import FastAPI, Request, Response
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    CollectorRegistry,
    Counter,
    Histogram,
    generate_latest,
)


def install_metrics(app: FastAPI) -> None:
    """Expose Prometheus metrics at /metrics.

    The handler label is the route *template* (e.g. "/{code}"), never the raw path,
    so label cardinality stays bounded.
    """
    registry = CollectorRegistry()
    requests_total = Counter(
        "http_requests_total",
        "Total HTTP requests",
        ["method", "handler", "status"],
        registry=registry,
    )
    request_seconds = Histogram(
        "http_request_duration_seconds",
        "HTTP request latency in seconds",
        ["method", "handler"],
        registry=registry,
    )

    @app.middleware("http")
    async def _record(request: Request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        route = request.scope.get("route")
        handler = getattr(route, "path", None) or "unmatched"
        if handler != "/metrics":
            requests_total.labels(request.method, handler, str(response.status_code)).inc()
            request_seconds.labels(request.method, handler).observe(time.perf_counter() - start)
        return response

    @app.get("/metrics", include_in_schema=False)
    def _metrics() -> Response:
        return Response(generate_latest(registry), media_type=CONTENT_TYPE_LATEST)
