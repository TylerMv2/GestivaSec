from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import json
from backend.database.connection import get_db
from backend.models.settings import SettingsModel

router = APIRouter(prefix="/settings", tags=["Settings"])

@router.get("")
def get_all_settings(db: Session = Depends(get_db)):
    settings_records = db.query(SettingsModel).all()
    results = []
    
    for s in settings_records:
        try:
            config_dict = json.loads(s.configuration or "{}")
        except Exception:
            config_dict = {}

        results.append({
            "id": s.id,
            "module_name": s.module_name,
            "enabled": s.enabled,
            "interval_seconds": s.interval_seconds,
            "config": config_dict
        })
        
    return results

@router.put("/{module_name}")
def update_module_setting(
    module_name: str, 
    enabled: bool | None = None, 
    interval_seconds: int | None = None, 
    config_update: dict | None = None,
    db: Session = Depends(get_db)
):
    setting = db.query(SettingsModel).filter(SettingsModel.module_name == module_name).first()
    if not setting:
        raise HTTPException(status_code=404, detail=f"Module {module_name} settings not found")
        
    if enabled is not None:
        setting.enabled = enabled
        
    if interval_seconds is not None:
        if interval_seconds < 5:
            raise HTTPException(status_code=400, detail="Monitoring interval cannot be less than 5 seconds")
        setting.interval_seconds = interval_seconds
        
    if config_update is not None:
        try:
            current_config = json.loads(setting.configuration or "{}")
            current_config.update(config_update)
            setting.configuration = json.dumps(current_config)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid configuration format: {e}")
            
    db.commit()
    db.refresh(setting)
    
    # Return formatted setting
    return {
        "module_name": setting.module_name,
        "enabled": setting.enabled,
        "interval_seconds": setting.interval_seconds,
        "config": json.loads(setting.configuration)
    }
