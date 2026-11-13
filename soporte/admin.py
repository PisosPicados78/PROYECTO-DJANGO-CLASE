from django.contrib import admin
from .models import Ticket, Tarea

class TareaInline(admin.TabularInline):
    model = Tarea
    extra = 1

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'prioridad')
    list_filter = ('prioridad',)
    search_fields = ('titulo', 'descripcion')
    inlines = [TareaInline]

@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = ('descripcion', 'prioridad', 'ticket')
    list_filter = ('prioridad',)
    search_fields = ('descripcion',)
