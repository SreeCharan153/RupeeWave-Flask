from flask import g
from app.utils.cookie_tools import set_cookie
from app.utils.jwt_tools import ACCESS_TTL


def refresh_cookie_middleware(app):
    """
    Flask equivalent of FastAPI refresh_cookie_middleware.
    If a route sets request.new_access_token, we refresh the atm_token cookie.
    """

    @app.before_request
    def init_flag():
        # initialize empty token attribute
        g.new_access_token = None

    @app.after_request
    def refresh_cookie(response):
        new_access = getattr(g, "new_access_token", None)
        if new_access:
            set_cookie(
                response,
                "atm_token",
                new_access,
                max_age=int(ACCESS_TTL.total_seconds()),
            )
        return response

    return app
