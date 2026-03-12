import base64
import hashlib
import hmac
import json
import secrets
import time

from fastapi import HTTPException, status


def _b64encode(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).decode().rstrip("=")


def _b64decode(value: str) -> bytes:
    padding = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode(f"{value}{padding}".encode())


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 390000)
    return f"{_b64encode(salt)}:{_b64encode(digest)}"


def verify_password(password: str, password_hash: str) -> bool:
    try:
        salt_b64, digest_b64 = password_hash.split(":", maxsplit=1)
    except ValueError:
        return False

    salt = _b64decode(salt_b64)
    expected_digest = _b64decode(digest_b64)
    actual_digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 390000)
    return hmac.compare_digest(actual_digest, expected_digest)


def create_access_token(username: str, role: str, secret: str, ttl_seconds: int = 28800) -> str:
    payload = {
        "sub": username,
        "role": role,
        "exp": int(time.time()) + ttl_seconds,
    }
    encoded_payload = _b64encode(
        json.dumps(payload, separators=(",", ":"), sort_keys=True).encode()
    )
    signature = _b64encode(
        hmac.new(secret.encode(), encoded_payload.encode(), hashlib.sha256).digest()
    )
    return f"{encoded_payload}.{signature}"


def decode_access_token(token: str, secret: str) -> dict:
    try:
        encoded_payload, signature = token.split(".", maxsplit=1)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token",
        ) from exc

    expected_signature = _b64encode(
        hmac.new(secret.encode(), encoded_payload.encode(), hashlib.sha256).digest()
    )
    if not hmac.compare_digest(signature, expected_signature):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token",
        )

    try:
        payload = json.loads(_b64decode(encoded_payload).decode())
    except (ValueError, json.JSONDecodeError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token",
        ) from exc

    if payload.get("exp", 0) < int(time.time()):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token expired",
        )
    return payload
