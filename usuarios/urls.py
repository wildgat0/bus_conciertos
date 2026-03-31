from django.urls import path
from . import views

urlpatterns = [
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('mi-perfil/', views.mi_perfil, name='mi_perfil'),
    # Admin
    path('gestion/', views.gestion_usuarios, name='gestion_usuarios'),
    path('gestion/crear/', views.crear_usuario, name='crear_usuario'),
    path('gestion/<int:pk>/editar/', views.editar_usuario, name='editar_usuario'),
    path('gestion/<int:pk>/eliminar/', views.eliminar_usuario, name='eliminar_usuario'),
    path('gestion/<int:pk>/rol/', views.asignar_rol, name='asignar_rol'),
]
