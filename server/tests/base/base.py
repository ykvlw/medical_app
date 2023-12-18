import pytest
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


@pytest.fixture
def api_client_with_credentials() -> APIClient:
    client = APIClient()
    user = User.objects.create_user(username="testuser", password="testpassword")
    token, _ = Token.objects.get_or_create(user=user)
    client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
    return client
