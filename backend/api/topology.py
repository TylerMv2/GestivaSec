from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database.connection import get_db
from backend.models.host import Host
from backend.models.service import Service

router = APIRouter(prefix="/topology", tags=["Topology"])

@router.get("")
def get_topology(db: Session = Depends(get_db)):
    hosts = db.query(Host).all()
    
    # Static base nodes for logical path representation
    nodes = [
        {"id": "internet", "label": "Internet Gateway", "type": "External", "status": "UP"},
        {"id": "firewall", "label": "Edge Firewall", "type": "Firewall", "status": "UP"},
        {"id": "switch", "label": "Core Switch", "type": "Switch", "status": "UP"}
    ]
    
    edges = [
        {"source": "internet", "target": "firewall"},
        {"source": "firewall", "target": "switch"}
    ]
    
    # Process hosts and services dynamically
    for host in hosts:
        # Avoid duplicate logical nodes if Localhost maps to Core Switch
        host_node_id = f"host_{host.id}"
        
        # Determine logical status
        nodes.append({
            "id": host_node_id,
            "label": f"{host.hostname}\n({host.ip})",
            "type": host.classification,
            "status": host.status,
            "latency": host.latency_ms
        })
        
        # Connect host to core switch or firewall based on classification
        if host.classification in ["Firewall", "Switch"]:
            edges.append({"source": "firewall", "target": host_node_id})
        else:
            edges.append({"source": "switch", "target": host_node_id})
            
        # Draw edges to host services
        services = db.query(Service).filter(Service.host_id == host.id).all()
        for svc in services:
            svc_node_id = f"svc_{svc.id}"
            nodes.append({
                "id": svc_node_id,
                "label": f"{svc.name}\n(Port {svc.port})",
                "type": "Service",
                "status": svc.status
            })
            edges.append({"source": host_node_id, "target": svc_node_id})
            
    return {
        "nodes": nodes,
        "links": edges
    }
