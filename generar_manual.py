from fpdf import FPDF
from fpdf.enums import XPos, YPos

class Manual(FPDF):
    def header(self):
        self.set_fill_color(13, 13, 13)
        self.rect(0, 0, 210, 18, 'F')
        self.set_font('Helvetica', 'B', 13)
        self.set_text_color(255, 214, 0)
        self.set_y(4)
        self.cell(0, 10, 'Bus Conciertos - Manual de Usuario', align='C')
        self.set_text_color(0, 0, 0)
        self.ln(14)

    def footer(self):
        self.set_y(-12)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, f'Pagina {self.page_no()}  |  Bus Conciertos v1.0 - Abril 2026', align='C')

    def titulo(self, texto):
        self.set_x(self.l_margin)
        self.set_fill_color(255, 214, 0)
        self.set_text_color(13, 13, 13)
        self.set_font('Helvetica', 'B', 13)
        self.ln(3)
        self.cell(0, 9, texto, fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_text_color(0, 0, 0)
        self.ln(1)

    def subtitulo(self, texto):
        self.set_x(self.l_margin)
        self.set_font('Helvetica', 'B', 11)
        self.set_text_color(13, 13, 13)
        self.ln(2)
        self.cell(0, 7, texto, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_draw_color(255, 214, 0)
        self.set_line_width(0.5)
        self.line(self.l_margin, self.get_y(), self.l_margin + 170, self.get_y())
        self.set_text_color(0, 0, 0)
        self.ln(1)

    def parrafo(self, texto):
        self.set_x(self.l_margin)
        self.set_font('Helvetica', '', 10)
        self.multi_cell(0, 6, texto)
        self.set_x(self.l_margin)
        self.ln(1)

    def nota(self, texto):
        self.set_x(self.l_margin)
        self.set_fill_color(255, 248, 200)
        self.set_font('Helvetica', 'I', 9)
        self.set_text_color(80, 60, 0)
        self.multi_cell(0, 5, '  Nota: ' + texto, fill=True)
        self.set_x(self.l_margin)
        self.set_text_color(0, 0, 0)
        self.ln(1)

    def lista(self, items):
        self.set_font('Helvetica', '', 10)
        for item in items:
            self.set_x(self.l_margin)
            self.multi_cell(0, 6, '  -  ' + item)
        self.ln(1)

    def pasos(self, items):
        self.set_font('Helvetica', '', 10)
        for i, item in enumerate(items, 1):
            self.set_x(self.l_margin)
            self.multi_cell(0, 6, f'  {i}.  {item}')
        self.ln(1)

    def tabla(self, encabezados, filas, anchos=None):
        if anchos is None:
            col_w = 170 / len(encabezados)
            anchos = [col_w] * len(encabezados)
        self.set_font('Helvetica', 'B', 9)
        self.set_fill_color(40, 40, 40)
        self.set_text_color(255, 214, 0)
        for h, w in zip(encabezados, anchos):
            self.cell(w, 7, h, border=1, fill=True)
        self.ln()
        self.set_font('Helvetica', '', 9)
        self.set_text_color(0, 0, 0)
        fill = False
        for fila in filas:
            self.set_fill_color(245, 245, 245) if fill else self.set_fill_color(255, 255, 255)
            for celda, w in zip(fila, anchos):
                self.cell(w, 6, celda, border=1, fill=True)
            self.ln()
            fill = not fill
        self.ln(2)


pdf = Manual()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.set_margins(20, 22, 20)

# ─── PORTADA ───────────────────────────────────────────────
pdf.add_page()
pdf.set_fill_color(13, 13, 13)
pdf.rect(0, 0, 210, 297, 'F')

pdf.set_y(80)
pdf.set_font('Helvetica', 'B', 36)
pdf.set_text_color(255, 214, 0)
pdf.cell(0, 16, 'BUS CONCIERTOS', align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

pdf.set_font('Helvetica', '', 18)
pdf.set_text_color(255, 255, 255)
pdf.cell(0, 10, 'Manual de Usuario', align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

pdf.ln(10)
pdf.set_draw_color(255, 214, 0)
pdf.set_line_width(1)
pdf.line(40, pdf.get_y(), 170, pdf.get_y())

pdf.ln(15)
pdf.set_font('Helvetica', '', 12)
pdf.set_text_color(180, 180, 180)
pdf.cell(0, 8, 'Sistema de reservas de buses para conciertos', align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.cell(0, 8, 'Regiones de Santiago y Valparaiso, Chile', align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

pdf.set_y(260)
pdf.set_font('Helvetica', 'I', 10)
pdf.set_text_color(120, 120, 120)
pdf.cell(0, 8, 'Version 1.0  -  Abril 2026', align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

# ─── ÍNDICE ────────────────────────────────────────────────
pdf.add_page()
pdf.titulo('Tabla de Contenidos')
secciones = [
    '1.  Introduccion',
    '2.  Acceso al Sistema',
    '3.  Perfil de Usuario',
    '4.  Ver Viajes Disponibles',
    '5.  Realizar una Reserva',
    '6.  Pago con WebPay',
    '7.  Mis Reservas',
    '8.  Programa de Descuentos por Fidelidad',
    '9.  Funciones del Coordinador',
    '10. Funciones del Administrador',
    '11. Preguntas Frecuentes',
]
pdf.lista(secciones)

# ─── 1. INTRODUCCIÓN ───────────────────────────────────────
pdf.add_page()
pdf.titulo('1. Introduccion')
pdf.parrafo(
    'Bus Conciertos es un sistema web de reserva de asientos en buses para asistir a conciertos '
    'en las regiones de Santiago y Valparaiso, Chile. Permite a los usuarios buscar viajes disponibles, '
    'reservar asientos y pagar de forma segura en linea mediante WebPay (Transbank).'
)
pdf.subtitulo('Roles de usuario')
pdf.tabla(
    ['Rol', 'Descripcion'],
    [
        ['Pasajero', 'Usuario regular: puede ver viajes, reservar y pagar.'],
        ['Coordinador', 'Gestiona viajes, horarios y pasajeros.'],
        ['Administrador', 'Control total: usuarios, roles y reportes financieros.'],
    ],
    anchos=[45, 125]
)

# ─── 2. ACCESO ─────────────────────────────────────────────
pdf.titulo('2. Acceso al Sistema')
pdf.subtitulo('2.1 Registro')
pdf.pasos([
    'Ir a la pagina de inicio y hacer clic en Registrarse.',
    'Completar el formulario: usuario, contrasena, nombre, apellido, correo, RUT, telefono, direccion, region y fecha de nacimiento (opcional).',
    'Hacer clic en Crear cuenta.',
])

pdf.subtitulo('2.2 Iniciar sesion')
pdf.pasos([
    'Hacer clic en Iniciar sesion en la barra de navegacion.',
    'Ingresar usuario y contrasena.',
    'Hacer clic en Entrar.',
])
pdf.nota('La sesion expira automaticamente tras 15 minutos de inactividad.')

pdf.subtitulo('2.3 Cerrar sesion')
pdf.parrafo('Hacer clic en el nombre de usuario (parte superior derecha) y seleccionar Cerrar sesion.')

# ─── 3. PERFIL ─────────────────────────────────────────────
pdf.add_page()
pdf.titulo('3. Perfil de Usuario')
pdf.pasos([
    'Hacer clic en el nombre de usuario en la barra de navegacion.',
    'Seleccionar Mi Perfil.',
    'Actualizar los campos deseados: nombre, correo, RUT, telefono o direccion.',
    'Hacer clic en Guardar cambios.',
])

# ─── 4. VER VIAJES ─────────────────────────────────────────
pdf.titulo('4. Ver Viajes Disponibles')
pdf.pasos([
    'Desde el menu principal, hacer clic en Viajes.',
    'Se muestra la lista de viajes con nombre del concierto, artista, fecha, lugar, origen, destino, cupos disponibles y estado.',
    'Usar los filtros para buscar por region, fecha o concierto.',
    'Hacer clic en un viaje para ver el detalle completo.',
])
pdf.subtitulo('Estados de un viaje')
pdf.tabla(
    ['Estado', 'Significado'],
    [
        ['Disponible', 'Acepta reservas.'],
        ['Completo', 'Sin cupos disponibles.'],
        ['Cancelado', 'El viaje fue cancelado por el coordinador.'],
        ['Realizado', 'El viaje ya ocurrio.'],
    ],
    anchos=[45, 125]
)

# ─── 5. RESERVA ────────────────────────────────────────────
pdf.titulo('5. Realizar una Reserva')
pdf.pasos([
    'En el detalle del viaje, revisar los horarios de salida disponibles (ciudades de embarque, hora y precios).',
    'Seleccionar horario/ciudad de embarque, tipo de pasaje (ida y vuelta / solo ida / solo vuelta), cantidad de asientos, datos del titular (nombre, RUT, telefono, email) y ciudad de regreso si aplica.',
    'Hacer clic en Agregar al carrito.',
    'Revisar el resumen y elegir: Reservar (pendiente) o Pagar ahora.',
])
pdf.nota(
    'Una reserva pendiente no garantiza el cupo hasta que sea pagada. '
    'Los cupos se descuentan solo al confirmar el pago.'
)

# ─── 6. WEBPAY ─────────────────────────────────────────────
pdf.add_page()
pdf.titulo('6. Pago con WebPay')
pdf.pasos([
    'Al seleccionar Pagar ahora, el sistema redirige al portal de Transbank WebPay.',
    'Ingresar los datos de la tarjeta (debito o credito).',
    'Confirmar el pago.',
    'El sistema redirige de vuelta con el resultado.',
])
pdf.parrafo(
    'Pago exitoso: Se confirman las reservas y se envia un comprobante al correo registrado con el numero de orden, '
    'detalle del viaje y datos del pasajero.\n'
    'Pago fallido: La reserva queda en estado pendiente y se puede reintentar.'
)

# ─── 7. MIS RESERVAS ───────────────────────────────────────
pdf.titulo('7. Mis Reservas')
pdf.pasos([
    'Hacer clic en Mis Reservas en el menu de usuario.',
    'Se muestra el historial con: numero de orden, concierto y fecha, tipo de pasaje, estado y monto.',
    'Las reservas pagadas muestran el icono de confirmacion.',
])

# ─── 8. DESCUENTOS ─────────────────────────────────────────
pdf.titulo('8. Programa de Descuentos por Fidelidad')
pdf.parrafo(
    'El sistema premia la lealtad de los pasajeros con descuentos acumulativos basados en '
    'la cantidad total de asientos comprados a lo largo del tiempo.'
)
pdf.tabla(
    ['Asiento N ', 'Beneficio'],
    [
        ['5, 15, 25... (multiplo de 5, no de 10)', '50% de descuento'],
        ['10, 20, 30... (multiplo de 10)', 'Asiento GRATIS'],
    ],
    anchos=[110, 60]
)
pdf.nota(
    'Ejemplo: Si llevas 9 asientos comprados, tu proximo asiento (el decimo) sera gratis. '
    'Si llevas 4, el proximo tendra un 50% de descuento. '
    'En el detalle del viaje se muestra cuantos asientos te faltan para el proximo beneficio.'
)

# ─── 9. COORDINADOR ────────────────────────────────────────
pdf.add_page()
pdf.titulo('9. Funciones del Coordinador')

pdf.subtitulo('9.1 Gestion de Viajes')
pdf.lista([
    'Ver viajes: Menu Gestion > Mis Viajes muestra viajes proximos y pasados.',
    'Crear viaje: Completar formulario con concierto, origen, destino, fecha, cupos y precio.',
    'Editar viaje: Modificar datos de un viaje existente.',
    'Eliminar viaje: Solo si no tiene reservas activas asociadas.',
])

pdf.subtitulo('9.2 Gestion de Horarios')
pdf.parrafo('Desde el detalle de un viaje, hacer clic en Horarios para agregar puntos de embarque (ciudad, lugar, hora de salida, precios) o editar/eliminar horarios existentes.')

pdf.subtitulo('9.3 Gestion de Pasajeros')
pdf.parrafo('Desde Gestion > Pasajeros del viaje:')
pdf.lista([
    'Ver listado completo de pasajeros inscritos.',
    'Cambiar estado de una reserva (pendiente / pagado / cancelado).',
    'Eliminar un pasajero del viaje.',
])

pdf.subtitulo('9.4 Agregar Pasajero Manual')
pdf.parrafo('Para registrar pasajeros que pagan por transferencia, presencial o WhatsApp:')
pdf.pasos([
    'Ir a Pasajeros del viaje > Agregar pasajero manual.',
    'Completar: nombre, RUT, telefono, email, cantidad, tipo de pasaje, precio, horario y plataforma de origen.',
    'Hacer clic en Guardar.',
])

pdf.subtitulo('9.5 Exportar Pasajeros')
pdf.parrafo('Desde la vista de pasajeros, hacer clic en Exportar Excel para descargar el listado completo en formato .xlsx con todos los datos relevantes.')

pdf.subtitulo('9.6 Gestion de Conciertos (Calendario)')
pdf.lista([
    'Ver calendario: Menu Calendario lista todos los conciertos registrados.',
    'Crear concierto: Completar nombre, artista, fecha, lugar, region, descripcion e imagen.',
    'Editar / Eliminar concierto: Desde el listado del calendario.',
])

pdf.subtitulo('9.7 Compras')
pdf.parrafo('El menu Compras muestra un resumen de todas las reservas registradas en el sistema, incluyendo plataforma de origen y estado de pago.')

# ─── 10. ADMINISTRADOR ─────────────────────────────────────
pdf.add_page()
pdf.titulo('10. Funciones del Administrador')
pdf.parrafo('El administrador tiene acceso completo al sistema, incluyendo todo lo del coordinador mas las siguientes funciones:')

pdf.subtitulo('10.1 Gestion de Usuarios')
pdf.lista([
    'Ver usuarios: Menu Gestion > Usuarios lista todos los usuarios del staff.',
    'Crear usuario: Agregar nuevo coordinador o administrador.',
    'Editar usuario: Modificar datos o rol asignado.',
    'Eliminar usuario: Dar de baja a un usuario del staff.',
])

pdf.subtitulo('10.2 Asignar Roles')
pdf.pasos([
    'Ir a la lista de usuarios.',
    'Seleccionar un usuario y hacer clic en Asignar Rol.',
    'Elegir entre Administrador o Coordinador.',
    'Confirmar el cambio.',
])

pdf.subtitulo('10.3 Auditoria Financiera')
pdf.lista([
    'Menu Auditoria muestra los ingresos totales por viaje.',
    'Se puede filtrar por mes y año.',
    'Boton Exportar auditoria descarga el reporte en Excel.',
])

# ─── 11. FAQ ───────────────────────────────────────────────
pdf.add_page()
pdf.titulo('11. Preguntas Frecuentes')

faq = [
    (
        '¿Puedo reservar sin pagar de inmediato?',
        'Si. Puedes guardar una reserva como "pendiente" y pagar antes de la fecha del viaje. '
        'Sin embargo, el cupo no queda asegurado hasta el pago.'
    ),
    (
        '¿Como se que mi pago fue exitoso?',
        'Recibiras un correo de confirmacion con el comprobante de pago y numero de orden. '
        'Ademas, el estado de tu reserva en "Mis Reservas" cambiara a Pagado.'
    ),
    (
        '¿Que pasa si el viaje se cancela?',
        'El coordinador actualiza el estado del viaje a Cancelado. Se recomienda contactar al equipo '
        'por WhatsApp (boton disponible en el sitio) para coordinar el reembolso.'
    ),
    (
        '¿Como puedo saber cuantos descuentos tengo acumulados?',
        'En el detalle de cualquier viaje disponible, el sistema muestra tu progreso de fidelidad '
        'y cuantos asientos te faltan para el proximo descuento.'
    ),
    (
        '¿Puedo comprar asientos para otras personas?',
        'Si. Al crear la reserva puedes ingresar el nombre y RUT del titular (quien viaja), '
        'que puede ser distinto al usuario que realiza la compra.'
    ),
    (
        '¿Donde puedo obtener ayuda?',
        'Usa el boton de WhatsApp disponible en todas las paginas del sitio para contactar '
        'directamente al equipo de Bus Conciertos.'
    ),
]

for pregunta, respuesta in faq:
    pdf.set_x(pdf.l_margin)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(13, 13, 13)
    pdf.multi_cell(0, 6, pregunta)
    pdf.set_x(pdf.l_margin)
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(60, 60, 60)
    pdf.multi_cell(0, 6, respuesta)
    pdf.set_x(pdf.l_margin)
    pdf.ln(3)

# ─── GUARDAR ───────────────────────────────────────────────
output = 'c:/Repositorio/bus_conciertos/Manual_Usuario_BusConciertos.pdf'
pdf.output(output)
print(f'PDF generado: {output}')
