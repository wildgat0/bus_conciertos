from django.contrib import admin
from .models import Concierto


@admin.register(Concierto)
class ConciertoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'artista', 'fecha', 'region', 'activo']
    list_filter = ['region', 'activo', 'fecha']
    search_fields = ['nombre', 'artista', 'lugar']
    ordering = ['fecha']
