from django.contrib import admin
from .models import FantasySportEvent, FantasyCompetition, FantasySeason, FantasyTeam, FantasyPlayer, FantasyStatistic, FantasyVenue

admin.site.register(FantasySportEvent)
admin.site.register(FantasyCompetition)
admin.site.register(FantasySeason)
admin.site.register(FantasyTeam)
admin.site.register(FantasyPlayer)
admin.site.register(FantasyStatistic)
admin.site.register(FantasyVenue)