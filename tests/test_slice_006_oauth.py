import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.domain.oauth import OAuthProviderConfig

client = TestClient(app)

def test_domain_oauth_provider_validation():
    with pytest.raises(ValueError, match="no soportado"):
        OAuthProviderConfig(
            provider_name="unsupported_provider",
            client_id="id",
            authorize_url="url",
            token_url="url"
        )

def test_rest_api_get_oauth_url():
    response = client.get("/api/v1/auth/oauth/authorize/google")
    assert response.status_code == 200
    data = response.json()
    assert data["provider"] == "google"
    assert "client_id=" in data["authorize_url"]

def test_rest_api_oauth_callback():
    response = client.get("/api/v1/auth/oauth/callback?code=mock_code&state=mock_state")
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["email"] == "sso.admin@gestivaone.com"
