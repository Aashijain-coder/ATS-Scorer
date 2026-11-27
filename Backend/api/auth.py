from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from Backend.core.config import SUPABASE_ANON_KEY, SUPABASE_URL

bearer = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
) -> str:
    if credentials is None:
        raise HTTPException(401, "Supabase access token required", headers={"WWW-Authenticate": "Bearer"})
    if not SUPABASE_URL or not SUPABASE_ANON_KEY:
        raise HTTPException(503, "Supabase authentication is not configured")

    import httpx

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                f"{SUPABASE_URL.rstrip('/')}/auth/v1/user",
                headers={
                    "apikey": SUPABASE_ANON_KEY,
                    "Authorization": f"Bearer {credentials.credentials}",
                },
            )
        if response.status_code in (401, 403):
            raise HTTPException(401, "Invalid Supabase access token", headers={"WWW-Authenticate": "Bearer"})
        response.raise_for_status()
        user = response.json()
    except (httpx.HTTPError, ValueError) as exc:
        raise HTTPException(503, "Supabase authentication is unavailable") from exc

    user_id = user.get("id") if isinstance(user, dict) else None
    if not isinstance(user_id, str) or not user_id:
        raise HTTPException(503, "Supabase returned an invalid user")
    return user_id
