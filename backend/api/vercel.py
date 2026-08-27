from fastapi import APIRouter
from backend.plugins.vercel_plugin import VercelPlugin

router = APIRouter(prefix="/vercel", tags=["Vercel Integration"])
vercel_plugin = VercelPlugin()

@router.get("/status")
def get_vercel_status():
    return vercel_plugin.get_status()

@router.get("/deployments")
def get_vercel_deployments(limit: int = 5):
    return vercel_plugin.get_deployments(limit=limit)

@router.get("/analytics")
def get_vercel_analytics():
    return vercel_plugin.get_web_analytics()

@router.get("/firewall")
def get_vercel_firewall(limit: int = 5):
    return vercel_plugin.get_firewall_logs(limit=limit)
