from flask import Blueprint

from app.services.cache_service import check_cache
from app.models.db import check_database


health_bp = Blueprint("health", __name__, url_prefix="/health")


@health_bp.get("/live")
def liveness_probe():
    return {"status": "alive"}, 200


@health_bp.get("/ready")
def readiness_probe():
    db_ok, db_message = check_database()
    cache_ok, cache_message = check_cache()

    overall_ok = db_ok and cache_ok
    if cache_message == "disabled":
        overall_ok = db_ok

    status_code = 200 if overall_ok else 503
    return {
        "status": "ready" if overall_ok else "degraded",
        "checks": {
            "database": {"ok": db_ok, "message": db_message},
            "redis": {"ok": cache_ok, "message": cache_message},
        },
    }, status_code
