from typing import Any, Dict, Optional, Tuple

from flask import Blueprint, request

from app.services.notes_service import (
    create_note as create_note_record,
    delete_note as delete_note_record,
    get_note as get_note_record,
    list_notes as list_note_records,
    update_note as update_note_record,
)


notes_bp = Blueprint("notes", __name__, url_prefix="/notes")


def _validate_payload(
    payload: Dict[str, Any], require_title: bool = True
) -> Tuple[Dict[str, Any], Optional[str]]:
    title = payload.get("title")
    content = payload.get("content", "")

    if title is None:
        if require_title:
            return {}, "Field 'title' is required."
        title = ""

    title = str(title).strip()
    content = "" if content is None else str(content)

    if require_title and not title:
        return {}, "Field 'title' cannot be empty."

    return {"title": title, "content": content}, None


@notes_bp.get("/")
def list_notes():
    items = list_note_records()
    return {"count": len(items), "items": items}


@notes_bp.get("/<int:note_id>")
def get_note(note_id: int):
    note = get_note_record(note_id)
    if note is None:
        return {"error": "Note not found."}, 404

    return note


@notes_bp.post("/")
def create_note():
    payload = request.get_json(silent=True) or {}
    note_data, error = _validate_payload(payload, require_title=True)

    if error:
        return {"error": error}, 400

    note = create_note_record(note_data["title"], note_data["content"])
    return note, 201


@notes_bp.put("/<int:note_id>")
def update_note(note_id: int):
    payload = request.get_json(silent=True) or {}
    existing_note = get_note_record(note_id)
    if existing_note is None:
        return {"error": "Note not found."}, 404

    updated_fields, error = _validate_payload(
        {
            "title": payload.get("title", existing_note["title"]),
            "content": payload.get("content", existing_note["content"]),
        },
        require_title=True,
    )

    if error:
        return {"error": error}, 400

    note = update_note_record(note_id, updated_fields["title"], updated_fields["content"])
    return note


@notes_bp.delete("/<int:note_id>")
def delete_note(note_id: int):
    deleted = delete_note_record(note_id)
    if not deleted:
        return {"error": "Note not found."}, 404

    return {"message": "Note deleted successfully."}
