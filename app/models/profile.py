import uuid
from datetime import datetime

from app import db


class BusinessProfile(db.Model):

    __tablename__ = "business_profiles"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    uuid = db.Column(
        db.String(100),
        unique=True,
        nullable=False,
        default=lambda: str(uuid.uuid4())
    )

    name = db.Column(
        db.String(255),
        nullable=False
    )

    domain = db.Column(
        db.String(255),
        nullable=False
    )

    industry = db.Column(
        db.String(255),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    status = db.Column(
        db.String(50),
        default="created"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )