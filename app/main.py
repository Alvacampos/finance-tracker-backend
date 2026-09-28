from fastapi import FastAPI

from app.schemas.health import HealthCheckResponse

app = FastAPI(title="Finance Tracker Backend")


@app.get("/api/health")
def health_check() -> HealthCheckResponse:
    return HealthCheckResponse()
