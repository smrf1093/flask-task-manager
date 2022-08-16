import uuid 
from  werkzeug.security import generate_password_hash, check_password_hash
from apps.shared.models import db
from flask_sqlalchemy import SQLAlchemy
from flask_user import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = "users"
    CHECK = "000000"
    ADMIN = "100000"
    PROJECT_MANAGER = "000010"
    DEVELOPER = "000001"

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    # User Authentication fields
    email = db.Column(db.String(255), nullable=False, unique=True)
    # TODO :omitted for this version
    # email_confirmed_at = db.Column(db.DateTime())
    password = db.Column(db.String(255), nullable=False)

    # User fields
    active = db.Column(db.Boolean())
    # Relationships
    name = db.Column(db.String(50), unique=True)
    roles = db.Column(db.String(50))

    @property
    def role_title(self):
        if self.roles == self.ADMIN:
            return "Admin"
        if self.roles == self.DEVELOPER:
            return "Developer"
        if self.roles == self.PROJECT_MANAGER:
            return "Project Manager"
        
        


