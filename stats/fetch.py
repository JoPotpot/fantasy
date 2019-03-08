import http.client
import sys
import json
from datetime import datetime

from stats.models import Sport_event    


DATA_FILE = "./stats/static/data.json"

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
        
        event = Sport_event(home_team=home_team, 
                            away_team=away_team, 
                            away_team_score=away_team_score, 
                            home_team_score=home_team_score,
                            competition_name=competition_name,
                            event_date=event_date)
        event.save()

    import ipdb; ipdb.set_trace()


if __name__ == "__main__":
    if sys.argv[1] == 'fetch':
        fetch_data_json()