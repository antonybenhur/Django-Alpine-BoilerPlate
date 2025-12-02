from typing import List
from ninja import Router, Schema
from django.shortcuts import get_object_or_404
from .models import Todo
from ninja.security import django_auth

router = Router(tags=["todos"])

class TodoSchema(Schema):
    id: int
    title: str
    completed: bool

class TodoCreateSchema(Schema):
    title: str

@router.get("/", response=List[TodoSchema], auth=django_auth)
def list_todos(request):
    return Todo.objects.filter(user=request.user).order_by('-created_at')

@router.post("/", response=TodoSchema, auth=django_auth)
def create_todo(request, payload: TodoCreateSchema):
    todo = Todo.objects.create(user=request.user, **payload.dict())
    return todo

@router.put("/{todo_id}", response=TodoSchema, auth=django_auth)
def update_todo(request, todo_id: int, completed: bool):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    todo.completed = completed
    todo.save()
    return todo

@router.delete("/{todo_id}", auth=django_auth)
def delete_todo(request, todo_id: int):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    todo.delete()
    return {"success": True}
