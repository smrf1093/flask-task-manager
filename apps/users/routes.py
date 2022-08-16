from apps.shared.constants import blueprints_prefix
from flask import Blueprint
from .views import RegisterView, LoginView

users_routes = Blueprint(
    "users", __name__, url_prefix=blueprints_prefix.format("users")
)
users_routes.add_url_rule(
    "/register/", view_func=RegisterView.as_view("register"), methods=["POST",]
)
users_routes.add_url_rule(
    "/login/", view_func=LoginView.as_view("login"), methods=["POST",]
)