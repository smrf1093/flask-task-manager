import uuid

from flask import request, make_response, jsonify
from flask_api import status
from flask_api.exceptions import APIException

from apps.shared.constants import ResponseKeys
from apps.shared.base_views import BaseView
from apps.shared.models import db
from apps.shared.utils import token_required
from .models import Project
from apps.users.models import User


class CreateProjectView(BaseView):
    decorators = [token_required, ]

    def validate(self, data):
        self.participants_emails, self.name = (
            data.get("participants_emails"),
            data.get("name"),
        )
        if not self.name:
            raise APIException(f"Dear {self.user.email}, name are required to create a project")
        if Project.query.filter_by(name=self.name).first():
            raise APIException(f"A project with this name ({self.name}) already exists")
        self.participants_emails = [item.strip() for item in self.participants_emails.split(',')]
        if self.participants_emails:
            for email in self.participants_emails:
                user = User.query.filter_by(email=email).first()
                if not user:
                    raise APIException(f"Email {email} does not exists")
    
    def post(self):
        data = request.form
        self.validate(data)
        project = Project(
            public_id=str(uuid.uuid4()),
            name=self.name,
            owner_id=self.user.public_id
        ) 
        if self.participants_emails and len(self.participants_emails) > 0:
            for email in self.participants_emails:
                project.participants.append(User.query.filter_by(email=email).first())
        db.session.add(project)
        db.session.commit()
        
        self.response[ResponseKeys.message] = "Project has been created successfully"
        return make_response(jsonify(self.response), status.HTTP_201_CREATED)


class CreateProjectMemberView(BaseView):
    decorators = [token_required, ]

    def post(self):
        return super().post()


class ListProjectView(BaseView):
    decorators = [token_required, ]

    def get(self):
        projects = [project.serialize() for project in Project.query.filter((Project.owner_id == self.user.public_id) | (Project.participants.any(public_id=self.user.public_id)))]
        return jsonify(
            projects
        )