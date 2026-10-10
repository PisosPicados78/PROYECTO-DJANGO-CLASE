from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('acerca-de/', views.acerca_de_view, name='acerca_de'),
    path('tickets/', views.tickets_view, name='tickets'),
    path('tickets/nuevo/', views.nuevo_ticket_view, name='nuevo_ticket'),
    path('tickets/<int:id>/', views.detalle_ticket_view, name='detalle_ticket'),
    path('tickets/<int:id>/editar/', views.editar_ticket_view, name='editar_ticket'),
    path('tickets/<int:ticket_id>/nueva-tarea/', views.crear_tarea_view, name='crear_tarea'),
]
