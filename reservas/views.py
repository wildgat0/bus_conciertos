from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from decimal import Decimal
from django.db.models import Sum, Count, Q
from django.http import JsonResponse, HttpResponse
from django.conf import settings
import uuid
import requests
import json
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment

from .models import Viaje, Reserva
from .forms import ViajeForm, PasajeroForm
from usuarios.decorators import coordinador_required, admin_required


def cupos_pagados_usuario(user):
    return Reserva.objects.filter(usuario=user, estado='pagado').aggregate(total=Sum('cantidad'))['total'] or 0


def calcular_monto_con_descuento(precio, cupos_base, cantidad):
    """Calcula el monto total aplicando descuentos cupo a cupo según posición histórica."""
    total = Decimal('0')
    for i in range(1, cantidad + 1):
        cupo_num = cupos_base + i
        if cupo_num % 10 == 0:       # gratis
            pass
        elif cupo_num % 5 == 0:      # 50% descuento
            total += precio * Decimal('0.5')
        else:
            total += precio
    return int(total)


def mensaje_descuento_rango(cupos_base, cantidad):
    """Retorna mensaje si algún cupo en el rango tiene descuento."""
    tiene_gratis = any((cupos_base + i) % 10 == 0 for i in range(1, cantidad + 1))
    tiene_50     = any((cupos_base + i) % 5  == 0 for i in range(1, cantidad + 1))
    if tiene_gratis:
        return '🎉 ¡Uno o más cupos de esta compra son GRATIS!'
    if tiene_50:
        return '🎊 ¡Uno o más cupos incluyen 50% de descuento!'
    return None


def es_coordinador(user):
    return user.is_authenticated and (
        user.is_superuser or
        user.groups.filter(name__in=['Administrador', 'Coordinador']).exists()
    )

def es_admin(user):
    return user.is_authenticated and (
        user.is_superuser or
        user.groups.filter(name='Administrador').exists()
    )


# ─── VIAJES PÚBLICOS ────────────────────────────────────────────────────────

def lista_viajes(request):
    viajes = Viaje.objects.filter(
        estado='disponible',
        fecha_salida__date__gte=timezone.now().date()
    ).select_related('concierto').order_by('fecha_salida')
    return render(request, 'reservas/lista_viajes.html', {'viajes': viajes})


@login_required
def detalle_viaje(request, pk):
    viaje = get_object_or_404(Viaje, pk=pk)
    perfil = request.user.perfilusuario if request.user.is_authenticated and hasattr(request.user, 'perfilusuario') else None
    reserva_pendiente = None
    cupos_pagados = 0
    if request.user.is_authenticated:
        reserva_pendiente = Reserva.objects.filter(
            viaje=viaje, usuario=request.user, estado='pendiente'
        ).first()
        cupos_pagados = Reserva.objects.filter(
            viaje=viaje, usuario=request.user, estado='pagado'
        ).aggregate(total=Sum('cantidad'))['total'] or 0
    cupos_base = 0
    proximo_hito = 0
    proximo_beneficio = ''
    if request.user.is_authenticated:
        cupos_base = cupos_pagados_usuario(request.user)
        ciclo = cupos_base % 10
        if ciclo < 4:
            proximo_hito = cupos_base + (4 - ciclo)
            proximo_beneficio = '50% descuento'
        elif ciclo < 9:
            proximo_hito = cupos_base + (9 - ciclo)
            proximo_beneficio = 'Reserva GRATIS'
        else:
            proximo_hito = cupos_base + (10 - ciclo)
            proximo_beneficio = '50% descuento'
    context = {
        'viaje': viaje,
        'reserva_pendiente': reserva_pendiente,
        'cupos_pagados': cupos_pagados,
        'perfil': perfil,
        'cupos_base': cupos_base,
        'proximo_hito': proximo_hito,
        'proximo_beneficio': proximo_beneficio,
    }
    return render(request, 'reservas/detalle_viaje.html', context)


# ─── WEBPAY / TRANSBANK ──────────────────────────────────────────────────────

