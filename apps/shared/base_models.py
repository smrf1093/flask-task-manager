from .models import db
from sqlalchemy.sql import func

class TimestampMixin(object):
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

