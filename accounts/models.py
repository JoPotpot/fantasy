from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from base import models as base_models
class FantasyUser(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, blank=True, upload_to="avatars/")
    favorite_player = models.CharField(max_length=256, default='Siffert4ever') 

    class Meta:
        verbose_name = _('Joueur')
        verbose_name_plural = _('Joueurs')


class FantasySportEvent(base_models.SportEvent):
    pass

class FantasyCompetition(base_models.Competition):
    pass # nonsense ?


class FantasySeason(base_models.Season):
    creator = models.ForeignKey('FantasyUser', on_delete=models.SET_NULL, null=True)



class FantasyTeam(base_models.Team):
    user = models.ForeignKey('FantasyUser', on_delete=models.CASCADE)
    fantasy_season = models.ForeignKey('FantasySeason', on_delete=models.CASCADE)


class FantasyPlayer(base_models.Player):
    fantasy_team = models.ForeignKey('FantasyTeam', on_delete=models.CASCADE)

    
class FantasyStatistic(base_models.Statistic):
    pass


class FantasyVenue(base_models.Venue):
    pass # nonsense ?