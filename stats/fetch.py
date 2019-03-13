import http.client
import sys
import json
import logging

from datetime import datetime

from stats.models import SportEvent, Competition, Season, Team, Player, Statistics  
from connector import connectors

_log = logging.getLogger(__name__)


DATA_FILE = "./stats/static/data.json"
API = connectors.HandballV2API()


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
        existing_comp = Competition.objects.filter(api_id=api_id)
        if len(existing_comp):
            try:
                comp = existing_comp[0]
                comp.name = name
                entries['updated'] += 1
                comp.save()
            except:
                entries['in_error'].append(comp)
        else:
            try:
                comp = Competition(api_id=api_id, name=name)
                comp.save()
                entries['imported'] += 1
            except:
                entries['in_error'].append(comp)
    
    _log.info('competitions entries : ' + entries)
    print('competitions entries : ' + entries)

def load_competition_seasons(competition_id):
    seasons_json = API.get_competition_seasons(competition_id).json()

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
        competition = Competition.objects.get(api_id = competition_id)

        existing_season = Season.objects.filter(api_id=api_id)
        if len(existing_season):
            try:
                season = existing_season[0]
                season.name = name
                entries['updated'] += 1
                season.save()
            except:
                entries['in_error'].append(season)
        else:
            try:
                season = Season(api_id=api_id, 
                                name=name, 
                                start_date=start_date, 
                                end_date=end_date,
                                year=year,
                                competition=competition,
                                )
                season.save()
                entries['imported'] += 1
            except:
                entries['in_error'].append(season)
    
    _log.info('Seasons entries : ' + str(entries))
    print('Seasons entries : ' + str(entries))





if __name__ == "__main__":
    if sys.argv[1] == 'fetch':
        fetch_data_json()