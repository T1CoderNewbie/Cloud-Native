from typing import Any, Dict, List, Optional

from sqlalchemy import delete, desc, func, insert, or_, select, update

from app.config import Config
from app.models.db import get_engine, notes_table, row_to_note
from app.services.cache_service import delete_keys, get_json, set_json
from app.services.event_service import publish_event


NOTES_CACHE_KEY = "notes:all"


def _note_cache_key(note_id: int) -> str:
    return "notes:{note_id}".format(note_id=note_id)


def list_notes(search_term: str = "") -> List[Dict[str, Any]]:
    normalized_search = search_term.strip().lower()

    if normalized_search:
        pattern = "%{term}%".format(term=normalized_search)
        statement = (
            select(notes_table)
            .where(
                or_(
                    func.lower(notes_table.c.title).like(pattern),
                    func.lower(notes_table.c.content).like(pattern),
                )
            )
            .order_by(desc(notes_table.c.updated_at), desc(notes_table.c.id))
        )

        with get_engine().connect() as connection:
            rows = connection.execute(statement).mappings().all()

        return [row_to_note(row) for row in rows]

    cached_items = get_json(NOTES_CACHE_KEY)
    if cached_items is not None:
        return cached_items

    statement = select(notes_table).order_by(desc(notes_table.c.updated_at), desc(notes_table.c.id))

    with get_engine().connect() as connection:
        rows = connection.execute(statement).mappings().all()

    items = [row_to_note(row) for row in rows]
    set_json(NOTES_CACHE_KEY, items, Config.CACHE_TTL_SECONDS)
    return items


def get_note_stats(search_term: str = "") -> Dict[str, Any]:
    items = list_notes(search_term)
    total_notes = len(items)
    total_title_characters = sum(len(note.get("title", "")) for note in items)
    total_content_characters = sum(len(note.get("content", "")) for note in items)

    average_content_length = 0
    if total_notes:
        average_content_length = round(total_content_characters / total_notes, 2)

    return {
        "count": total_notes,
        "query": search_term.strip(),
        "total_title_characters": total_title_characters,
        "total_content_characters": total_content_characters,
        "average_content_length": average_content_length,
    }


def list_recent_notes(limit: int = 5) -> List[Dict[str, Any]]:
    safe_limit = max(1, min(limit, 20))
    statement = select(notes_table).order_by(desc(notes_table.c.updated_at), desc(notes_table.c.id)).limit(safe_limit)

    with get_engine().connect() as connection:
        rows = connection.execute(statement).mappings().all()

    return [row_to_note(row) for row in rows]


def get_note(note_id: int) -> Optional[Dict[str, Any]]:
    cache_key = _note_cache_key(note_id)
    cached_note = get_json(cache_key)
    if cached_note is not None:
        return cached_note

    statement = select(notes_table).where(notes_table.c.id == note_id)
    with get_engine().connect() as connection:
        row = connection.execute(statement).mappings().first()

    if row is None:
        return None

    note = row_to_note(row)
    set_json(cache_key, note, Config.CACHE_TTL_SECONDS)
    return note


def create_note(title: str, content: str) -> Dict[str, Any]:
    with get_engine().begin() as connection:
        result = connection.execute(insert(notes_table).values(title=title, content=content))
        note_id = result.inserted_primary_key[0]
        row = connection.execute(
            select(notes_table).where(notes_table.c.id == note_id)
        ).mappings().one()

    note = row_to_note(row)
    delete_keys(NOTES_CACHE_KEY)
    set_json(_note_cache_key(note["id"]), note, Config.CACHE_TTL_SECONDS)
    publish_event("note.created", note)
    return note


def update_note(note_id: int, title: str, content: str) -> Optional[Dict[str, Any]]:
    with get_engine().begin() as connection:
        result = connection.execute(
            update(notes_table)
            .where(notes_table.c.id == note_id)
            .values(title=title, content=content, updated_at=func.now())
        )
        if result.rowcount == 0:
            return None

        row = connection.execute(
            select(notes_table).where(notes_table.c.id == note_id)
        ).mappings().first()

    if row is None:
        return None

    note = row_to_note(row)
    delete_keys(NOTES_CACHE_KEY, _note_cache_key(note_id))
    set_json(_note_cache_key(note_id), note, Config.CACHE_TTL_SECONDS)
    publish_event("note.updated", note)
    return note


def delete_note(note_id: int) -> bool:
    with get_engine().begin() as connection:
        row = connection.execute(
            select(notes_table).where(notes_table.c.id == note_id)
        ).mappings().first()
        if row is None:
            return False

        connection.execute(delete(notes_table).where(notes_table.c.id == note_id))

    deleted_note = row_to_note(row)
    delete_keys(NOTES_CACHE_KEY, _note_cache_key(note_id))
    publish_event("note.deleted", deleted_note)
    return True
