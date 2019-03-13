from .views import ServiceView, check


def setup_routes(app):
    app.router.add_get("/check", check)
    app.router.add_route('*', '/service', ServiceView)
