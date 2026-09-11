import os

from celery import Celery

# Railway'da Redis plagini ulansa REDIS_URL avtomatik keladi.
# Lokal docker-compose'da esa redis://redis:6379/0
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

celery = Celery(
    "worker",
    broker=REDIS_URL,
    backend=REDIS_URL,
)

celery.conf.task_routes = {
    "app.tasks.*": {"queue": "default"}
}
