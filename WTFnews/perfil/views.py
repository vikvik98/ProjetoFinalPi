from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from perfil.models import *


# Create your views here.

@login_required
def index(request):
    return render(request, 'index.html', {'perfil_logado': get_perfil_logado(request)})

@login_required
def get_perfil_logado(request):
    return request.user.perfil


