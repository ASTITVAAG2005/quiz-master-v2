# celery_tasker.py
from celery import Task

class FlaskTask(Task):
    def __call__(self, *args, **kwargs):
        from app import create_app  # ✅ Delayed import to avoid circular error
        app = create_app()
        with app.app_context():
            return self.run(*args, **kwargs)
