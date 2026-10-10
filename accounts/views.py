from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .forms import RegistroForm, GrupoForm

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistroForm()
    return render(request, 'accounts/registro.html', {'form': form})

@login_required
def grupos_view(request):
    grupos = Group.objects.all()
    if request.method == 'POST':
        form = GrupoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('grupos')
    else:
        form = GrupoForm()
    return render(request, 'accounts/grupos.html', {'grupos': grupos, 'form': form})

@login_required
def editar_grupo_view(request, id):
    grupo = get_object_or_404(Group, id=id)
    if request.method == 'POST':
        form = GrupoForm(request.POST, instance=grupo)
        if form.is_valid():
            form.save()
            return redirect('grupos')
    else:
        form = GrupoForm(instance=grupo)
    return render(request, 'accounts/editar_grupo.html', {'form': form, 'grupo': grupo})
