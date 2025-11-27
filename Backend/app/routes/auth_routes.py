from flask import Blueprint, request, jsonify, make_response, g
from functools import wraps

from app.dependencies.auth_deps import get_current_user
from app.services.auth_service import AuthService
from app.utils.jwt_tools import (
    make_access,
    make_refresh,
    decode_token,
    ACCESS_TTL,
    REFRESH_TTL,
)
from app.utils.cookie_tools import set_cookie, clear_cookie
from app.schemas.auth_schemas import CreateUserRequest


auth_bp = Blueprint("auth", __name__)
auth_service = AuthService()


# -------- ROLE DECORATOR --------
def role_required(role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            user = get_current_user()
            if not user or user.get("app_role") != role:
                return jsonify({"detail": "Not authorized"}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator


# -------- HEALTH --------
@auth_bp.route("/health", methods=["GET"])
def auth_health():
    return jsonify({"status": "OK", "scope": "auth"})


# -------- CREATE USER (Admin Only) --------
@auth_bp.route("/create-user", methods=["POST"])
@role_required("admin")
def create_user():
    db = g.service

    payload = request.get_json()
    if not payload:
        return jsonify({"detail": "Missing JSON"}), 400

    try:
        data = CreateUserRequest(**payload)
    except Exception:
        return jsonify({"detail": "Invalid payload"}), 400

    if data.pas != data.vps:
        return jsonify({"detail": "Passwords do not match"}), 400

    if len(data.pas) < 4:
        return jsonify({"detail": "Password must be at least 4 characters"}), 400

    ok, msg = auth_service.create_employ(db, data.username, data.pas, data.role)
    if not ok:
        return jsonify({"detail": msg}), 400

    user = auth_service.get_user(db, data.username)
    if not user:
        return jsonify({"detail": "User created but cannot fetch ID"}), 500

    return jsonify({
        "success": True,
        "message": f"User created: {data.username}",
        "user_id": user["id"],
    })


# -------- LOGIN --------
@auth_bp.route("/login", methods=["POST"])
def login():
    db = g.service

    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        return jsonify({"detail": "Missing credentials"}), 400

    if not auth_service.password_check(db, username, password):
        auth_service.log_event(db, username, "login_failed", "Wrong password", request)
        return jsonify({"detail": "Invalid credentials"}), 401

    user = auth_service.get_user(db, username)
    if not user:
        return jsonify({"detail": "User not found"}), 404

    user_id = str(user["id"])
    app_role = user["role"]

    access_token = make_access(user_id, app_role)
    refresh_token = make_refresh(user_id, app_role)

    response = make_response(
        jsonify({"success": True, "role": app_role, "user_name": username})
    )

    set_cookie(response, "atm_token", access_token, max_age=int(ACCESS_TTL.total_seconds()))
    set_cookie(response, "refresh_token", refresh_token, max_age=int(REFRESH_TTL.total_seconds()))

    auth_service.log_event(db, username, "login_success", "User authenticated", request)
    return response


# -------- LOGOUT --------
@auth_bp.route("/logout", methods=["POST"])
def logout():
    response = make_response(jsonify({"success": True, "message": "Logged out"}))
    clear_cookie(response, "atm_token")
    clear_cookie(response, "refresh_token")
    return response


# -------- REFRESH TOKENS --------
@auth_bp.route("/refresh", methods=["POST"])
def refresh_tokens():
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        return jsonify({"detail": "Missing refresh token"}), 401

    claims = decode_token(refresh_token)
    if claims.get("type") != "refresh":
        return jsonify({"detail": "Invalid refresh token"}), 401

    sub = claims.get("sub")
    app_role = claims.get("app_role")
    if not sub or not app_role:
        return jsonify({"detail": "Invalid refresh payload"}), 401

    db = g.service

    res = (
        db.table("users")
        .select("role")
        .eq("uid", sub)
        .single()
        .execute()
    )

    if not res.data:
        return jsonify({"detail": "User not found"}), 401

    app_role = res.data["role"]

    new_access = make_access(str(sub), app_role)
    new_refresh = make_refresh(str(sub), app_role)

    response = make_response(jsonify({"success": True}))

    set_cookie(response, "atm_token", new_access, max_age=int(ACCESS_TTL.total_seconds()))
    set_cookie(response, "refresh_token", new_refresh, max_age=int(REFRESH_TTL.total_seconds()))

    return response


# -------- AUTH CHECK --------
@auth_bp.route("/check", methods=["GET"])
def auth_check():
    user = get_current_user()
    if not user:
        return jsonify({"authenticated": False}), 401

    return jsonify({
        "authenticated": True,
        "user_id": user["sub"],
        "role": user["app_role"],
    })
