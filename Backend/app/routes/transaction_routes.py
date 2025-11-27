from flask import Blueprint, request, jsonify, g

from app.dependencies.auth_deps import roles_required
from app.schemas.transaction_schemas import TransactionRequest, TransferRequest
from app.services.transaction_service import TransactionService


transaction_bp = Blueprint("transaction", __name__)
transaction_service = TransactionService()


# ---------------- DEPOSIT ----------------
@transaction_bp.route("/deposit", methods=["POST"])
@roles_required("admin", "teller", "customer")
def deposit():
    db = g.service  # from middleware

    payload = request.get_json()
    if not payload:
        return jsonify({"detail": "Missing JSON"}), 400

    try:
        data = TransactionRequest(**payload)
    except Exception:
        return jsonify({"detail": "Invalid payload"}), 400

    ok, msg = transaction_service.deposit(
        db=db,
        ac_no=data.acc_no,
        amount=data.amount,
        pin=data.pin,
        request=request,
    )

    if not ok:
        return jsonify({"detail": msg}), 400

    return jsonify({"success": True, "message": msg})


# ---------------- WITHDRAW ----------------
@transaction_bp.route("/withdraw", methods=["POST"])
@roles_required("admin", "teller", "customer")
def withdraw():
    db = g.service

    payload = request.get_json()
    if not payload:
        return jsonify({"detail": "Missing JSON"}), 400

    try:
        data = TransactionRequest(**payload)
    except Exception:
        return jsonify({"detail": "Invalid payload"}), 400

    ok, msg = transaction_service.withdraw(
        db=db,
        ac_no=data.acc_no,
        amount=data.amount,
        pin=data.pin,
        request=request,
    )

    if not ok:
        return jsonify({"detail": msg}), 400

    return jsonify({"success": True, "message": msg})


# ---------------- TRANSFER ----------------
@transaction_bp.route("/transfer", methods=["POST"])
@roles_required("admin", "teller", "customer")
def transfer():
    db = g.service

    payload = request.get_json()
    if not payload:
        return jsonify({"detail": "Missing JSON"}), 400

    try:
        data = TransferRequest(**payload)
    except Exception:
        return jsonify({"detail": "Invalid payload"}), 400

    ok, msg = transaction_service.transfer(
        db=db,
        from_ac=data.acc_no,
        to_ac=data.rec_acc_no,
        amount=data.amount,
        pin=data.pin,
        request=request,
    )

    if not ok:
        return jsonify({"detail": msg}), 400

    return jsonify({"success": True, "message": msg})
