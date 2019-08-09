from django.contrib import admin
from .models import OfficialSportEvent, OfficialCompetition, OfficialSeason, OfficialTeam, OfficialPlayer, OfficialStatistic, OfficialVenue

@admin.register(OfficialPlayer)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'player_type', 'birthdate', 'country_code', 'height', 'weight', 'team_id')

    list_filter = (
        ('team_id', admin.RelatedFieldListFilter),
        ('player_type', admin.ChoicesFieldListFilter),
        ('country_code', admin.AllValuesFieldListFilter),
    )
    search_fields = ['name']


@admin.register(OfficialStatistic)
class StatisticAdmin(admin.ModelAdmin):
    list_display = ('player_id', 'game_id', 'goals_scored', 'yellow_cards', 'red_cards', 'suspensions' ,'seven_m_goals', 'field_goals', 'assists', 'technical_fouls', 'steals', 'blocks', 'saves',)

    list_filter = (
        ('game_id', admin.RelatedFieldListFilter),
    )

    search_fields = ['player_id__name']


@admin.register(OfficialCompetition)
class CompetitionAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(OfficialSeason)
class SeasonAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name', 'start_date', 'end_date', 'year', 'competition_id',)

@admin.register(OfficialTeam)
class TeamAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name', 'country', 'country_code', 'abbreviation', 'manager_id', 'venue_id',) 

@admin.register(OfficialVenue)
class VenueAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name', 'city_name', 'country_code', 'country_name', 'capacity', 'team_id',) 

@admin.register(OfficialSportEvent)
class SportEventAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('home_team', 'home_team_score', 'away_team_score', 'away_team', 'season_id', 'event_date', 'start_time_confirmed', 'match_status', 'winner_id',)