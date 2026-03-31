from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib import messages
from .forms import RegistroForm, LoginForm, EditarPerfilForm, CrearUsuarioAdminForm, AsignarRolForm
from .models import PerfilUsuario
from .decorators import admin_required


def registro(request):
    if request.user.is_authenticated:
        return redirect('inicio')
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'¡Bienvenido {user.first_name}! Tu cuenta fue creada exitosamente.')
            return redirect('inicio')
    else:
        form = RegistroForm()
    return render(request, 'usuarios/registro.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('inicio')
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'¡Bienvenido de vuelta, {user.first_name or user.username}!')
            return redirect(request.GET.get('next', 'inicio'))
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = LoginForm()
    return render(request, 'usuarios/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'Sesión cerrada correctamente.')
    return redirect('inicio')


@login_required
def mi_perfil(request):
    perfil = getattr(request.user, 'perfilusuario', None)
    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            perfil_obj = form.save(commit=False)
            perfil_obj.usuario = request.user
            perfil_obj.save()
            # Actualizar datos del User
            request.user.first_name = form.cleaned_data.get('first_name', request.user.first_name)
            request.user.last_name = form.cleaned_data.get('last_name', request.user.last_name)
            request.user.email = form.cleaned_data.get('email', request.user.email)
            request.user.save()
            messages.success(request, 'Perfil actualizado correctamente.')
            return redirect('mi_perfil')
    else:
        initial = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        }
        form = EditarPerfilForm(instance=perfil, initial=initial)
    return render(request, 'usuarios/mi_perfil.html', {'form': form, 'perfil': perfil})


# ─── GESTIÓN DE USUARIOS (ADMIN) ─────────────────────────────────────────────

@admin_required
def gestion_usuarios(request):
    usuarios = User.objects.filter(
        groups__name__in=['Administrador', 'Coordinador']
    ).prefetch_related('groups', 'perfilusuario').order_by('date_joined')
    usuarios_pasajeros = User.objects.filter(
        groups__isnull=True, is_superuser=False
    ).prefetch_related('groups', 'perfilusuario').order_by('date_joined')
    return render(request, 'usuarios/gestion_usuarios.html', {
        'usuarios': usuarios,
        'usuarios_pasajeros': usuarios_pasajeros,
    })


@admin_required
def crear_usuario(request):
    if request.method == 'POST':
        form = CrearUsuarioAdminForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario creado exitosamente.')
            return redirect('gestion_usuarios')
    else:
        form = CrearUsuarioAdminForm()
    return render(request, 'usuarios/form_usuario.html', {'form': form, 'titulo': 'Crear Usuario'})


@admin_required
def editar_usuario(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    perfil = getattr(usuario, 'perfilusuario', None)
    if request.method == 'POST':
        # Actualizar datos básicos
        usuario.first_name = request.POST.get('first_name', usuario.first_name)
        usuario.last_name = request.POST.get('last_name', usuario.last_name)
        usuario.email = request.POST.get('email', usuario.email)
        usuario.is_active = 'is_active' in request.POST
        usuario.save()
        messages.success(request, 'Usuario actualizado.')
        return redirect('gestion_usuarios')
    return render(request, 'usuarios/editar_usuario.html', {'usuario': usuario, 'perfil': perfil})


@admin_required
def eliminar_usuario(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    if usuario == request.user:
        messages.error(request, 'No puedes eliminar tu propio usuario.')
        return redirect('gestion_usuarios')
    if request.method == 'POST':
        usuario.delete()
        messages.success(request, 'Usuario eliminado.')
        return redirect('gestion_usuarios')
    return render(request, 'usuarios/confirmar_eliminar_usuario.html', {'usuario': usuario})


@admin_required
def asignar_rol(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = AsignarRolForm(request.POST)
        if form.is_valid():
            usuario.groups.clear()
            grupo = form.cleaned_data.get('grupo')
            if grupo:
                usuario.groups.add(grupo)
            messages.success(request, f'Rol actualizado para {usuario.username}.')
            return redirect('gestion_usuarios')
    else:
        grupo_actual = usuario.groups.first()
        form = AsignarRolForm(initial={'grupo': grupo_actual})
    return render(request, 'usuarios/asignar_rol.html', {'form': form, 'usuario': usuario})
