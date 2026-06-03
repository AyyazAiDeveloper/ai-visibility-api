from flask import Blueprint, request
from datetime import datetime

from app import db
from app.models.profile import BusinessProfile
from app.models.pipeline_run import PipelineRun
from app.services.pipeline import PipelineService

profiles_bp = Blueprint(
    "profiles",
    __name__
)


@profiles_bp.route("/test")
def test():
    return {
        "message": "API Working"
    }



@profiles_bp.route(
    "/api/v1/profiles",
    methods=["POST"]
)
def create_profile():

    data = request.get_json()

    if not data:
        return {"error": "JSON body required"}, 400

    name = data.get("name")
    domain = data.get("domain")
    industry = data.get("industry")
    description = data.get("description")

    if not name:
        return {"error": "name is required"}, 400

    if not domain:
        return {"error": "domain is required"}, 400

    if not industry:
        return {"error": "industry is required"}, 400

    profile = BusinessProfile(
        name=name,
        domain=domain,
        industry=industry,
        description=description
    )

    db.session.add(profile)
    db.session.commit()

    return {
        "profile_uuid": profile.uuid,
        "name": profile.name,
        "domain": profile.domain,
        "status": profile.status,
        "created_at": profile.created_at.isoformat()
    }, 201



@profiles_bp.route(
    "/api/v1/profiles/<profile_uuid>",
    methods=["GET"]
)
def get_profile(profile_uuid):

    profile = BusinessProfile.query.filter_by(uuid=profile_uuid).first()

    if not profile:
        return {"error": "Profile not found"}, 404

    return {
        "profile_uuid": profile.uuid,
        "name": profile.name,
        "domain": profile.domain,
        "industry": profile.industry,
        "description": profile.description,
        "status": profile.status,
        "created_at": profile.created_at.isoformat()
    }, 200



@profiles_bp.route(
    "/api/v1/profiles/<profile_uuid>/run",
    methods=["POST"]
)
def run_pipeline(profile_uuid):

    profile = BusinessProfile.query.filter_by(uuid=profile_uuid).first()

    if not profile:
        return {"error": "Profile not found"}, 404

    pipeline_run = PipelineRun(
        profile_uuid=profile_uuid,
        status="running",
        started_at=datetime.utcnow()
    )

    db.session.add(pipeline_run)
    db.session.commit()

    try:
   
        pipeline = PipelineService()
        result = pipeline.run(profile)

        pipeline_run.status = "completed"
        pipeline_run.queries_discovered = len(result["queries"])
        pipeline_run.queries_scored = len(result["queries"])
        pipeline_run.completed_at = datetime.utcnow()

        db.session.commit()

        return {
            "status": "completed",
            "profile_uuid": profile_uuid,
            "queries_count": len(result["queries"]),
            "top_queries": result["top_queries"],
            "recommendations": result["recommendations"]
        }, 200

    except Exception as e:

  
        pipeline_run.status = "failed"
        pipeline_run.error_message = str(e)
        pipeline_run.completed_at = datetime.utcnow()

        db.session.commit()

        return {
            "status": "failed",
            "error": str(e)
        }, 500