import os
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

from sqlalchemy import Column, DateTime, Integer, MetaData, String, Table, Text, create_engine, func, text
from sqlalchemy.engine import Engine, RowMapping
from sqlalchemy.exc import SQLAlchemyError


BASE_DIR = Path(__file__).resolve().parents[2]
DEFAULT_DATABASE_PATH = BASE_DIR / "data" / "notes.db"

metadata = MetaData()

notes_table = Table(
    "notes",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("title", String(255), nullable=False),
    Column("content", Text, nullable=False, default=""),
    Column("created_at", DateTime(timezone=True), nullable=False, server_default=func.now()),
    Column(
        "updated_at",
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    ),
)

_engine: Optional[Engine] = None


def get_database_url() -> str:
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return database_url
    return "sqlite:///{path}".format(path=DEFAULT_DATABASE_PATH)


def _ensure_sqlite_directory(database_url: str) -> None:
    if not database_url.startswith("sqlite:///"):
        return

    sqlite_path = database_url.replace("sqlite:///", "", 1)
    if sqlite_path == ":memory:":
        return

    db_path = Path(sqlite_path)
    if not db_path.is_absolute():
        db_path = BASE_DIR / db_path
    db_path.parent.mkdir(parents=True, exist_ok=True)


def get_engine() -> Engine:
    global _engine

    if _engine is None:
        database_url = get_database_url()
        _ensure_sqlite_directory(database_url)

        connect_args = {}
        if database_url.startswith("sqlite"):
            connect_args["check_same_thread"] = False

        _engine = create_engine(
            database_url,
            future=True,
            pool_pre_ping=True,
            connect_args=connect_args,
        )

    return _engine


def reset_engine() -> None:
    global _engine

    if _engine is not None:
        _engine.dispose()
    _engine = None


def init_db() -> None:
    metadata.create_all(get_engine())


def row_to_note(row: RowMapping) -> Dict[str, Any]:
    note = dict(row)
    for key in ("created_at", "updated_at"):
        value = note.get(key)
        if hasattr(value, "isoformat"):
            note[key] = value.isoformat()
    return note


def check_database() -> Tuple[bool, str]:
    try:
        with get_engine().connect() as connection:
            connection.execute(text("SELECT 1"))
        return True, "ok"
    except SQLAlchemyError as exc:
        return False, str(exc)
