import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()


BASE_DIR = Path(__file__).resolve().parents[1]


class Config:
    APP_NAME = "Cloud Notes App"
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    PORT = int(os.getenv("PORT", "5000"))
    FLASK_DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", str(10 * 1024 * 1024)))
    CACHE_TTL_SECONDS = int(os.getenv("CACHE_TTL_SECONDS", "60"))
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "sqlite:///{path}".format(path=BASE_DIR / "data" / "notes.db"),
    )
    REDIS_URL = os.getenv("REDIS_URL", "")
    KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "")
    KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "cloud-notes.events")
    AWS_REGION = os.getenv("AWS_REGION", "ap-southeast-1")
    AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME", "")
    S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL", "")
    S3_PUBLIC_BASE_URL = os.getenv("S3_PUBLIC_BASE_URL", "")
