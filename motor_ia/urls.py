from django.urls import path
from . import views

urlpatterns = [
    path('', views.probar_ia_view, name='probar_ia'),
]
