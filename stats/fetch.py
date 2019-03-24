import http.client
import sys
import json
from django.utils.timezone import make_aware

from datetime import datetime

from stats.models import SportEvent, Competition, Season, Team, Player, Statistic, Venue  
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
def _update_or_create(model, entries={}, 
                    filter_fields=None, 
                    change_fields=None, 
                    fixed_fields=None):
    try:
        existing_obj = model.objects.get(**filter_fields)

        for key, value in change_fields.items(): 
            setattr(existing_obj, key, value)      
        existing_obj.save()
        entries['updated'] += 1
        return existing_obj.id
    except model.DoesNotExist:
        new_obj = model(**filter_fields, **change_fields, **fixed_fields)
        new_obj.save()
        entries['imported'] += 1
        return new_obj.id
    except Exception: 
        entries['in_error'].append(Exception + str(filter_fields))
        return None


def load_season_events(season_api_id):
    season_json = API.get_season_summaries(season_api_id).json()
    games = []

    entries = {
        'imported': 0,
        'updated': 0,
        'in_error': [],
    }

    for summary in season_json['summaries']:
        if summary.get('sport_event'):
            event = summary['sport_event']
            api_id = event.get('id')
            if event.get('competitors'):
                home_team = Team.objects.get(api_id = event['competitors'][0]['id'])
                away_team = Team.objects.get(api_id = event['competitors'][1]['id']) 
            try:
                event_date = datetime.strptime(
                                utc_fetched_date(event['start_time']),
                                '%Y-%m-%dT%H:%M:%S%z')
            except: 
                event_date = None
            start_time_confirmed = event.get('start_time_confirmed', False)
            season_id = Season.objects.get(api_id = season_api_id)

            # TODO: differentiate league/cup/finals types of stage
            # on event['stage'] and event['round']

            
        if summary.get('sport_event_status'):
            status = summary['sport_event_status']
            away_team_score = status.get('away_score', 0)
            home_team_score = status.get('home_score', 0)
            winner_id = Team.objects.get(api_id = status['winner_id']) if status.get('winner_id') else None
            match_status = status.get('match_status', '')
            
            # TODO: have "scores class"
            # if status.get('period_scores'):
            #     for period in status['period_scores']:

        # TODO: fetch statistics
        # if summary.get('statistics'):
           


        filter_fields = {
            'api_id': api_id,
        }
        change_fields = {
            'home_team': home_team,
            'away_team': away_team,
            'event_date': event_date,
            'start_time_confirmed': start_time_confirmed,
            'season_id': season_id,
            'match_status': match_status,
            'away_team_score': away_team_score,
            'home_team_score': home_team_score,
            'winner_id': winner_id,
        }
        fixed_fields = {}

        obj = _update_or_create(SportEvent, entries=entries, filter_fields=filter_fields, change_fields=change_fields, fixed_fields=fixed_fields)
        games.append(obj)

    print('Seasons entries : ' + str(entries))
    return games


def load_competitions():
    comp_json = API.get_competitions_list().json()

    entries = {
        'imported': 0,
        'updated': 0,
        'in_error': [],
    }
    for competition in comp_json['competitions']:
        api_id = competition.get('id', '')
        name = competition.get('name', '')
        _update_or_create(Competition, entries, 
                        filter_fields={'api_id': api_id},
                        change_fields={'name': name}
                        )
    
    print('competitions entries : ' + str(entries))

def load_competition_seasons(competition):
    seasons_json = API.get_competition_seasons(competition).json()

    entries = {
        'imported': 0,
        'updated': 0,
        'in_error': [],
    }
    for season in seasons_json['seasons']:
        api_id = season.get('id', '')
        name = season.get('name', '')
        start_date = season.get('start_date', '')
        end_date = season.get('end_date', '')
        year = season.get('year', '')
        competition_id = Competition.objects.get(api_id = competition)

        _update_or_create(Season, entries, 
                        filter_fields={'api_id': api_id},
                        change_fields={'name': name},
                        fixed_fields={'start_date': start_date, 
                                      'end_date': end_date,
                                      'year': year,
                                      'competition_id': competition_id,
                                      })
    
    print('Seasons entries : ' + str(entries))

