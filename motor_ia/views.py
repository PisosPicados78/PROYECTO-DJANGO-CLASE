from django.shortcuts import render
from .services import predecir_prioridad


def probar_ia_view(request):
    contexto = {}
    if request.method == 'POST':
        texto = request.POST.get('texto', '').strip()
        contexto['texto'] = texto
        if texto:
            contexto['resultado'] = predecir_prioridad(texto)
        else:
            contexto['error'] = 'Ingresa la descripción de un problema técnico para evaluarlo.'
    return render(request, 'motor_ia/probar_ia.html', contexto)
