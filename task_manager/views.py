from django.shortcuts import render


def home(request):
    return render(request, 'home.html')


def register_page(request):
    return render(request, 'register.html')


def login_page(request):
    return render(request, 'login.html')


def dashboard_page(request):
    return render(request, 'dashboard.html')


def tasks_page(request):
    return render(request, 'tasks.html')


def calendar_page(request):
    return render(request, 'calendar.html')


def settings_page(request):
    return render(request, 'settings.html')
