import json
import os
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from kafka import KafkaProducer
from kafka.errors import KafkaError


_producer: Optional[KafkaProducer] = None


def get_kafka_producer() -> Optional[KafkaProducer]:
    global _producer

    bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
    if not bootstrap_servers:
        return None

    if _producer is None:
        try:
            _producer = KafkaProducer(
                bootstrap_servers=[server.strip() for server in bootstrap_servers.split(",") if server.strip()],
                value_serializer=lambda value: json.dumps(value).encode("utf-8"),
            )
        except KafkaError:
            return None
        except Exception:
            return None

    return _producer


def publish_event(event_type: str, payload: Dict[str, Any]) -> None:
    producer = get_kafka_producer()
    if producer is None:
        return

    topic = os.getenv("KAFKA_TOPIC", "cloud-notes.events")
    event = {
        "event_type": event_type,
        "payload": payload,
        "occurred_at": datetime.now(timezone.utc).isoformat(),
    }

    try:
        producer.send(topic, event)
        producer.flush(timeout=5)
    except KafkaError:
        return
