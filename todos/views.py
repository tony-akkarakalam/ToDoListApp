from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import TodoItem
from .forms import TodoForm

from django.utils import timezone

@login_required
def todo_list(request):
    todos = TodoItem.objects.filter(user=request.user)
    
    # Search
    query = request.GET.get('q')
    if query:
        todos = todos.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
    
    # Filter by Priority
    priority = request.GET.get('priority')
    if priority:
        todos = todos.filter(priority=priority)
    
    # Sorting
    sort = request.GET.get('sort', '-created_at')
    todos = todos.order_by(sort)

    # Dashboard Stats (calculated on the full queryset before filtering if possible, but calculating on filtered is fine too.
    # Actually dashboard should probably show TOTAL stats, not filtered stats.
    all_todos = TodoItem.objects.filter(user=request.user)
    stats = {
        'total': all_todos.count(),
        'completed': all_todos.filter(completed=True).count(),
        'pending': all_todos.filter(completed=False).count(),
        'due_today': all_todos.filter(due_date=timezone.now().date(), completed=False).count()
    }

    context = {
        'todos': todos,
        'today': timezone.now().date(),
        'priority_high': priority == 'HIGH',
        'priority_medium': priority == 'MEDIUM',
        'priority_low': priority == 'LOW',
        'sort_newest': sort == '-created_at',
        'sort_oldest': sort == 'created_at',
        'sort_due': sort == 'due_date',
        'stats': stats,
    }
    return render(request, 'todos/todo_list_final.html', context)

@login_required
def todo_create(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            return redirect('todo-list')
    else:
        form = TodoForm()
    return render(request, 'todos/todo_form.html', {'form': form})

@login_required
def todo_update(request, pk):
    todo = get_object_or_404(TodoItem, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect('todo-list')
    else:
        form = TodoForm(instance=todo)
    return render(request, 'todos/todo_form.html', {'form': form, 'todo': todo})

@login_required
def todo_delete(request, pk):
    todo = get_object_or_404(TodoItem, pk=pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('todo-list')
    return render(request, 'todos/todo_confirm_delete.html', {'todo': todo})
