from flask import Blueprint, g, jsonify
from functools import wraps

from app.dependencies.auth_deps import get_current_user, roles_required
from app.services.account_service import AccountService
from app.schemas.account_schemas import CreateAccountRequest


account_bp = Blueprint("account", __name__)
account_service = AccountService()


# -------- ROLE DECORATOR (same as used in auth routes) --------
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


# -------- CREATE ACCOUNT (Admin Only) --------
@account_bp.route("/create", methods=["POST"])
@role_required("admin")
def create_account():
    db = g.service  # obtained from middleware

    # Flask doesn't auto-validate JSON → must load manually
    payload = g.get("json")
    if not payload:
        return jsonify({"detail": "Missing JSON"}), 400

    # Pydantic-like validation using your schema
    try:
        data = CreateAccountRequest(**payload)
    except Exception:
        return jsonify({"detail": "Invalid payload"}), 400

    ok, result = account_service.create_account(
        db=db,
        holder_name=data.holder_name,
        pin=data.pin,
        vpin=data.vpin,
        mobileno=data.mobileno,
        gmail=data.gmail,
        request=g.request,
    )

    if not ok:
        return jsonify({"detail": result}), 400

    return jsonify({
        "success": True,
        "account_no": result["account_no"],
        "message": result["message"],
    })
