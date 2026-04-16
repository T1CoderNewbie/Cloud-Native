import os

from app.models.db import reset_engine


def create_test_client(tmp_path):
    database_url = "sqlite:///{path}".format(path=tmp_path / "test-notes.db")
    os.environ["DATABASE_URL"] = database_url
    os.environ.pop("REDIS_URL", None)
    os.environ.pop("KAFKA_BOOTSTRAP_SERVERS", None)
    reset_engine()

    from main import create_app

    app = create_app()
    app.testing = True
    return app.test_client()


def test_health_and_notes_crud(tmp_path):
    client = create_test_client(tmp_path)

    response = client.get("/health/live")
    assert response.status_code == 200
    assert response.get_json()["status"] == "alive"

    response = client.get("/health/ready")
    assert response.status_code == 200

    response = client.post(
        "/notes",
        json={"title": "Assignment 2", "content": "Deploy on EKS with Istio"},
    )
    assert response.status_code == 201
    created_note = response.get_json()
    assert created_note["title"] == "Assignment 2"

    note_id = created_note["id"]

    response = client.get("/notes")
    assert response.status_code == 200
    assert response.get_json()["count"] == 1

    response = client.post(
        "/notes",
        json={"title": "Kafka events", "content": "Add event publishing for notes"},
    )
    assert response.status_code == 201

    response = client.put(
        "/notes/{note_id}".format(note_id=note_id),
        json={"title": "Assignment 2 Updated", "content": "RDS, Docker, Terraform"},
    )
    assert response.status_code == 200
    assert response.get_json()["title"] == "Assignment 2 Updated"

    response = client.delete("/notes/{note_id}".format(note_id=note_id))
    assert response.status_code == 200

    response = client.get("/notes/{note_id}".format(note_id=note_id))
    assert response.status_code == 404

    response = client.get("/notes?q=kafka")
    assert response.status_code == 200
    assert response.get_json()["count"] == 1
    assert response.get_json()["items"][0]["title"] == "Kafka events"

    response = client.get("/notes/export?q=kafka")
    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("application/json")
    assert "attachment; filename=\"cloud-notes-export.json\"" == response.headers["Content-Disposition"]
    assert "Kafka events" in response.get_data(as_text=True)

    response = client.get("/notes/stats?q=kafka")
    assert response.status_code == 200
    stats = response.get_json()
    assert stats["count"] == 1
    assert stats["query"] == "kafka"
    assert stats["total_title_characters"] == len("Kafka events")
    assert stats["total_content_characters"] == len("Add event publishing for notes")
    assert stats["average_content_length"] == float(len("Add event publishing for notes"))


def test_homepage_renders_notes_ui(tmp_path):
    client = create_test_client(tmp_path)

    response = client.get("/")
    page = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "Cloud Notes App" in page
    assert "Create a Note" in page
    assert "Saved Notes" in page
    assert "Export JSON" in page
    assert "Notes Stats" in page
