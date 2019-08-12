from django.db import models
from django.utils import timezone

from django.utils.translation import ugettext_lazy as _
from base import models as base_models


class OfficialSportEvent(base_models.SportEvent):
    pass


class OfficialCompetition(base_models.Competition):
    pass


class OfficialSeason(base_models.Season):
    pass


class OfficialTeam(base_models.Team):
    pass


class OfficialPlayer(base_models.Player):
    pass

    
class OfficialStatistic(base_models.Statistic):
    pass


class OfficialVenue(base_models.Venue):
    pass