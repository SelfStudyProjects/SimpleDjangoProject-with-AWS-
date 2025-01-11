from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from .models import Todo
from .forms import TodoForm
from django.contrib.auth.decorators import login_required

class TodoListView(ListView):
    model = Todo
    template_name = 'todo/todo_list.html'
    context_object_name = 'todos'

@login_required
def todo_list(request):
    todos = Todo.objects.filter(user=request.user)
    return render(request, 'todo/todo_list.html', {'todos': todos})

@login_required
def add_todo(request):
    if request.method == 'POST':
        title = request.POST['title']
        Todo.objects.create(user=request.user, title=title)
        return redirect('todo_list')
    return render(request, 'todo/add_todo.html')

@login_required
def edit_todo(request, todo_id):
    todo = Todo.objects.get(id=todo_id, user=request.user)
    if request.method == 'POST':
        todo.title = request.POST['title']
        todo.save()
        return redirect('todo_list')
    return render(request, 'todo/edit_todo.html', {'todo': todo})

@login_required
def delete_todo(request, todo_id):
    todo = Todo.objects.get(id=todo_id, user=request.user)
    todo.delete()
    return redirect('todo_list')