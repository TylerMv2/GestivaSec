import sys
import json
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from backend.database.connection import SessionLocal
from backend.models.settings import SettingsModel

def seed_api_settings():
    db = SessionLocal()
    try:
        # Check if API_Integrations already exists
        api_setting = db.query(SettingsModel).filter(SettingsModel.module_name == "API_Integrations").first()
        if api_setting:
            print("[*] API_Integrations settings row already present.")
            return

        print("[*] Seeding API_Integrations base configuration row...")
        default_config = {
            "vercel_auth_token": "",
            "vercel_project_id": "",
            "vercel_team_id": "",
            "notion_auth_token": "",
            "notion_database_id": "",
            "shodan_api_key": "",
            "virustotal_api_key": ""
        }
        
        set_model = SettingsModel(
            module_name="API_Integrations",
            enabled=True,
            interval_seconds=0, # Static configuration module, no background thread needed
            configuration=json.dumps(default_config)
        )
        db.add(set_model)
        db.commit()
        print("[+] API_Integrations base configuration successfully created!")
    except Exception as e:
        db.rollback()
        print(f"[-] Failed to seed API settings: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_api_settings()
