from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django_ratelimit.decorators import ratelimit
from .forms import TodoForm, UserCreationForm, LoginForm
from .models import Todo


def index(request):
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
    item_list = []
    if request.user.id:
        item_list = Todo.objects.filter(creator=request.user).order_by("-date")
    form = TodoForm()
    page = {
        "forms": form,
        "list": item_list,
        "title": "TODO LIST",
    }
    return render(request, "index.html", page)


def remove(request, item_id):
    todos = Todo.objects.raw(f"SELECT * FROM todo_todo WHERE id={item_id};")
    for todo in todos:
        todo.delete()
        messages.info(request, "Todo was deleted.")
    return redirect("/")


def user_signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "signup.html", {"form": form})

#@ratelimit(key='ip', rate='5/m', method='POST', block=True)
def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect("/")
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect("/")
