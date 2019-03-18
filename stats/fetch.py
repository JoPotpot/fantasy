import http.client
import sys
import json

from datetime import datetime

from stats.models import SportEvent, Competition, Season, Team, Player, Statistics  
from connector import connectors


DATA_FILE = "./stats/static/data.json"
API = connectors.HandballV2API()

"""
param filter_fields: requested fields to recognize duplicates
param change_fields: fields that will be updated
param fixed_fields: fields that wont be updated, but used at creation
"""
def _update_from_API(model, entries={}, 
                    filter_fields=None, 
                    change_fields=None, 
                    fixed_fields=None):
    try:
        existing_obj = model.objects.get(**filter_fields)

        for key, value in change_fields.items(): 
            setattr(existing_obj, key, value)      
        existing_obj.save()
        entries['updated'] += 1

    except model.DoesNotExist:
        new_obj = model(**filter_fields, **change_fields, **fixed_fields)
        new_obj.save()
        entries['imported'] += 1
    except Exception: 
        entries['in_error'].append(Exception + str(filter_fields))


def fetch_data_json():
    conn = http.client.HTTPSConnection("api.sportradar.com")
    api_key = "wumub272m2pku55ws9q9kvp9" 
    nantes_id =  "sr:competitor:24069"
    conn.request("GET", "/handball/trial/v2/fr/competitors/%s/summaries.json?api_key=%s" % (nantes_id, api_key) )


    res = conn.getresponse()
    data = res.read()

    f = open(DATA_FILE, 'w+')
    f.write(data.decode("utf-8"))

    f.close()
    return f

def load_data_json():
    f = open(DATA_FILE, 'r')
    f_json = json.load(f)
    
    games = f_json['summaries']
    for game in games:
        home_team = game['sport_event']['competitors'][0]['name'] if game['sport_event']['competitors'] else '<home_team>'
        away_team = game['sport_event']['competitors'][1]['name'] if game['sport_event']['competitors'] else '<away_team>'
        away_team_score = game['sport_event_status']['away_score'] if game['sport_event_status'].get('away_score') else 0
        home_team_score = game['sport_event_status']['home_score'] if game['sport_event_status'].get('home_score') else 0
        competition_name = game['sport_event']['sport_event_context']['competition']['name'] if game['sport_event']['sport_event_context'] else '<Competition_name>'

        date = game['sport_event']['start_time'] 
        event_date = datetime.strptime(date[0:10],'%Y-%m-%d') or None
        
        event = SportEvent(home_team=home_team, 
                            away_team=away_team, 
                            away_team_score=away_team_score, 
                            home_team_score=home_team_score,
                            competition_name=competition_name,
                            event_date=event_date)
        event.save()


def load_competitions():
    comp_json = API.get_competitions_list().json()

    entries = {
        'imported': 0,
        'updated': 0,
        'in_error': [],
    }
    for competition in comp_json['competitions']:
        api_id = competition['id'] if competition.get('id') else ''
        name = competition['name'] if competition.get('name') else ''
        _update_from_API(Competition, entries, 
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
        api_id = season['id'] if season.get('id') else ''
        name = season['name'] if season.get('name') else ''
        start_date = season['start_date'] if season.get('start_date') else ''
        end_date = season['end_date'] if season.get('end_date') else ''
        year = season['year'] if season.get('year') else ''
        competition_id = Competition.objects.get(api_id = competition)

        _update_from_API(Season, entries, 
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

    entries = {
        'imported': 0,
        'updated': 0,
        'in_error': [],
    }
    for team in season_json['stages'][0]['groups'][0]['competitors']:
        api_id = team['id'] if team.get('id') else ''
        name = team['name'] if team.get('name') else ''
        country = team['country'] if team.get('country') else ''
        country_code = team['country_code'] if team.get('country_code') else ''
        abbreviation = team['abbreviation'] if team.get('abbreviation') else ''

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

        _update_from_API(Team, entries=entries, filter_fields=filter_fields, change_fields=change_fields, fixed_fields=fixed_fields)
    print('Seasons entries : ' + str(entries))