@login_required
def reservar_pendiente(request, pk):
    if request.method != 'POST':
        return redirect('detalle_viaje', pk=pk)

    viaje = get_object_or_404(Viaje, pk=pk, estado='disponible')

    if viaje.cupos_disponibles <= 0:
        messages.error(request, 'Lo sentimos, este viaje ya no tiene cupos disponibles.')
        return redirect('lista_viajes')

    try:
        cantidad = max(1, int(request.POST.get('cantidad', 1)))
    except (ValueError, TypeError):
        cantidad = 1

    if cantidad > viaje.cupos_disponibles:
        messages.error(request, f'Solo quedan {viaje.cupos_disponibles} cupos disponibles.')
        return redirect('detalle_viaje', pk=pk)

    cupos_base_pend = cupos_pagados_usuario(request.user)
    monto = calcular_monto_con_descuento(viaje.precio, cupos_base_pend, cantidad)

    # Reutilizar solo reserva pendiente (nunca cancelada) o crear nueva
    reserva = Reserva.objects.filter(
        viaje=viaje, usuario=request.user, estado='pendiente'
    ).first()
    if reserva:
        reserva.cantidad = cantidad
        reserva.monto = monto
        reserva.save()
    else:
        Reserva.objects.create(
            viaje=viaje,
            usuario=request.user,
            estado='pendiente',
            cantidad=cantidad,
            monto=monto,
        )

    messages.success(request, f'Reserva realizada. Recuerda pagar antes de 5 días previos al evento.')
    return redirect('mis_reservas')


@login_required
def iniciar_pago(request, pk):
    viaje = get_object_or_404(Viaje, pk=pk, estado='disponible')

    if viaje.cupos_disponibles <= 0:
        messages.error(request, 'Lo sentimos, este viaje ya no tiene cupos disponibles.')
        return redirect('lista_viajes')

    # Leer cantidad solicitada
    try:
        cantidad = max(1, int(request.POST.get('cantidad', 1)))
    except (ValueError, TypeError):
        cantidad = 1

    if cantidad > viaje.cupos_disponibles:
        messages.error(request, f'Solo quedan {viaje.cupos_disponibles} cupos disponibles.')
        return redirect('detalle_viaje', pk=pk)

    cupos_base_pago = cupos_pagados_usuario(request.user)
    monto_total = calcular_monto_con_descuento(viaje.precio, cupos_base_pago, cantidad)

    # Reutilizar solo reserva pendiente; nunca tocar pagadas ni canceladas
    reserva = Reserva.objects.filter(
        viaje=viaje, usuario=request.user, estado='pendiente'
    ).first()
    if reserva:
        reserva.estado = 'pendiente'
        reserva.cantidad = cantidad
        reserva.monto = monto_total
        reserva.orden_compra = f'BC-{uuid.uuid4().hex[:10].upper()}'
        reserva.token_webpay = None
        reserva.save()
    else:
        reserva = Reserva.objects.create(
            viaje=viaje,
            usuario=request.user,
            estado='pendiente',
            cantidad=cantidad,
            monto=monto_total,
        )

    # Si el monto es 0 (todos los cupos son gratis), confirmar sin pasar por WebPay
    if monto_total == 0:
        reserva.estado = 'pagado'
        reserva.orden_compra = f'BC-{uuid.uuid4().hex[:10].upper()}'
        reserva.save()
        messages.success(request, '¡Reserva confirmada! Tu cupo fue GRATIS por tu fidelidad. 🎉')
        return redirect('mis_reservas')

    # Iniciar transacción Webpay
    url_retorno = request.build_absolute_uri(f'/reservas/webpay/retorno/{reserva.id}/')
    headers = {
        'Tbk-Api-Key-Id': settings.TRANSBANK_COMMERCE_CODE,
        'Tbk-Api-Key-Secret': settings.TRANSBANK_API_KEY,
        'Content-Type': 'application/json',
    }
    if settings.TRANSBANK_ENVIRONMENT == 'TEST':
        base_url = 'https://webpay3gint.transbank.cl'
    else:
        base_url = 'https://webpay3g.transbank.cl'

    payload = {
        'buy_order': reserva.orden_compra,
        'session_id': f'session-{request.user.id}-{reserva.id}',
        'amount': int(reserva.monto),
        'return_url': url_retorno,
    }

    try:
        resp = requests.post(
            f'{base_url}/rswebpaytransaction/api/webpay/v1.2/transactions',
            headers=headers,
            json=payload,
            timeout=15
        )
        data = resp.json()
        if 'token' in data:
            reserva.token_webpay = data['token']
            reserva.save()
            return render(request, 'reservas/webpay_redirect.html', {
                'url': data['url'],
                'token': data['token'],
            })
        else:
            reserva.delete()
            messages.error(request, 'Error al conectar con Webpay. Intenta nuevamente.')
    except Exception as e:
        reserva.delete()
        messages.error(request, f'Error de conexión con Transbank: {str(e)}')

    return redirect('detalle_viaje', pk=pk)


