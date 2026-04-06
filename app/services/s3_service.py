import os
from datetime import datetime, timezone
from uuid import uuid4

import boto3
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename


def get_s3_client():
    client_kwargs = {
        "service_name": "s3",
        "region_name": os.getenv("AWS_REGION", "ap-southeast-1"),
    }

    access_key = os.getenv("AWS_ACCESS_KEY_ID")
    secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    session_token = os.getenv("AWS_SESSION_TOKEN")
    endpoint_url = os.getenv("S3_ENDPOINT_URL")

    if access_key:
        client_kwargs["aws_access_key_id"] = access_key
    if secret_key:
        client_kwargs["aws_secret_access_key"] = secret_key
    if session_token:
        client_kwargs["aws_session_token"] = session_token
    if endpoint_url:
        client_kwargs["endpoint_url"] = endpoint_url

    return boto3.client(**client_kwargs)


def build_object_key(filename: str) -> str:
    safe_name = secure_filename(filename) or f"upload-{uuid4().hex}.bin"
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"uploads/{timestamp}-{uuid4().hex[:8]}-{safe_name}"


def build_file_url(bucket_name: str, object_key: str) -> str:
    public_base_url = os.getenv("S3_PUBLIC_BASE_URL")
    if public_base_url:
        return f"{public_base_url.rstrip('/')}/{object_key}"

    endpoint_url = os.getenv("S3_ENDPOINT_URL")
    if endpoint_url:
        return f"{endpoint_url.rstrip('/')}/{bucket_name}/{object_key}"

    region = os.getenv("AWS_REGION", "ap-southeast-1")
    if region == "us-east-1":
        return f"https://{bucket_name}.s3.amazonaws.com/{object_key}"
    return f"https://{bucket_name}.s3.{region}.amazonaws.com/{object_key}"


def upload_file_to_s3(file: FileStorage) -> dict:
    bucket_name = os.getenv("AWS_BUCKET_NAME")
    if not bucket_name:
        raise ValueError("Missing AWS_BUCKET_NAME. Please configure your S3 bucket first.")

    object_key = build_object_key(file.filename or "upload.bin")
    client = get_s3_client()

    extra_args = {}
    if file.mimetype:
        extra_args["ContentType"] = file.mimetype

    if extra_args:
        client.upload_fileobj(file.stream, bucket_name, object_key, ExtraArgs=extra_args)
    else:
        client.upload_fileobj(file.stream, bucket_name, object_key)

    return {
        "message": "File uploaded successfully.",
        "file_name": file.filename,
        "object_key": object_key,
        "url": build_file_url(bucket_name, object_key),
    }
