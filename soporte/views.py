from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from motor_ia.services import predecir_prioridad
from .forms import TareaForm, TicketForm
from .models import Tarea, Ticket


def home_view(request):
    context = {
        'total_tickets': Ticket.objects.count(),
        'tickets_alta': Ticket.objects.filter(prioridad='Alta').count(),
        'total_tareas': Tarea.objects.count(),
        'tickets_recientes': (
            Ticket.objects.annotate(num_tareas=Count('tareas')).order_by('-id')[:4]
            if request.user.is_authenticated
            else []
        ),
    }
    return render(request, 'soporte/home.html', context)


def acerca_de_view(request):
    return render(request, 'soporte/acerca-de.html')


@login_required
def tickets_view(request):
    tickets = Ticket.objects.annotate(num_tareas=Count('tareas')).order_by('-id')
    return render(request, 'soporte/tickets.html', {'tickets': tickets})


@login_required
def nuevo_ticket_view(request):
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            texto_analizar = f"{ticket.titulo} {ticket.descripcion}".strip()
            prioridad_detectada = predecir_prioridad(texto_analizar)
            ticket.prioridad = prioridad_detectada
            ticket.save()

            Tarea.objects.create(
                ticket=ticket,
                descripcion="Diagnóstico y revisión inicial del incidente",
                prioridad=prioridad_detectada,
            )
            return redirect('tickets')
    else:
        form = TicketForm()
    return render(request, 'soporte/nuevo-ticket.html', {'form': form})


@login_required
def detalle_ticket_view(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    return render(request, 'soporte/detalle-ticket.html', {'ticket': ticket})


@login_required
def editar_ticket_view(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('detalle_ticket', id=ticket.id)
    else:
        form = TicketForm(instance=ticket)
    return render(request, 'soporte/editar-ticket.html', {'form': form, 'ticket': ticket})


@login_required
def crear_tarea_view(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == 'POST':
        form = TareaForm(request.POST)
        if form.is_valid():
            tarea = form.save(commit=False)
            tarea.ticket = ticket
            tarea.save()
            return redirect('detalle_ticket', id=ticket.id)
    else:
        form = TareaForm()
    return render(request, 'soporte/crear-tarea.html', {'form': form, 'ticket': ticket})
