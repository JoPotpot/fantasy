import http.client
import sys
import json
from django.utils.timezone import make_aware

from datetime import datetime

from stats.models import OfficialSportEvent, OfficialCompetition, OfficialSeason, OfficialTeam, OfficialPlayer, OfficialStatistic, OfficialVenue  
from connector import connectors


DATA_FILE = "./stats/static/data.json"
API = connectors.HandballV2API()

"""
param filter_fields: requested fields to recognize duplicates
param change_fields: fields that will be updated
param fixed_fields: fields that wont be updated, but used at creation
"""

def utc_fetched_date(date):
    if date[22] == ':':
        begin = date[0:-3]
        end = date[-2:]
        return begin + end
    return date

def _log(obj, created):
    action = "created" if created else "updated"
    print("{} - {} ({})- has been {}.".format(obj.__class__.__name__, str(obj), str(obj.api_id) or '', action))

def load_competitions():
    comp_json = API.get_competitions_list().json()

    for competition in comp_json['competitions']:
        api_id = competition.get('id', '')
        obj, created = OfficialCompetition.objects.get_or_create(api_id=api_id)
        obj.name = competition.get('name', '')
        obj.save()
        _log(obj, created)

def load_competition_seasons(competition):
    seasons_json = API.get_competition_seasons(competition).json()

    for season in seasons_json['seasons']:
        api_id = season.get('id', '')
        obj, created = OfficialSeason.objects.get_or_create(api_id=api_id)
        obj.name = season.get('name', '')
        obj.start_date = season.get('start_date', '')
        obj.end_date = season.get('end_date', '')
        obj.year = season.get('year', '')
        obj.competition_id = OfficialCompetition.objects.get(api_id = competition)

        obj.save()
        _log(obj, created)

def load_teams(season_id):
    season_json = API.get_season_information(season_id).json()
    teams=[]
    season_obj = OfficialSeason.objects.get(api_id=season_id)
    for stage in season_json['stages']:
        for group in stage['groups']:
            for team in group['competitors']:
                api_id = team.get('id', '')
                obj, created = OfficialTeam.objects.get_or_create(api_id=api_id)
                obj.name = team.get('name', '')
                obj.country = team.get('country', '')
                obj.country_code = team.get('country_code', '')
                obj.abbreviation = team.get('abbreviation', '')
                obj.season_ids.add(season_obj)
                obj.save()

                teams.append(obj)
                _log(obj, created)

    return teams

def _load_team_players(tid):
    team_json = API.get_team_profile(tid).json()
    team_obj = OfficialTeam.objects.get(api_id=tid)
    players=[]

    players_list = team_json.get('players', [])
    for player in players_list:
        
        api_id = player.get('id', '')
        obj, created = OfficialPlayer.objects.get_or_create(api_id=api_id)

        obj.name = player.get('name', '')
        obj.country_code = player.get('country_code', '')
        obj.jersey_number = player.get('abbreviation', 0)
        obj.birthdate = player.get('date_of_birth', None)
        obj.gender = player.get('gender', '')
        obj.height = player.get('height', 0)
        obj.weight = player.get('weight', 0)
        obj.nationality = player.get('nationality', '')
        obj.player_type = player.get('type', 'UK')
        obj.team_id = OfficialTeam.objects.get(api_id=tid)

        obj.save()
        _log(obj, created)
        players.append(obj)


    #load manager
    manager = team_json.get('manager', None)
    if manager:
        api_id = manager.get('id', '')
        manager_obj, man_created = OfficialPlayer.objects.get_or_create(api_id=api_id)
        manager_obj.name = manager.get('name', '')
        manager_obj.gender = manager.get('gender', '')
        manager_obj.country_code = manager.get('country_code', '')
        manager_obj.nationality = manager.get('nationality', '')
        manager_obj.team_id = OfficialTeam.objects.get(api_id=tid)
        manager_obj.player_type = "MG"

        manager_obj.save()
        team_obj.manager_id = manager_obj
        _log(manager_obj, man_created)

    #load venue
    venue = team_json.get('venue', None)
    if venue:
        api_id = venue.get('id', '')
        venue_obj, ven_created = OfficialVenue.objects.get_or_create(api_id=api_id)
        venue_obj.name = venue.get('name', '')
        venue_obj.city_name = venue.get('city_name', '')
        venue_obj.country_code = venue.get('country_code', '')
        venue_obj.country_name = venue.get('country_name', '')
        venue_obj.capacity = venue.get('capacity', 0)
        venue_obj.map_coordinates = venue.get('map_coordinates', (0,0))
        venue_obj.team_id = OfficialTeam.objects.get(api_id=tid)

        venue_obj.save()        
        team_obj.venue_id = venue_obj
        _log(venue_obj, ven_created)
    team_obj.save()
    return players

