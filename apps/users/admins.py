from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app import app
from .models import User, Role, UserRoles
from apps.shared.models import db

# Flask and Flask-SQLAlchemy initialization here

admin = Admin(app, name='microblog', template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Role, db.session))
admin.add_view(ModelView(UserRoles, db.session))


