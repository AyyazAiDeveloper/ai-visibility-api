import uuid
from datetime import datetime
from app import db


class PipelineRun(db.Model):

    __tablename__ = "pipeline_runs"

    id = db.Column(db.Integer, primary_key=True)

    uuid = db.Column(
        db.String(100),
        unique=True,
        default=lambda: str(uuid.uuid4())
    )

    profile_uuid = db.Column(db.String(100), nullable=False)

    status = db.Column(db.String(50), default="running")

    queries_discovered = db.Column(db.Integer, default=0)
    queries_scored = db.Column(db.Integer, default=0)

    tokens_used = db.Column(db.Integer, default=0)

    error_message = db.Column(db.Text, nullable=True)

    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)