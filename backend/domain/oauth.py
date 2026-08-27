"""
Gestiva Security (GestivaSec V1) — IAM-OAUTH: OAuth Provider Integration (CAP-01)
Encapsulates OAuth2 Social Login and Provider Authorization Token Exchange.
"""
from dataclasses import dataclass
from typing import Optional

SUPPORTED_PROVIDERS = {"google", "github", "gestivaone"}

@dataclass
class OAuthProviderConfig:
    provider_name: str
    client_id: str
    authorize_url: str
    token_url: str

    def __post_init__(self):
        if self.provider_name.lower() not in SUPPORTED_PROVIDERS:
            raise ValueError(f"Proveedor OAuth '{self.provider_name}' no soportado. Soportados: {SUPPORTED_PROVIDERS}")

    def build_authorize_redirect(self, redirect_uri: str, state: str) -> str:
        return f"{self.authorize_url}?client_id={self.client_id}&redirect_uri={redirect_uri}&response_type=code&state={state}"
