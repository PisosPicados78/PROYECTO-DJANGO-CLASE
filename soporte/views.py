from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Ticket, Tarea
from .forms import TicketForm, TareaForm

def home_view(request):
    return render(request, 'soporte/home.html')

def acerca_de_view(request):
    return render(request, 'soporte/acerca-de.html')

@login_required
def tickets_view(request):
    tickets = Ticket.objects.all()
    return render(request, 'soporte/tickets.html', {'tickets': tickets})

@login_required
def nuevo_ticket_view(request):
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
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
