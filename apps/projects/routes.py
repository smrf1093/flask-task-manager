from apps.shared.constants import blueprints_prefix
from flask import Blueprint
from .views import CreateProjectView, CreateProjectMemberView, ListProjectView

projects_routes = Blueprint(
    "projects", __name__, url_prefix=blueprints_prefix.format("projects")
)
projects_routes.add_url_rule(
    "/create/", view_func=CreateProjectView.as_view("create-project"), methods=["POST",]
)
projects_routes.add_url_rule(
    "/add-member/", view_func=CreateProjectMemberView.as_view("create-project-member"), methods=["POST",]
)
projects_routes.add_url_rule(
    "/", view_func=ListProjectView.as_view("list-project"), methods=["GET",]
)
