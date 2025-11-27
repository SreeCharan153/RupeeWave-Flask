from flask import Blueprint, g, jsonify
from functools import wraps
from app.dependencies.auth_deps import get_current_user


debug_bp = Blueprint("debug", __name__)


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


# -------- DEBUG JWT --------
@debug_bp.route("/jwt", methods=["GET"])
@role_required("admin")     # locked to admin, same as FastAPI
def debug_jwt():
    db = g.service  # from middleware

    try:
        res = db.rpc("debug_claims").execute()
        return jsonify({"jwt": res.data})
    except Exception as e:
        return jsonify({"error": str(e)})
