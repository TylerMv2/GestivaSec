from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database.connection import get_db
from backend.models.certificate import Certificate

router = APIRouter(prefix="/certificates", tags=["Certificates"])

@router.get("")
def get_certificates(db: Session = Depends(get_db)):
    certs = db.query(Certificate).all()
    results = []
    
    for c in certs:
        # Load associated host and service
        host = c.host
        service = c.service
        
        results.append({
            "id": c.id,
            "host_id": c.host_id,
            "hostname": host.hostname if host else "Unknown",
            "service_id": c.service_id,
            "service_name": service.name if service else "Unknown",
            "domain": c.domain,
            "issuer": c.issuer,
            "signature_algorithm": c.signature_algorithm,
            "valid_from": c.valid_from.isoformat() if c.valid_from else None,
            "valid_to": c.valid_to.isoformat() if c.valid_to else None,
            "days_remaining": c.days_remaining,
            "status": c.status,
            "cipher_suite": c.cipher_suite,
            "tls_version": c.tls_version,
            "updated_at": c.updated_at.isoformat()
        })
        
    return results
