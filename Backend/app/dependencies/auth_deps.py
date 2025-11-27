from flask import g, jsonify
from functools import wraps
from typing import Dict, Any

from app.utils.jwt_tools import decode_token, make_access, REFRESH_GRACE_SECONDS
from app.utils.time_tools import now_utc_ts
from app.core.supabase_client import get_public_client


def get_current_user() -> Dict[str, str] | None:
    """
    Extract and validate user from access token in Flask.
    Returns a dict OR None if unauthorized.
    """

    token = g.cookies.get("atm_token")
    if not token:
        return None

    # Decode token
    try:
        claims = decode_token(token)
    except Exception:
        return None

    if claims.get("type") != "access":
        return None

    user_id = claims.get("sub")
    app_role = claims.get("app_role")
    if not user_id or not app_role:
        return None

    # Fetch user from Supabase
    client = getattr(g, "supabase", None) or get_public_client()

    try:
        res = (
            client.table("users")
            .select("uid, role")
            .eq("uid", user_id)
            .single()
            .execute()
        )
    except Exception:
        return None

    if not res.data:
        return None

    # DB is source of truth
    db_role = res.data["role"]
    if db_role != app_role:
        app_role = db_role

    # Opportunistic refresh → Flask version
    exp = claims.get("exp")
    if exp and (exp - now_utc_ts()) < REFRESH_GRACE_SECONDS:
        # Our converted middleware looks for this
        g.new_access_token = make_access(str(user_id), app_role)

    return {"sub": str(user_id), "app_role": app_role}


def roles_required(*roles):
    """
    Decorator replacement for FastAPI's role enforcement.
    """

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            user = get_current_user()
            if not user:
                return jsonify({"detail": "Unauthorized"}), 401

            if user["app_role"] not in roles:
                return jsonify({"detail": "Forbidden: insufficient role"}), 403

            return fn(*args, **kwargs)
        return wrapper
    return decorator
