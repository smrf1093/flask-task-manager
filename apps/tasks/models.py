from email.policy import default
from apps.shared.models import db, TimestampMixin
from sqlalchemy.sql import func


class Task(db.Model, TimestampMixin):
    """We can have attachments and many 
       other features, also tasks can be assigned to more than one employee
       also task can have status such as done should be in separated model
    """

    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    title = db.Column(db.String(255), nullable=False)
    desc = db.Column(db.Text(), nullable=True)
    # TODO: do not support time in apis for now
    due_date = db.Column(db.DateTime, default=func.now())
    status = db.Column(db.String(50), default="pending")
    assignee_id = db.Column(db.Integer(), db.ForeignKey("users.id", ondelete="CASCADE"))
    assignee = db.relationship("User", backref=db.backref("tasks", uselist=True))
    project_id = db.Column(db.Integer(), db.ForeignKey("projects.id", ondelete="CASCADE"))
    project = db.relationship("Project", backref=db.backref("tasks", uselist=True))

    def serialize(self):
      serialize_obj = dict()
      serialize_obj["id"] = self.public_id
      serialize_obj["title"] = self.title
      serialize_obj["description"] = self.desc
      serialize_obj["assignee"] = self.assignee.public_id
      serialize_obj["assignee_email"] = self.assignee.email
      serialize_obj["date"] = self.due_date
      serialize_obj["project"] = self.project.serialize()
      return serialize_obj

