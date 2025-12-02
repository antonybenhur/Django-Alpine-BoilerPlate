from ninja import Router, Schema
from .tasks import long_running_task
from ninja.security import django_auth

router = Router(tags=["tasks"])

class TaskStartSchema(Schema):
    seconds: int

@router.post("/start", auth=django_auth)
def start_task(request, payload: TaskStartSchema):
    task = long_running_task.delay(payload.seconds)
    return {"task_id": task.id}
