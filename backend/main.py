"""
Gestiva Security (GestivaSec V1) — Main FastAPI Backend Application Entrypoint
Integrates IAM, Passive Discovery, SOC Scheduler, Threat Intelligence, Alert Engine & Incident Console.
"""
import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse

from backend.config.settings import settings
from backend.config.logging import setup_logging, logger
from backend.api.auth_router import router as auth_router
from backend.api.oauth_router import router as oauth_router
from backend.api.organizations_router import router as organizations_router
from backend.api.users_router import router as users_router
from backend.api.roles_router import router as roles_router
from backend.api.permissions_router import router as permissions_router
from backend.api.assets_router import router as assets_router
from backend.api.synthetic_router import router as synthetic_router, synthetic_alias_router as synthetic_alias_router
from backend.api.passive_discovery_router import router as passive_discovery_router
from backend.api.soc_scheduler_router import router as soc_scheduler_router
from backend.api.threat_intel_router import router as threat_intel_router
from backend.api.alert_router import router as alert_router
from backend.api.audit_router import router as audit_router
from backend.api.dashboard_telemetry_router import router as dashboard_telemetry_router
from backend.api.discovery_router import router as discovery_router
from backend.api.collectors_router import router as collectors_router
from backend.api.normalization_router import router as normalization_router
from backend.api.detection_router import router as detection_router
from backend.api.correlation_router import router as correlation_router
from backend.api.incident_case_router import router as incident_case_router
from backend.api.threat_intel_engine_router import router as threat_intel_engine_router
from backend.api.soar_router import router as soar_router
from backend.api.reporting_router import router as reporting_router
from backend.api.diagnostics import router as diagnostics_router

setup_logging()

app = FastAPI(
    title="Gestiva Security API",
    description="Enterprise SOC & Continuous Passive Security Observability Platform for GestivaOne",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# DYNAMIC CORS MIDDLEWARE FOR SELF-HOSTED DEPLOYMENT
origins = [o.strip() for o in settings.CORS_ORIGINS.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if origins else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# REGISTER REST ROUTERS
app.include_router(auth_router)
app.include_router(oauth_router)
app.include_router(organizations_router)
app.include_router(users_router)
app.include_router(roles_router)
app.include_router(permissions_router)
app.include_router(assets_router)
app.include_router(synthetic_router)
app.include_router(synthetic_alias_router)
app.include_router(passive_discovery_router)
app.include_router(soc_scheduler_router)
app.include_router(threat_intel_router)
app.include_router(incident_case_router)
app.include_router(alert_router)
app.include_router(audit_router)
app.include_router(dashboard_telemetry_router)
app.include_router(discovery_router)
app.include_router(collectors_router)
app.include_router(normalization_router)
app.include_router(detection_router)
app.include_router(correlation_router)
app.include_router(threat_intel_engine_router)
app.include_router(soar_router)
app.include_router(reporting_router)
app.include_router(diagnostics_router)

# MOUNT FRONTEND STATIC ASSETS IF PRESENT
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
static_dir = os.path.join(frontend_dir, "static")

if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/", include_in_schema=False)
async def serve_index():
    index_path = os.path.join(frontend_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return JSONResponse(content={"message": "GestivaSec API Operating Baseline"})

@app.on_event("startup")
async def startup_event():
    logger.info("GestivaSec Backend Engine Initialized with Alert Engine & SOC Incident Console", environment=settings.ENVIRONMENT, port=settings.PORT)

@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "service": "GestivaSec Backend Engine",
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT
    }

@app.get("/metrics", tags=["Telemetry"])
async def prometheus_metrics():
    return JSONResponse(
        content={
            "gestivasec_uptime_seconds": 100,
            "gestivasec_active_tenants": 2,
            "gestivasec_monitored_assets": 3
        }
    )

if __name__ == "__main__":
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=settings.PORT,
        reload=(settings.ENVIRONMENT == "development")
    )
