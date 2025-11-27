from flask import Blueprint, request, jsonify, g
from app.dependencies.auth_deps import roles_required
from app.schemas.update_schemas import (
    ChangePinRequest,
    UpdateMobileRequest,
    UpdateEmailRequest
)
from app.services.update_service import UpdateService


update_bp = Blueprint("update", __name__)
update_service = UpdateService()


# -------- CHANGE PIN --------
@update_bp.route("/change-pin", methods=["PUT"])
@roles_required("admin", "teller")
def change_pin():
    db = g.service   # middleware provided

    payload = request.get_json()
    if not payload:
        return jsonify({"detail": "Missing JSON"}), 400

    try:
        data = ChangePinRequest(**payload)
    except Exception:
        return jsonify({"detail": "Invalid payload"}), 400

    if data.newpin != data.vnewpin:
        return jsonify({"detail": "New PINs do not match."}), 400

    ok, msg = update_service.change_pin(
        db=db,
        ac_no=data.acc_no,
        old_pin=data.pin,
        new_pin=data.newpin,
        request=request,
    )

    if not ok:
        return jsonify({"detail": msg}), 400

    return jsonify({"success": True, "message": msg})


# -------- UPDATE MOBILE --------
@update_bp.route("/update-mobile", methods=["PUT"])
@roles_required("admin", "teller")
def update_mobile():
    db = g.service

    payload = request.get_json()
    if not payload:
        return jsonify({"detail": "Missing JSON"}), 400

    try:
        data = UpdateMobileRequest(**payload)
    except Exception:
        return jsonify({"detail": "Invalid payload"}), 400

    ok, msg = update_service.update_mobile(
        db=db,
        ac_no=data.acc_no,
        pin=data.pin,
        old_mobile=data.omobile,
        new_mobile=data.nmobile,
        request=request,
    )

    if not ok:
        return jsonify({"detail": msg}), 400

    return jsonify({"success": True, "message": msg})


# -------- UPDATE EMAIL --------
@update_bp.route("/update-email", methods=["PUT"])
@roles_required("admin", "teller")
def update_email():
    db = g.service

    payload = request.get_json()
    if not payload:
        return jsonify({"detail": "Missing JSON"}), 400

    try:
        data = UpdateEmailRequest(**payload)
    except Exception:
        return jsonify({"detail": "Invalid payload"}), 400

    ok, msg = update_service.update_email(
        db=db,
        ac_no=data.acc_no,
        pin=data.pin,
        old_email=data.oemail,
        new_email=data.nemail,
        request=request,
    )

    if not ok:
        return jsonify({"detail": msg}), 400

    return jsonify({"success": True, "message": msg})
