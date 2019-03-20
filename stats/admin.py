from django.contrib import admin
from .models import SportEvent, Competition, Season, Team, Player, Statistic, Venue

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'player_type', 'birthdate', 'country_code', 'height', 'weight', 'team_id')
    list_display_links = ('team_id',)

    list_filter = (
        ('team_id', admin.RelatedFieldListFilter),
        ('player_type', admin.ChoicesFieldListFilter),
        ('country_code', admin.AllValuesFieldListFilter),
    )


admin.site.register(Competition)
admin.site.register(Season)
admin.site.register(Team)
admin.site.register(Statistic)
admin.site.register(Venue)
admin.site.register(SportEvent)
