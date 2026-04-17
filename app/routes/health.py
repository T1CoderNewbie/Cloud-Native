from flask import Blueprint

from app.services.cache_service import check_cache
from app.models.db import check_database
from app.services.notes_service import list_notes


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


@health_bp.get("/summary")
def health_summary():
    db_ok, db_message = check_database()
    cache_ok, cache_message = check_cache()

    note_count = None
    if db_ok:
        note_count = len(list_notes())

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
        "note_count": note_count,
    }, status_code
