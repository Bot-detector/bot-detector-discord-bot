from fastapi import Header, HTTPException
from src.core.config import CONFIG


async def authenticate_user(authorization: str = Header(..., example="Bearer <key>")):
    # Replace this with your own authentication logic
    if not authorization or authorization != f"Bearer {CONFIG.BEARER}":
        raise HTTPException(status_code=401, detail="Unauthorized")