def load_teams(season_id):
    season_json = API.get_season_information(season_id).json()
    teams=[]
    entries = {
        'imported': 0,
        'updated': 0,
        'in_error': [],
    }
    for stage in season_json['stages']:
        for group in stage['groups']:
            for team in group['competitors']:
                api_id = team.get('id', '')
                name = team.get('name', '')
                country = team.get('country', '')
                country_code = team.get('country_code', '')
                abbreviation = team.get('abbreviation', '')

                filter_fields = {
                    'api_id': api_id,
                    'name': name,
                }
                change_fields = {
                    'country': country,
                    'country_code': country_code,
                }
                fixed_fields = {
                    'abbreviation': abbreviation,
                }

                obj = _update_or_create(Team, entries=entries, filter_fields=filter_fields, change_fields=change_fields, fixed_fields=fixed_fields)
                teams.append(obj)

    print('Seasons entries : ' + str(entries))
    return teams

def _load_team_players(tid):
    team_json = API.get_team_profile(tid).json()
    players=[]
    entries = {
        'imported': 0,
        'updated': 0,
        'in_error': [],
    }
    players_list = team_json.get('players', [])
    for player in players_list:
        api_id = player.get('id', '')
        name = player.get('name', '')
        country_code = player.get('country_code', '')
        jersey_number = player.get('abbreviation', 0)
        birthdate = player.get('date_of_birth', None)
        gender = player.get('gender', '')
        height = player.get('height', 0)
        weight = player.get('weight', 0)
        nationality = player.get('nationality', '')
        player_type = player.get('type', 'UK')
        team_id = Team.objects.get(api_id=tid)

        filter_fields = {
            'api_id': api_id,
        }
        change_fields = {
            'name': name,
            'jersey_number': jersey_number,
            'country_code': country_code,
            'team_id': team_id,
            'gender': gender,
            'height': height,
            'weight': weight,
            'player_type': player_type,
            'nationality': nationality,
        }
        fixed_fields = {
            'birthdate': birthdate,
        }

        obj = _update_or_create(Player, entries=entries, filter_fields=filter_fields, change_fields=change_fields, fixed_fields=fixed_fields)
        players.append(obj)
    print('Team {}, players : {}'.format(tid, str(entries)))


    #load manager
    manager = team_json.get('manager', None)
    if manager:
        api_id = manager.get('id', '')
        name = manager.get('name', '')
        gender = manager.get('gender', '')
        country_code = manager.get('country_code', '')
        nationality = manager.get('nationality', '')
        team_id = Team.objects.get(api_id=tid)
        player_type = "MG"

        filter_fields = {
            'api_id': api_id,
        }
        change_fields = {
            'name': name,
            'country_code': country_code,
            'team_id': team_id,
            'gender': gender,
            'player_type': player_type,
            'nationality': nationality,
        }
        fixed_fields = {}
        
        manager_obj = _update_or_create(Player, entries=entries, filter_fields=filter_fields, change_fields=change_fields, fixed_fields=fixed_fields)

        print('Team {}, manager : {}'.format(tid, name))


    #load venue
    venue = team_json.get('venue', None)
    if venue:
        api_id = venue.get('id', '')
        name = venue.get('name', '')
        city_name = venue.get('city_name', '')
        country_code = venue.get('country_code', '')
        country_name = venue.get('country_name', '')
        capacity = venue.get('capacity', 0)
        map_coordinates = venue.get('map_coordinates', (0,0))
        team_id = Team.objects.get(api_id=tid)

        filter_fields = {
            'api_id': api_id,
        }
        change_fields = {
            'name': name,
            'country_code': country_code,
            'country_name': country_name,
            'city_name': city_name,
            'capacity': capacity,
            'map_coordinates': map_coordinates,
            'team_id': team_id,
        }
        fixed_fields = {}
        venue_obj = _update_or_create(Venue, entries=entries, filter_fields=filter_fields, change_fields=change_fields, fixed_fields=fixed_fields)

        print('Team {}, venue : {}'.format(tid, name))
    
    return players

def load_complete_season(season_api_id):
    """
    Will make N API calls, where 
    N = number of teams in the season + 2
    """
    print('get teams for season %s' % season_api_id)
    team_ids = load_teams(season_api_id)

    for team_id in team_ids:
        team_obj = Team.objects.get(id=team_id)
        print('get players for team %s' % team_obj.name)

        players = _load_team_players(team_obj.api_id)

    load_season_events(season_api_id)