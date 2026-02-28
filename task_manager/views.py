from django.shortcuts import render


def home(request):
    return render(request, 'home.html')


def register_page(request):
    return render(request, 'register.html')


def login_page(request):
    return render(request, 'login.html')


def tasks_page(request):
    return render(request, 'tasks.html')
