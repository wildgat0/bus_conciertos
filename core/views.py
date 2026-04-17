import os
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse, FileResponse, Http404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Concierto, PreguntaFrecuente
from .forms import ConciertoForm
from usuarios.decorators import coordinador_required


def inicio(request):
    hoy = timezone.now().date()
    conciertos_santiago = Concierto.objects.filter(
        region='santiago', fecha__gte=hoy, activo=True
    ).order_by('fecha')[:6]
    conciertos_valparaiso = Concierto.objects.filter(
        region='valparaiso', fecha__gte=hoy, activo=True
    ).order_by('fecha')[:6]
    context = {
        'conciertos_santiago': conciertos_santiago,
        'conciertos_valparaiso': conciertos_valparaiso,
    }
    return render(request, 'core/inicio.html', context)


def quienes_somos(request):
    return render(request, 'core/quienes_somos.html')


def preguntas_frecuentes(request):
    preguntas = PreguntaFrecuente.objects.filter(activo=True)
    return render(request, 'core/preguntas_frecuentes.html', {'preguntas': preguntas})


# ─── CALENDARIO DE CONCIERTOS (Coordinador) ──────────────────────────────────

@coordinador_required
def calendario_conciertos(request):
    hoy = timezone.now().date()
    proximos = Concierto.objects.filter(fecha__gte=hoy).order_by('fecha')
    pasados = Concierto.objects.filter(fecha__lt=hoy).order_by('-fecha')[:10]
    return render(request, 'core/calendario_conciertos.html', {
        'proximos': proximos,
        'pasados': pasados,
        'form': ConciertoForm(),
    })


@coordinador_required
def crear_concierto(request):
    if request.method == 'POST':
        form = ConciertoForm(request.POST)
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if form.is_valid():
            form.save()
            if is_ajax:
                return JsonResponse({'ok': True})
            messages.success(request, 'Concierto agregado al calendario.')
            return redirect('calendario_conciertos')
        else:
            if is_ajax:
                errors = {field: list(errs) for field, errs in form.errors.items()}
                return JsonResponse({'ok': False, 'errors': errors})
    else:
        form = ConciertoForm()
    return render(request, 'core/form_concierto.html', {'form': form, 'titulo': 'Nuevo Concierto'})


@coordinador_required
def editar_concierto(request, pk):
    concierto = get_object_or_404(Concierto, pk=pk)
    if request.method == 'POST':
        form = ConciertoForm(request.POST, instance=concierto)
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if form.is_valid():
            form.save()
            if is_ajax:
                return JsonResponse({'ok': True})
            messages.success(request, 'Concierto actualizado.')
            return redirect('calendario_conciertos')
        else:
            if is_ajax:
                errors = {field: list(errs) for field, errs in form.errors.items()}
                return JsonResponse({'ok': False, 'errors': errors})
    else:
        form = ConciertoForm(instance=concierto)
    return render(request, 'core/form_concierto.html', {'form': form, 'titulo': 'Editar Concierto', 'concierto': concierto})


@coordinador_required
def eliminar_concierto(request, pk):
    concierto = get_object_or_404(Concierto, pk=pk)
    if request.method == 'POST':
        concierto.delete()
        messages.success(request, 'Concierto eliminado del calendario.')
        return redirect('calendario_conciertos')
    return render(request, 'core/confirmar_eliminar_concierto.html', {'concierto': concierto})


@login_required
def descargar_manual(request):
    grupos = [g.name for g in request.user.groups.all()]
    if not (request.user.is_superuser or 'Administrador' in grupos or 'Coordinador' in grupos):
        raise Http404
    ruta = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Manual_Usuario_BusConciertos.pdf')
    if not os.path.exists(ruta):
        raise Http404
    return FileResponse(open(ruta, 'rb'), as_attachment=True, filename='Manual_Usuario_BusConciertos.pdf')
