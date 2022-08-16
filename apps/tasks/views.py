
import uuid
from datetime import datetime

from flask import request, make_response, jsonify
from flask_api import status
from flask_api.exceptions import APIException

from apps.shared.constants import ResponseKeys
from apps.shared.base_views import BaseView
from apps.shared.models import db
from apps.shared.utils import token_required
from .models import Task
from apps.users.models import User
from apps.projects.models import Project


class CreateTaskView(BaseView):
    decorators = [token_required, ]

    def validate(self, data):
        # TODO: more standard validation mechanism should be used instead of this 
        self.title, self.due_date, self.assignee_id, self.project_id = (
            data.get("title"),
            data.get("due_date"),
            data.get("assignee_id"),
            data.get("project_id")
        )
        if not all([self.title, self.due_date, self.assignee_id, self.project_id]):
            raise APIException("To create a task you must provide title, due_date, assignee_id and project_id")
        if len(self.title) < 3:
            raise APIException("The minimum length for title is 3 character")
        self.user = User.query.filter_by(public_id=self.assignee_id).first()
        if not self.user:
            raise APIException("Assignee user does not exists!")
        self.project = Project.query.filter_by(public_id=self.project_id).first()
        if not self.project:
            raise APIException("Project does not exists!")
        
        

    def post(self):
        data = request.form
        self.validate(data)
        task = Task(
            public_id=str(uuid.uuid4()),
            title=self.title,
            desc=data.get("description"),
            due_date=datetime.strptime(self.due_date, '%Y-%m-%d'),
            # TODO: can be sended by user 
            status="pending",
            assignee_id=self.user.id,
            project_id=self.project.id
        )
        db.session.add(task)
        db.session.commit()
        self.response[ResponseKeys.message] = "Task has been created successfully"
        return make_response(jsonify(self.response), status.HTTP_201_CREATED)
    
    def patch(self):
        if 'task_id' not in request.args:
            raise APIException("Task id is required")
        data = request.form
        task = Task.query.filter(Task.public_id==request.args.get('task_id')).first()
        if not task:
            raise APIException("Task does not exists")
            
        authorized_users = [user.public_id for user in task.project.participants if user.roles == User.PROJECT_MANAGER]
        authorized_users.append(task.assignee.public_id)
        
        if not data.get("title"):
            raise APIException("To update you need to provide a new title")
        if self.user.public_id not in authorized_users:
            raise APIException("You do not authorized to update this task")
        task.title = data.get("title")
        db.session.add(task)
        db.session.commit()
        self.response[ResponseKeys.message] = "Successfully updated"
        return make_response(
            jsonify(self.response),
            status.HTTP_200_OK
        )


class ListTaskView(BaseView):
    decorators = [token_required, ]

    def get(self):
        project = Project.query.filter(
            (Project.public_id==request.args.get('project_id')) & (Project.participants.any(public_id=self.user.public_id) | (Project.owner_id == self.user.public_id))
        ).first()
        if not project:
            raise APIException("Project does not exists")
        tasks = [task.serialize() for task in project.tasks]
        return jsonify(
            tasks
        )
    


class DeleteTaskAPIView(BaseView):
    decorators = [token_required, ]

    def delete(self):
        if 'task_id' not in request.args:
            raise APIException("Task id is required")
        task = Task.query.filter(Task.public_id==request.args.get('task_id')).first()
        if not task:
            raise APIException("Task does not exists")
        authorized_users = [user.public_id for user in task.project.participants if user.roles == User.PROJECT_MANAGER]
        authorized_users.append(task.assignee.public_id)
        if self.user.public_id not in authorized_users:
            raise APIException("You are not authorized")
        db.session.delete(task)
        db.session.commit()    
        self.response[ResponseKeys.message] = "Task has been deleted"
        return make_response(
            jsonify(self.response), status.HTTP_200_OK
        )
        