@login_required
def retorno_webpay(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id, usuario=request.user)
    token = request.POST.get('token_ws') or request.GET.get('token_ws')

    if not token:
        reserva.estado = 'cancelado'
        reserva.save()
        messages.error(request, 'Pago cancelado o no completado.')
        return redirect('lista_viajes')

    headers = {
        'Tbk-Api-Key-Id': settings.TRANSBANK_COMMERCE_CODE,
        'Tbk-Api-Key-Secret': settings.TRANSBANK_API_KEY,
        'Content-Type': 'application/json',
    }
    if settings.TRANSBANK_ENVIRONMENT == 'TEST':
        base_url = 'https://webpay3gint.transbank.cl'
    else:
        base_url = 'https://webpay3g.transbank.cl'

    try:
        resp = requests.put(
            f'{base_url}/rswebpaytransaction/api/webpay/v1.2/transactions/{token}',
            headers=headers,
            timeout=15
        )
        data = resp.json()
        if data.get('response_code') == 0:
            reserva.estado = 'pagado'
            reserva.save()
            # Actualizar estado del viaje si está lleno
            if reserva.viaje.cupos_disponibles <= 0:
                reserva.viaje.estado = 'completo'
                reserva.viaje.save()
            messages.success(request, '¡Reserva confirmada! Tu pago fue procesado exitosamente.')
            return render(request, 'reservas/pago_exitoso.html', {'reserva': reserva, 'data': data})
        else:
            reserva.estado = 'cancelado'
            reserva.save()
            messages.error(request, 'El pago fue rechazado por Webpay.')
    except Exception as e:
        messages.error(request, f'Error al confirmar el pago: {str(e)}')

    return render(request, 'reservas/pago_fallido.html', {'reserva': reserva})


# ─── MIS RESERVAS ────────────────────────────────────────────────────────────

@login_required
def mis_reservas(request):
    reservas = Reserva.objects.filter(usuario=request.user).select_related('viaje__concierto')
    return render(request, 'reservas/mis_reservas.html', {'reservas': reservas})


# ─── GESTIÓN COORDINADOR ─────────────────────────────────────────────────────

@login_required
@user_passes_test(es_coordinador)
def gestion_viajes(request):
    hoy = timezone.now()
    # Marcar como realizados todos los viajes pasados que aún no lo estén
    Viaje.objects.filter(fecha_salida__lt=hoy).exclude(estado='realizado').update(estado='realizado')
    if es_admin(request.user):
        viajes = Viaje.objects.filter(fecha_salida__gte=hoy).select_related('concierto', 'coordinador')
        viajes_pasados = Viaje.objects.filter(fecha_salida__lt=hoy).select_related('concierto', 'coordinador').order_by('-fecha_salida')
    else:
        viajes = Viaje.objects.filter(coordinador=request.user, fecha_salida__gte=hoy).select_related('concierto')
        viajes_pasados = Viaje.objects.filter(coordinador=request.user, fecha_salida__lt=hoy).select_related('concierto').order_by('-fecha_salida')
    return render(request, 'reservas/gestion_viajes.html', {'viajes': viajes, 'viajes_pasados': viajes_pasados})


