from botocore.exceptions import BotoCoreError, ClientError
from flask import Blueprint, request

from app.services.s3_service import upload_file_to_s3


upload_bp = Blueprint("upload", __name__, url_prefix="/upload")


@upload_bp.post("/")
def upload_file():
    if "file" not in request.files:
        return {"error": "Missing file in form-data. Use the key 'file'."}, 400

    file = request.files["file"]
    if not file or not file.filename:
        return {"error": "Please choose a file before uploading."}, 400

    try:
        upload_result = upload_file_to_s3(file)
    except ValueError as exc:
        return {"error": str(exc)}, 500
    except (BotoCoreError, ClientError) as exc:
        return {"error": "S3 upload failed.", "details": str(exc)}, 502

    return upload_result, 201
