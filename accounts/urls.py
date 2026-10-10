from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.registro_view, name='registro'),
    path('grupos/', views.grupos_view, name='grupos'),
    path('grupos/editar/<int:id>/', views.editar_grupo_view, name='editar_grupo'),
]
