from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Perfil(models.Model):
    nome = models.CharField(max_length=250, null=False)
    usuario = models.OneToOneField(User, related_name='perfil', on_delete=models.CASCADE)
    amigos = models.ManyToManyField('self')
    def convidar(self, perfil_convidado):
        convite = Convite(solicitante=self, convidado=perfil_convidado)
        convite.save()


class Convite(models.Model):
    solicitante = models.ForeignKey(Perfil, related_name='convites_feitos', on_delete=models.CASCADE)
    convidado = models.ForeignKey(Perfil, related_name='convites_recebidos', on_delete=models.CASCADE)

    def aceitar(self):
        self.convidado.amigos.add(self.solicitante)
        self.solicitante.amigos.add(self.convidado)
        self.delete()