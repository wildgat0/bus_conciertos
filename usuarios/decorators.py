from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from functools import wraps


def coordinador_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if request.user.is_superuser or request.user.groups.filter(name__in=['Administrador', 'Coordinador']).exists():
            return view_func(request, *args, **kwargs)
        return redirect('inicio')
    return wrapper


def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if request.user.is_superuser or request.user.groups.filter(name='Administrador').exists():
            return view_func(request, *args, **kwargs)
        return redirect('inicio')
    return wrapper
