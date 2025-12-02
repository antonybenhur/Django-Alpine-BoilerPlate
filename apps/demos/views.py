from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def todo_view(request):
    return render(request, 'demos/todo.html')

@login_required
def celery_view(request):
    return render(request, 'demos/celery.html')

@login_required
def websockets_view(request):
    return render(request, 'demos/websockets.html')

@login_required
def celery_beat_view(request):
    from django_celery_beat.models import PeriodicTask, IntervalSchedule
    from django.contrib import messages
    import json

    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            task_name = request.POST.get('task')
            period = request.POST.get('period')
            every = int(request.POST.get('every'))

            if not all([name, task_name, period, every]):
                messages.error(request, 'All fields are required')
            else:
                schedule, created = IntervalSchedule.objects.get_or_create(
                    every=every,
                    period=period,
                )
                
                PeriodicTask.objects.create(
                    interval=schedule,
                    name=name,
                    task=task_name,
                )
                messages.success(request, f'Task "{name}" scheduled successfully')
        except Exception as e:
            messages.error(request, f'Error scheduling task: {str(e)}')

    from celery import current_app
    
    # Ensure tasks are loaded
    current_app.loader.import_default_modules()
    
    # Get all registered tasks
    available_tasks = [
        task for task in current_app.tasks.keys() 
        if not task.startswith('celery.')
    ]
    available_tasks.sort()

    periodic_tasks = PeriodicTask.objects.all()
    
    # Fetch generated ToDos
    from apps.tasks.models import ToDo
    todos = ToDo.objects.all().order_by('-created_at')[:10]  # Show last 10

    return render(request, 'demos/celery_beat.html', {
        'periodic_tasks': periodic_tasks,
        'available_tasks': available_tasks,
        'todos': todos,
    })

@login_required
def todo_list_partial(request):
    from apps.tasks.models import ToDo
    from django.utils import timezone
    import datetime
    
    todos = ToDo.objects.all().order_by('-created_at')[:10]
    
    # Mark new items (created within last 5 seconds)
    now = timezone.now()
    for todo in todos:
        # Assuming created_at is timezone aware
        age = (now - todo.created_at).total_seconds()
        todo.is_new = age < 5

    return render(request, 'demos/partials/todo_list.html', {'todos': todos})

@login_required
def delete_periodic_task(request, task_id):
    from django.shortcuts import redirect
    from django.contrib import messages
    if request.method == 'POST':
        from django_celery_beat.models import PeriodicTask
        try:
            task = PeriodicTask.objects.get(id=task_id)
            task.delete()
            messages.success(request, f'Task "{task.name}" deleted successfully.')
        except PeriodicTask.DoesNotExist:
            messages.error(request, 'Task not found.')
        except Exception as e:
            messages.error(request, f'Error deleting task: {str(e)}')
    return redirect('demo_celery_beat')

@login_required
def clear_todos(request):
    from django.shortcuts import redirect
    from django.contrib import messages
    from apps.tasks.models import ToDo
    
    if request.method == 'POST':
        try:
            count, _ = ToDo.objects.all().delete()
            messages.success(request, f'Successfully deleted {count} ToDo items.')
        except Exception as e:
            messages.error(request, f'Error clearing ToDos: {str(e)}')
            
    return redirect('demo_celery_beat')

@login_required
def kanban_view(request):
    from apps.tasks.models import KanbanCard
    
    # Fetch all cards
    cards = KanbanCard.objects.all()
    
    # Organize by status
    columns = {
        'todo': cards.filter(status='todo').order_by('order'),
        'in_progress': cards.filter(status='in_progress').order_by('order'),
        'done': cards.filter(status='done').order_by('order'),
    }
    
    return render(request, 'demos/kanban.html', {'columns': columns})

@login_required
def update_kanban_card(request):
    import json
    from django.http import JsonResponse
    from apps.tasks.models import KanbanCard
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            card_id = data.get('card_id')
            new_status = data.get('status')
            new_order = data.get('order')
            
            card = KanbanCard.objects.get(id=card_id)
            card.status = new_status
            card.order = new_order
            card.save()
            
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
            
    return JsonResponse({'success': False, 'error': 'Invalid method'}, status=405)

@login_required
def create_kanban_card(request):
    from django.shortcuts import redirect
    from django.contrib import messages
    from apps.tasks.models import KanbanCard
    
    if request.method == 'POST':
        try:
            title = request.POST.get('title')
            description = request.POST.get('description')
            status = request.POST.get('status', 'todo')
            
            KanbanCard.objects.create(
                title=title,
                description=description,
                status=status
            )
            messages.success(request, 'Task created successfully.')
        except Exception as e:
            messages.error(request, f'Error creating task: {str(e)}')
            
    return redirect('demo_kanban')

@login_required
def edit_kanban_card(request, card_id):
    from django.shortcuts import redirect, get_object_or_404
    from django.contrib import messages
    from apps.tasks.models import KanbanCard
    
    if request.method == 'POST':
        try:
            card = get_object_or_404(KanbanCard, id=card_id)
            card.title = request.POST.get('title')
            card.description = request.POST.get('description')
            # Status might be updated via drag/drop, but allow it here too if needed
            # card.status = request.POST.get('status') 
            card.save()
            messages.success(request, 'Task updated successfully.')
        except Exception as e:
            messages.error(request, f'Error updating task: {str(e)}')
            
    return redirect('demo_kanban')

@login_required
def delete_kanban_card(request, card_id):
    from django.shortcuts import redirect, get_object_or_404
    from django.contrib import messages
    from apps.tasks.models import KanbanCard
    
    if request.method == 'POST':
        try:
            card = get_object_or_404(KanbanCard, id=card_id)
            card.delete()
            messages.success(request, 'Task deleted successfully.')
        except Exception as e:
            messages.error(request, f'Error deleting task: {str(e)}')
            
    return redirect('demo_kanban')
