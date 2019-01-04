from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from perfil.models import *


# Create your views here.

@login_required
def index(request):
    todos_perfis =Perfil.objects.all()
    perfil_logado = get_perfil_logado(request)
    amigos_do_perfil_logado = []
    perfis = []

    for perfil in perfil_logado.amigos.all():
        amigos_do_perfil_logado.append(perfil)



    for perfil in todos_perfis:
        if not perfil.nome == perfil_logado.nome and perfil not in amigos_do_perfil_logado:
            perfis.append(perfil)

    return render(request, 'index.html', {'perfil_logado': get_perfil_logado(request),
                                          'perfis': perfis})

@login_required
def get_perfil_logado(request):
    return request.user.perfil

@login_required
def exibir_perfil(request, perfil_id):
    perfil = Perfil.objects.get(id=perfil_id)
    perfil_logado = get_perfil_logado(request)
    ja_eh_amigo = perfil in perfil_logado.amigos.all()

    return render(request, 'perfil.html',
                  {'perfil': perfil,
                   'ja_eh_amigo':ja_eh_amigo})


@login_required
def exibir_perfil_logado(request):
    perfil_logado = get_perfil_logado(request)

    return render(request, 'perfil_logado.html',
                  {'perfil_logado': perfil_logado})


@login_required
def convidar(request, perfil_id):
    perfil_convidado = Perfil.objects.get(id=perfil_id)
    perfil_logado = get_perfil_logado(request)
    perfil_logado.convidar(perfil_convidado)
    return redirect('index')


@login_required
def aceitar(request, convite_id):
    convite = Convite.objects.get(id=convite_id)
    convite.aceitar()
    return redirect('index')