@login_required
@user_passes_test(es_coordinador)
def crear_viaje(request):
    from core.models import Concierto
    if request.method == 'POST':
        form = ViajeForm(request.POST)
        if form.is_valid():
            texto = form.cleaned_data['concierto_nombre'].strip()
            concierto = Concierto.objects.filter(
                Q(artista__icontains=texto) | Q(nombre__icontains=texto)
            ).first()
            if not concierto:
                form.add_error('concierto_nombre', f'No se encontró ningún concierto con "{texto}". Créalo primero en el Calendario.')
            else:
                viaje = form.save(commit=False)
                viaje.concierto = concierto
                viaje.coordinador = request.user
                viaje.save()
                messages.success(request, 'Viaje creado exitosamente.')
                return redirect('gestion_viajes')
    else:
        form = ViajeForm()
    return render(request, 'reservas/form_viaje.html', {'form': form, 'titulo': 'Crear Nuevo Viaje'})


@login_required
@user_passes_test(es_coordinador)
def editar_viaje(request, pk):
    from core.models import Concierto
    viaje = get_object_or_404(Viaje, pk=pk)
    if request.method == 'POST':
        form = ViajeForm(request.POST, instance=viaje)
        if form.is_valid():
            texto = form.cleaned_data['concierto_nombre'].strip()
            concierto = Concierto.objects.filter(
                Q(artista__icontains=texto) | Q(nombre__icontains=texto)
            ).first()
            if not concierto:
                form.add_error('concierto_nombre', f'No se encontró ningún concierto con "{texto}". Créalo primero en el Calendario.')
            else:
                viaje = form.save(commit=False)
                viaje.concierto = concierto
                viaje.save()
                messages.success(request, 'Viaje actualizado exitosamente.')
                return redirect('gestion_viajes')
    else:
        form = ViajeForm(instance=viaje)
    return render(request, 'reservas/form_viaje.html', {'form': form, 'titulo': 'Editar Viaje', 'viaje': viaje})


@login_required
@user_passes_test(es_coordinador)
def eliminar_viaje(request, pk):
    viaje = get_object_or_404(Viaje, pk=pk)
    if request.method == 'POST':
        viaje.delete()
        messages.success(request, 'Viaje eliminado.')
        return redirect('gestion_viajes')
    return render(request, 'reservas/confirmar_eliminar.html', {'objeto': viaje, 'tipo': 'viaje'})


@login_required
@user_passes_test(es_coordinador)
def pasajeros_viaje(request, pk):
    viaje = get_object_or_404(Viaje, pk=pk)
    reservas_qs = Reserva.objects.filter(viaje=viaje).exclude(estado='cancelado').select_related('usuario__perfilusuario').order_by('usuario__id', 'estado')

    # Agrupar por (usuario, estado) sumando cantidad y monto
    agrupado = {}
    for r in reservas_qs:
        key = (r.usuario_id, r.estado)
        if key not in agrupado:
            agrupado[key] = {
                'usuario': r.usuario,
                'estado': r.estado,
                'cantidad': 0,
                'monto': 0,
            }
        agrupado[key]['cantidad'] += r.cantidad
        agrupado[key]['monto'] += r.monto

    pasajeros = list(agrupado.values())
    return render(request, 'reservas/pasajeros_viaje.html', {'viaje': viaje, 'pasajeros': pasajeros, 'reservas': reservas_qs})


