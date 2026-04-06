import os

from flask import Flask
from dotenv import load_dotenv

from app.config import Config
from app.models.db import init_db
from app.routes.health import health_bp
from app.routes.notes import notes_bp
from app.routes.upload import upload_bp


def create_app() -> Flask:
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object(Config)
    app.config["MAX_CONTENT_LENGTH"] = Config.MAX_CONTENT_LENGTH
    app.url_map.strict_slashes = False

    init_db()
    app.register_blueprint(health_bp)
    app.register_blueprint(notes_bp)
    app.register_blueprint(upload_bp)

    @app.get("/")
    def home():
        return {
            "message": "Cloud Notes App Running",
            "environment": app.config["ENVIRONMENT"],
            "routes": {
                "health": "/",
                "liveness": "/health/live",
                "readiness": "/health/ready",
                "notes": "/notes",
                "upload": "/upload",
            },
        }

    return app


app = create_app()


if __name__ == "__main__":
    port = int(os.getenv("PORT", str(Config.PORT)))
    debug = os.getenv("FLASK_DEBUG", str(Config.FLASK_DEBUG)).lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)
