from django import forms
from .models import Tarea, Ticket


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['titulo', 'descripcion', 'imagen']
        labels = {
            'titulo': 'Título del incidente',
            'descripcion': 'Descripción detallada',
            'imagen': 'Captura del error',
        }
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Error al iniciar el servidor de facturación',
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe el problema, pasos para reproducirlo o mensajes mostrados...',
            }),
            'imagen': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
            }),
        }


class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['descripcion', 'prioridad']
        labels = {
            'descripcion': 'Descripción de la tarea',
            'prioridad': 'Nivel de prioridad',
        }
        widgets = {
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Detalle de la acción técnica a ejecutar...',
            }),
            'prioridad': forms.Select(attrs={'class': 'form-select'}),
        }
