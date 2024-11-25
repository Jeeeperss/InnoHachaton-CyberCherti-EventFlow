from fastapi_users.authentication import BearerTransport
from core.authentication.settings import settings

bearer_transport = BearerTransport(tokenUrl = settings.api.bearer_token_url)