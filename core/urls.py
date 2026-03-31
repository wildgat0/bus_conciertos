from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('quienes-somos/', views.quienes_somos, name='quienes_somos'),
    path('calendario/', views.calendario_conciertos, name='calendario_conciertos'),
    path('calendario/nuevo/', views.crear_concierto, name='crear_concierto'),
    path('calendario/<int:pk>/editar/', views.editar_concierto, name='editar_concierto'),
    path('calendario/<int:pk>/eliminar/', views.eliminar_concierto, name='eliminar_concierto'),
]