@login_required
@user_passes_test(es_coordinador)
def exportar_pasajeros_excel(request, pk):
    viaje = get_object_or_404(Viaje, pk=pk)
    reservas_qs = Reserva.objects.filter(viaje=viaje).exclude(estado='cancelado').select_related('usuario__perfilusuario').order_by('usuario__id', 'estado')

    # Agrupar igual que en la vista pasajeros_viaje
    agrupado = {}
    for r in reservas_qs:
        key = (r.usuario_id, r.estado)
        if key not in agrupado:
            agrupado[key] = {
                'usuario': r.usuario,
                'estado': r.estado,
                'cantidad': 0,
                'monto': 0,
            }
        agrupado[key]['cantidad'] += r.cantidad
        agrupado[key]['monto'] += r.monto
    pasajeros = list(agrupado.values())

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Pasajeros'

    header_font = Font(bold=True, color='000000')
    header_fill = PatternFill(fill_type='solid', fgColor='FFD600')
    header_align = Alignment(horizontal='center', vertical='center')

    encabezados = ['#', 'Nombre', 'RUT', 'Teléfono', 'Cupos', 'Monto', 'Estado']
    for col, texto in enumerate(encabezados, start=1):
        celda = ws.cell(row=1, column=col, value=texto)
        celda.font = header_font
        celda.fill = header_fill
        celda.alignment = header_align

    for i, p in enumerate(pasajeros, start=1):
        perfil = getattr(p['usuario'], 'perfilusuario', None)
        estado_display = {'pagado': 'Pagado', 'pendiente': 'Pendiente de Pago', 'cancelado': 'Cancelado'}.get(p['estado'], p['estado'])
        ws.append([
            i,
            p['usuario'].get_full_name() or p['usuario'].username,
            perfil.rut if perfil else '',
            perfil.telefono if perfil else '',
            p['cantidad'],
            int(p['monto']),
            estado_display,
        ])

    anchos = [5, 30, 15, 18, 8, 14, 20]
    for col, ancho in enumerate(anchos, start=1):
        ws.column_dimensions[ws.cell(row=1, column=col).column_letter].width = ancho

    nombre_archivo = f"pasajeros_{viaje.concierto.artista}_{viaje.fecha_salida.strftime('%Y%m%d')}.xlsx"
    nombre_archivo = nombre_archivo.replace(' ', '_')

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="{nombre_archivo}"'
    wb.save(response)
    return response


@login_required
@user_passes_test(es_coordinador)
def editar_pasajero(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    if request.method == 'POST':
        form = PasajeroForm(request.POST, instance=reserva)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reserva del pasajero actualizada.')
            return redirect('pasajeros_viaje', pk=reserva.viaje.pk)
    else:
        form = PasajeroForm(instance=reserva)
    return render(request, 'reservas/form_pasajero.html', {'form': form, 'reserva': reserva})


@login_required
@user_passes_test(es_coordinador)
def eliminar_pasajero(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    viaje_pk = reserva.viaje.pk
    if request.method == 'POST':
        reserva.estado = 'cancelado'
        reserva.save()
        messages.success(request, 'Pasajero eliminado del viaje.')
        return redirect('pasajeros_viaje', pk=viaje_pk)
    return render(request, 'reservas/confirmar_eliminar.html', {'objeto': reserva, 'tipo': 'pasajero'})


# ─── MÓDULO AUDITORÍA (ADMIN) ─────────────────────────────────────────────────

@login_required
@user_passes_test(es_admin)
def auditoria_ganancias(request):
    viajes = Viaje.objects.filter(estado='disponible').select_related('concierto', 'coordinador').prefetch_related('reserva_set').order_by('-fecha_salida')
    viajes_finalizados = Viaje.objects.exclude(estado='disponible').select_related('concierto', 'coordinador').prefetch_related('reserva_set').order_by('-fecha_salida')
    total_general = sum(v.ganancia_total for v in viajes)
    total_pasajeros = sum(v.cupos_ocupados for v in viajes) + sum(v.cupos_ocupados for v in viajes_finalizados)
    total_finalizados = sum(v.ganancia_total for v in viajes_finalizados)
    total_combinado = total_general + total_finalizados
    context = {
        'viajes': viajes,
        'viajes_finalizados': viajes_finalizados,
        'total_general': total_general,
        'total_pasajeros': total_pasajeros,
        'total_finalizados': total_finalizados,
        'total_combinado': total_combinado,
    }
    return render(request, 'reservas/auditoria.html', context)