def load_season_events(season_api_id):
    season_json = API.get_season_summaries(season_api_id).json()
    games = []

    for summary in season_json['summaries']:
        event = summary.get('sport_event')
        obj, created = OfficialSportEvent.objects.get_or_create(api_id=event.get('id'))
        if event.get('competitors'):
            obj.home_team = OfficialTeam.objects.get(api_id = event['competitors'][0]['id'])
            obj.away_team = OfficialTeam.objects.get(api_id = event['competitors'][1]['id']) 
        try:
            obj.event_date = datetime.strptime(
                            utc_fetched_date(event['start_time']),
                            '%Y-%m-%dT%H:%M:%S%z')
        except: 
            obj.event_date = None
        obj.start_time_confirmed = event.get('start_time_confirmed', False)
        obj.season_id = OfficialSeason.objects.get(api_id = season_api_id)

        # TODO: differentiate league/cup/finals types of stage
        # on event['stage'] and event['round']

            
        if summary.get('sport_event_status'):
            status = summary['sport_event_status']
            obj.away_team_score = status.get('away_score', 0)
            obj.home_team_score = status.get('home_score', 0)
            obj.winner_id = OfficialTeam.objects.get(api_id = status['winner_id']) if status.get('winner_id') else None
            obj.match_status = status.get('match_status', '')
            
            # TODO: have "scores class"
            # if status.get('period_scores'):
            #     for period in status['period_scores']:

        # load statistics
        stats = summary.get('statistics', {})
        totals = stats.get('totals', {})
        for competitor in totals.get('competitors', []):
            for player in competitor.get('players'):
                player_id = player.get('id', '')
                player_name = player.get('name', '')
                player_obj = OfficialPlayer.objects.get_or_create(api_id=player_id, name=player_name, defaults={'team_id': OfficialTeam.objects.get(api_id=competitor.get('id'))})
                stat_obj, stat_created = OfficialStatistic.objects.get_or_create(
                                                        player_id=player_obj[0],
                                                        game_id=obj)
                stat_elt = player.get('statistics', {})
                stat_obj.yellow_cards = stat_elt.get('yellow_cards', 0)
                stat_obj.red_cards = stat_elt.get('red_cards', 0)
                stat_obj.suspensions = stat_elt.get('suspensions', 0)
                stat_obj.goals_scored = stat_elt.get('goals_scored', 0)
                stat_obj.seven_m_goals = stat_elt.get('seven_m_goals', 0)
                stat_obj.field_goals = stat_elt.get('field_goals', 0)
                stat_obj.assists = stat_elt.get('assists', 0)
                stat_obj.technical_fouls = stat_elt.get('technical_fouls', 0)
                stat_obj.steals = stat_elt.get('steals', 0)
                stat_obj.blocks = stat_elt.get('blocks', 0)
                stat_obj.saves = stat_elt.get('saves', 0)
                stat_obj.save()
                # _log(stat_obj, stat_created)

    
        obj.save()
        games.append(obj)
        _log(obj, created)
    return games

def load_complete_season(season_api_id):
    """
    Will make N API calls, where 
    N = number of teams in the season + 2
    """
    print('get teams for season %s' % season_api_id)
    team_ids = load_teams(season_api_id)

    for team_id in team_ids:
        team_obj = OfficialTeam.objects.get(id=team_id.id)
        print('get players for team %s' % team_obj.name)

        players = _load_team_players(team_obj.api_id)

    load_season_events(season_api_id)