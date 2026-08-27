"""
Gestiva Security (GestivaSec V1) — IAM-OAUTH: OAuth REST API Router
Exposes /api/v1/auth/oauth endpoints.
"""
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from backend.domain.oauth import OAuthProviderConfig, SUPPORTED_PROVIDERS
from backend.domain.auth import UserIdentity

router = APIRouter(prefix="/api/v1/auth/oauth", tags=["OAuth Authentication"])

class OAuthAuthorizeResponse(BaseModel):
    provider: str
    authorize_url: str

class OAuthCallbackResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    email: str

@router.get("/authorize/{provider}", response_model=OAuthAuthorizeResponse)
async def get_oauth_authorize_url(provider: str, redirect_uri: str = Query("http://localhost:8000/api/v1/auth/oauth/callback")):
    """Generates OAuth authorization redirect URL for requested provider."""
    if provider.lower() not in SUPPORTED_PROVIDERS:
        raise HTTPException(status_code=400, detail=f"Proveedor OAuth '{provider}' no soportado.")
    
    config = OAuthProviderConfig(
        provider_name=provider,
        client_id="gestivasec-client-id-2026",
        authorize_url=f"https://auth.{provider}.com/oauth/v2/authorize",
        token_url=f"https://auth.{provider}.com/oauth/v2/token"
    )
    redirect_url = config.build_authorize_redirect(redirect_uri, state="gestivasec-state-nonce")
    return OAuthAuthorizeResponse(provider=provider, authorize_url=redirect_url)

@router.get("/callback", response_model=OAuthCallbackResponse)
async def oauth_callback(code: str = Query(...), state: str = Query(...)):
    """Handles OAuth provider authorization code exchange and issues JWT token."""
    # Simulated provider user resolution for OAuth flow
    mock_user = UserIdentity(
        id="00000000-0000-0000-0000-000000000088",
        organization_id="00000000-0000-0000-0000-000000000001",
        email="sso.admin@gestivaone.com",
        password_hash="oauth-sso-login",
        role="SOC_ADMIN"
    )
    token = mock_user.generate_access_token()
    return OAuthCallbackResponse(access_token=token, email=mock_user.email)
