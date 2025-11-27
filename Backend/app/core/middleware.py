from flask import g
from app.core.supabase_client import get_public_client, get_service_client


def attach_supabase_middleware(app):
    """
    Flask equivalent of the FastAPI middleware.
    Uses Flask's 'g' context object for per-request storage.
    """

    @app.before_request
    def add_supabase_clients():
        g.supabase = get_public_client()
        g.service = get_service_client()

    return app
