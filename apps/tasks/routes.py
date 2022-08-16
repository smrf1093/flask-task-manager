from apps.shared.constants import blueprints_prefix
from flask import Blueprint
from .views import CreateTaskView, ListTaskView, DeleteTaskAPIView

tasks_routes = Blueprint(
    "tasks", __name__, url_prefix=blueprints_prefix.format("tasks")
)

tasks_routes.add_url_rule(
    "/create/", view_func=CreateTaskView.as_view("create-task"), methods=["POST", "PATCH"]
)

tasks_routes.add_url_rule(
    "/delete/", view_func=DeleteTaskAPIView.as_view("delete-task"), methods=["DELETE",]
)

tasks_routes.add_url_rule(
    "/", view_func=ListTaskView.as_view("list-task"), methods=["GET",]
)