from flask import Flask
from flask_cors import CORS

from app.core.middleware import attach_supabase_middleware
from app.core.security import refresh_cookie_middleware

# Blueprints
from app.routes.auth_routes import auth_bp
from app.routes.account_routes import account_bp
from app.routes.transaction_routes import transaction_bp
from app.routes.update_routes import update_bp
from app.routes.history_routes import history_bp
from app.routes.debug_routes import debug_bp


def create_app():
    app = Flask(__name__)

    # -------------------- CORS --------------------
    CORS(
        app,
        supports_credentials=True,
        origins=[
            "http://localhost:3000",
            "https://rupee-wave-flask.vercel.app",
            "https://rupee-wave-flask.onrender.com",
        ],
    )

    # -------------------- Middlewares --------------------
    # These functions MODIFY the app directly.
    attach_supabase_middleware(app)
    refresh_cookie_middleware(app)

    # ------------------- Blueprints -------------------
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(account_bp, url_prefix="/account")
    app.register_blueprint(transaction_bp, url_prefix="/transaction")
    app.register_blueprint(update_bp, url_prefix="/update")
    app.register_blueprint(history_bp, url_prefix="/history")
    app.register_blueprint(debug_bp, url_prefix="/debug")

    return app
