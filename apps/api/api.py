from ninja import NinjaAPI
from ninja.security import django_auth

api = NinjaAPI(
    title="Django Boilerplate API",
    version="1.0.0",
    description="API for Django Boilerplate",
)

@api.get("/hello")
def hello(request):
    return {"message": "Hello World"}

@api.get("/me", auth=django_auth)
def me(request):
    return {
        "username": request.user.username,
        "email": request.user.email,
    }

from apps.demos.api import router as demos_router
from apps.tasks.api import router as tasks_router

api.add_router("/todos", demos_router)
api.add_router("/tasks", tasks_router)


