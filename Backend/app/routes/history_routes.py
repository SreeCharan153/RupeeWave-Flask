from flask import Blueprint, request, jsonify, g
from app.dependencies.auth_deps import roles_required, get_current_user
from app.services.history_service import HistoryService
from app.services.auth_service import AuthService


history_bp = Blueprint("history", __name__)

history_service = HistoryService()
auth_service = AuthService()


# -------- GET HISTORY --------
@history_bp.route("/<string:ac_no>", methods=["GET"])
@roles_required("admin", "teller")
def get_history(ac_no):
    db = g.service

    # Query parameter
    pin = request.args.get("pin")
    if not pin:
        return jsonify({"detail": "PIN is required"}), 400

    # Check PIN correctness
    ok, msg = auth_service.check(db, ac_no=ac_no, pin=pin, request=request)
    if not ok:
        return jsonify({"detail": msg}), 400

    # Fetch history
    ok, history = history_service.get_history(db, ac_no)
    if not ok:
        return jsonify({"detail": history}), 404

    return jsonify({"history": history})
