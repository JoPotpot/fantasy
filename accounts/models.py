from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from base import models as Abstracts

class FantasyPlayer(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, blank=True, upload_to="avatars/")
    favorite_player = models.CharField(max_length=256, default='Siffert4ever') 

    class Meta:
        verbose_name = _('Joueur')
        verbose_name_plural = _('Joueurs')

class FantasyTeam(Abstracts.Team):
    pass