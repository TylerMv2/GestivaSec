from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import json
from backend.database.connection import get_db
from backend.models.host import Host
from backend.schemas.host import HostResponse, HostCreate, HostUpdate

router = APIRouter(prefix="/hosts", tags=["Hosts"])

@router.get("", response_model=list[HostResponse])
def get_hosts(db: Session = Depends(get_db)):
    return db.query(Host).all()

@router.get("/{host_id}", response_model=HostResponse)
def get_host(host_id: int, db: Session = Depends(get_db)):
    host = db.query(Host).filter(Host.id == host_id).first()
    if not host:
        raise HTTPException(status_code=404, detail="Host not found")
    return host

@router.post("", response_model=HostResponse, status_code=status.HTTP_201_CREATED)
def create_host(host_data: HostCreate, db: Session = Depends(get_db)):
    # Validate ports JSON
    try:
        json.loads(host_data.ports_authorized)
    except ValueError:
        raise HTTPException(status_code=400, detail="ports_authorized must be a valid JSON array of integers")

    # Validate tags JSON
    try:
        json.loads(host_data.tags)
    except ValueError:
        raise HTTPException(status_code=400, detail="tags must be a valid JSON array of strings")

    new_host = Host(
        hostname=host_data.hostname,
        ip=host_data.ip,
        os=host_data.os,
        classification=host_data.classification,
        ports_authorized=host_data.ports_authorized,
        notes=host_data.notes,
        tags=host_data.tags,
        status="UNKNOWN"
    )
    db.add(new_host)
    db.commit()
    db.refresh(new_host)
    return new_host

@router.put("/{host_id}", response_model=HostResponse)
def update_host(host_id: int, host_data: HostUpdate, db: Session = Depends(get_db)):
    host = db.query(Host).filter(Host.id == host_id).first()
    if not host:
        raise HTTPException(status_code=404, detail="Host not found")
        
    for key, value in host_data.model_dump(exclude_unset=True).items():
        if key in ["ports_authorized", "tags"]:
            # Validate JSON if provided
            try:
                json.loads(value)
            except ValueError:
                raise HTTPException(status_code=400, detail=f"{key} must be a valid JSON string")
        setattr(host, key, value)
        
    db.commit()
    db.refresh(host)
    return host

@router.delete("/{host_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_host(host_id: int, db: Session = Depends(get_db)):
    host = db.query(Host).filter(Host.id == host_id).first()
    if not host:
        raise HTTPException(status_code=404, detail="Host not found")
    db.delete(host)
    db.commit()
    return None
