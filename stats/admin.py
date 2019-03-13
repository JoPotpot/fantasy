from django.contrib import admin
from .models import SportEvent, Competition, Season, Team, Player, Statistics 

admin.site.register(SportEvent)
admin.site.register(Competition)
admin.site.register(Season)
admin.site.register(Team)
admin.site.register(Player)
admin.site.register(Statistics)