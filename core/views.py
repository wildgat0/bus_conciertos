from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from .models import Concierto
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


# ─── CALENDARIO DE CONCIERTOS (Coordinador) ──────────────────────────────────

@coordinador_required
def calendario_conciertos(request):
    hoy = timezone.now().date()
    proximos = Concierto.objects.filter(fecha__gte=hoy).order_by('fecha')
    pasados = Concierto.objects.filter(fecha__lt=hoy).order_by('-fecha')[:10]
    return render(request, 'core/calendario_conciertos.html', {
        'proximos': proximos,
        'pasados': pasados,
    })


@coordinador_required
def crear_concierto(request):
    if request.method == 'POST':
        form = ConciertoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Concierto agregado al calendario.')
            return redirect('calendario_conciertos')
    else:
        form = ConciertoForm()
    return render(request, 'core/form_concierto.html', {'form': form, 'titulo': 'Nuevo Concierto'})


@coordinador_required
def editar_concierto(request, pk):
    concierto = get_object_or_404(Concierto, pk=pk)
    if request.method == 'POST':
        form = ConciertoForm(request.POST, instance=concierto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Concierto actualizado.')
            return redirect('calendario_conciertos')
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
