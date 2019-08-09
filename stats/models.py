from django.db import models
from django.utils import timezone
from base import models as Abstracts


class OfficialSportEvent(Abstracts.SportEvent):
    pass


class OfficialCompetition(Abstracts.Competition):
    pass


class OfficialSeason(Abstracts.Season):
    pass


class OfficialTeam(Abstracts.Team):
    pass


class OfficialPlayer(Abstracts.Player):
    pass

    
class OfficialStatistic(Abstracts.Statistic):
    pass


class OfficialVenue(Abstracts.Venue):
    pass