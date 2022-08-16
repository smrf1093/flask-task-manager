import email
from apps.shared.models import db, TimestampMixin

class Project(db.Model, TimestampMixin):
    __tablename__ = "projects"
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique = True)
    owner_id = db.Column(db.Integer(), db.ForeignKey("users.id", ondelete="CASCADE"))
    name = db.Column(db.String(255), nullable=False, unique=True)
    participants = db.relationship("User", secondary="projects_participants")

    def serialize(self):
        serialize_obj = dict()
        serialize_obj["public_id"] = self.public_id
        serialize_obj["name"] = self.name
        serialize_obj["owner_id"] = self.owner_id
        serialize_obj["participants"] = []
        for participant in self.participants:
            serialize_obj["participants"].append({
                "id": participant.public_id,
                "email": participant.email,
                "role": participant.role_title
            })
        return serialize_obj



class ProjectParticipant(db.Model, TimestampMixin):
    __tablename__ = "projects_participants"
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(
        db.Integer(), db.ForeignKey("projects.id", ondelete="CASCADE")
    )
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id", ondelete="CASCADE"))
