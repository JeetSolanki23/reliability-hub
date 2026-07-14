from fastapi import FastAPI, Request
from prometheus_client import make_asgi_app, Counter, Histogram
import time
from app.api import services, health, incidents, slo
from app.core.config import settings
from app.core.database import engine, Base

app = FastAPI(title=settings.PROJECT_NAME)

@app.on_event("startup")
def startup_event():
    # Create tables (for local dev without migrations initially)
    # In production, we would use Alembic
    if "sqlite" in str(engine.url):
        Base.metadata.create_all(bind=engine)

# Prometheus metrics
REQUEST_COUNT = Counter("reliability_hub_requests_total", "Total HTTP requests", ["method", "endpoint", "http_status"])
REQUEST_LATENCY = Histogram("reliability_hub_http_request_duration_seconds", "HTTP request latency", ["method", "endpoint"])

@app.middleware("http")
async def monitor_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    latency = time.time() - start_time

    # We use path_params or similar if we want cleaner endpoint names, but simple for now
    endpoint = request.url.path
    REQUEST_COUNT.labels(method=request.method, endpoint=endpoint, http_status=response.status_code).inc()
    REQUEST_LATENCY.labels(method=request.method, endpoint=endpoint).observe(latency)

    return response

# Include Routers
app.include_router(services.router)
app.include_router(health.router)
app.include_router(incidents.router)
app.include_router(slo.router)

# Metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.get("/readyz")
def readyz():
    return {"status": "ready"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.API_PORT)  # nosec B104
