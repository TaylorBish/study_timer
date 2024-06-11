from flask import Blueprint

from study_timer.routes.user_route import user_route
def init_routes(app):
    app.register_blueprint(user_route)