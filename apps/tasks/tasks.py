from celery import shared_task
from celery_progress.backend import ProgressRecorder
import time
from .models import ToDo
from django.utils import timezone

@shared_task(bind=True)
def long_running_task(self, seconds):
    progress_recorder = ProgressRecorder(self)
    for i in range(seconds):
        time.sleep(1)
        progress_recorder.set_progress(i + 1, seconds, f'Processed {i + 1} of {seconds} seconds')
    return 'Task completed!'

@shared_task
def create_todo_task():
    """
    A simple task that creates a ToDo item.
    Useful for testing Celery Beat.
    """
    timestamp = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
    todo = ToDo.objects.create(
        title=f"Scheduled Task Created at {timestamp}",
        description="This task was created automatically by Celery Beat.",
        is_completed=False
    )
    return f"Created ToDo: {todo.title}"
