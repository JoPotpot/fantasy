from django.contrib import admin
from .models import SportEvent, Competition, Season, Team, Player, Statistic, Venue

admin.site.register(Competition)
admin.site.register(Season)
admin.site.register(Team)
admin.site.register(Player)
admin.site.register(Statistic)
admin.site.register(Venue)
admin.site.register(SportEvent)
