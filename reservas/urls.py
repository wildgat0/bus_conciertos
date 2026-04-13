from django.urls import path
from . import views

urlpatterns = [
    # Públicas
    path('', views.lista_viajes, name='lista_viajes'),
    path('<int:pk>/', views.detalle_viaje, name='detalle_viaje'),
    path('mis-reservas/', views.mis_reservas, name='mis_reservas'),

    # Webpay
    path('<int:pk>/pagar/', views.iniciar_pago, name='iniciar_pago'),
    path('<int:pk>/reservar-pendiente/', views.reservar_pendiente, name='reservar_pendiente'),
    path('webpay/retorno/<int:reserva_id>/', views.retorno_webpay, name='retorno_webpay'),

    # Coordinador
    path('gestion/', views.gestion_viajes, name='gestion_viajes'),
    path('gestion/crear/', views.crear_viaje, name='crear_viaje'),
    path('gestion/<int:pk>/editar/', views.editar_viaje, name='editar_viaje'),
    path('gestion/<int:pk>/eliminar/', views.eliminar_viaje, name='eliminar_viaje'),
    path('gestion/<int:pk>/pasajeros/', views.pasajeros_viaje, name='pasajeros_viaje'),
    path('gestion/<int:pk>/pasajeros/agregar/', views.agregar_pasajero_manual, name='agregar_pasajero_manual'),
    path('gestion/<int:pk>/pasajeros/exportar/', views.exportar_pasajeros_excel, name='exportar_pasajeros_excel'),
    path('gestion/pasajero/<int:pk>/editar/', views.editar_pasajero, name='editar_pasajero'),
    path('gestion/pasajero/<int:pk>/editar-manual/', views.editar_pasajero_manual, name='editar_pasajero_manual'),
    path('gestion/pasajero/<int:pk>/eliminar/', views.eliminar_pasajero, name='eliminar_pasajero'),
    path('gestion/<int:pk>/horarios/', views.horarios_viaje, name='horarios_viaje'),
    path('gestion/horario/<int:pk>/editar/', views.editar_horario, name='editar_horario'),
    path('gestion/horario/<int:pk>/eliminar/', views.eliminar_horario, name='eliminar_horario'),

    # Admin
    path('auditoria/', views.auditoria_ganancias, name='auditoria_ganancias'),

    # Compras
    path('compras/', views.compras, name='compras'),

    # Exportar auditoría
    path('auditoria/exportar/', views.exportar_auditoria_excel, name='exportar_auditoria_excel'),
]
