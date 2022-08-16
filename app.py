import os
from flask_api import FlaskAPI
from apps.shared.models import db
from config import config
from flask_migrate import Migrate
from apps.users.routes import users_routes
from apps.projects.routes import projects_routes
from apps.tasks.routes import tasks_routes

basedir = os.path.abspath(os.path.dirname(__file__))

def create_app(config_object):

    app = FlaskAPI(__name__)
    app.config.from_object(config_object)

    db.init_app(app)
    Migrate(app, db)

    from apps.users.models import User
    from apps.projects.models import Project, ProjectParticipant
    from apps.tasks.models import Task

    app.register_blueprint(users_routes)
    app.register_blueprint(projects_routes)
    app.register_blueprint(tasks_routes)
    print(app.url_map)
    return app

app = create_app(config.DevelopmentConfig)

if __name__ == "__main__":
    app.run(debug=True)
