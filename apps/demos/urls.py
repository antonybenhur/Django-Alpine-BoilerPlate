from django.urls import path
from . import views

urlpatterns = [
    path('todo/', views.todo_view, name='demo_todo'),
    path('celery/', views.celery_view, name='demo_celery'),
    path('celery-beat/', views.celery_beat_view, name='demo_celery_beat'),
    path('celery-beat/todos/', views.todo_list_partial, name='demo_todo_list_partial'),
    path('celery-beat/delete/<int:task_id>/', views.delete_periodic_task, name='delete_periodic_task'),
    path('celery-beat/clear-todos/', views.clear_todos, name='clear_todos'),
    path('kanban/', views.kanban_view, name='demo_kanban'),
    path('kanban/create/', views.create_kanban_card, name='create_kanban_card'),
    path('kanban/edit/<int:card_id>/', views.edit_kanban_card, name='edit_kanban_card'),
    path('kanban/delete/<int:card_id>/', views.delete_kanban_card, name='delete_kanban_card'),
    path('kanban/update/', views.update_kanban_card, name='update_kanban_card'),
    path('websockets/', views.websockets_view, name='demo_websockets'),
]
