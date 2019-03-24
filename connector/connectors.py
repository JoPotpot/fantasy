# Sportradar APIs

"""
API details and documentation: https://developer.sportradar.com/io-docs
"""

import requests
import time
import os

FORMAT = '.json' # only json proof
LANGUAGE = 'en' 


class HandballV2API(object):
    """Sportradar API to connect to Handball data"""

    def __init__(self, api_key='',
                 access_level='trial', timeout=5, sleep_time=1.2):
        """ Sportradar Handball V2 API Constructor

        :param api_key: key provided by Sportradar
        :param format_: response format to request from the API (json, xml)
        :param timeout: time before quitting on response (seconds)
        :param sleep_time: time to wait between requests, (free min is 1 second)
        """


        # TODO : clean get_key
        if api_key == '':
            local_path = os.path.dirname(__file__)
            filename = os.path.join(local_path, 'api_key.txt')
            f = open(filename, 'r')
            api_key = f.read()
            f.close          
        self.api_key = {'api_key': api_key}
        self.FORMAT = FORMAT # only json proof
        self.timeout = timeout
        self._sleep_time = sleep_time
        self.api_root = 'http://api.sportradar.us/'
        self.access_level = access_level
        self.language = LANGUAGE
        self.version = 2
        self.prefix = 'handball/{level}/v{ver}/{lang}/'.format(
            level=self.access_level, ver=self.version, lang=self.language)

    def _make_request(self, path):
        """Make a GET request to the API"""
        time.sleep(self._sleep_time)  # Rate limiting
        full_uri = self.api_root + path + self.FORMAT
        print('path : ' + path)
        print('full_uri : ' + full_uri)
        response = requests.get(full_uri,
                                timeout=self.timeout,
                                params=self.api_key)
        return response

    def get_competitions_list(self):
        """Provides all API available international competitions list 
        """
        path = "competitions"
        return self._make_request(self.prefix + path)

    def get_competition_seasons(self, competition_id):
        """Provides the API available seasons of a competition"""
        path = "competitions/{competition_id}/seasons".format(
            competition_id=competition_id)
        return self._make_request(self.prefix + path)

    # Not used yet
    def get_season_probabilities(self, season_id):
        """Provides each game probabilities on a competition's season"""
        path = "seasons/{season_id}/probabilities".format(
            season_id=season_id)
        return self._make_request(self.prefix + path)

    # Not used yet
    def get_season_standings(self, season_id):
        """
        Provides standings ('classement') on a competition's season
        """
        path = "seasons/{season_id}/standings".format(
            season_id=season_id)
        return self._make_request(self.prefix + path)

    # Not used yet
    def get_season_summaries(self, season_id):
        """
        Provides all games summaries on a competition's season
        """
        path = "seasons/{season_id}/summaries".format(
            season_id=season_id)
        return self._make_request(self.prefix + path)

    # Not used yet
    def get_team_season_statistics(self, season_id, competitor_id):
        """
        Provides global statistics for a team on a given season
        """
        path = "seasons/{season_id}/competitors/{competitor_id}/statistics".format(
            season_id=season_id, competitor_id=competitor_id)
        return self._make_request(self.prefix + path)

    def get_team_profile(self, competitor_id):
        """Provides information on a team in a given season competition, as :
             - players list
        """
        path = "competitors/{competitor_id}/profile".format(
            competitor_id=competitor_id)
        return self._make_request(self.prefix + path)

    def get_team_summaries(self, competitor_id):
        """Provides games summaries on a team 
           in a given season competition
        """
        path = "competitors/{competitor_id}/summaries".format(
            competitor_id=competitor_id)
        return self._make_request(self.prefix + path)

    # Not used yet
    def get_versus_stats(self, team1_id, team2_id):
        """Provides all head to head summaries on two teams, as :
             - full summaries 
        """
        path = "competitors/{team1_id}/versus/{team2_id}/summaries".format(
            team1_id=team1_id, team2_id=team2_id)
        return self._make_request(self.prefix + path)

    # Not used yet
    def get_event_timeline(self, match_id):
        """Provides precise data on a specific game, as :
            - goals, injuries, and precise times
        """
        path = "sport_events/{match_id}/timeline".format(
            match_id=match_id)
        return self._make_request(self.prefix + path) 


    # following requests can be used to know which data need to be
    # fetch again, because of event change - launch every week ?
    # Not used yet
    def get_change_log(self):
        """Provides changed event (removed, date change...)"""
        path = "sport_events/updated"
        return self._make_request(self.prefix + path)

    # Not used yet
    def get_removed_events(self):
        """Provides all removed events"""
        path = "sport_events/removed"
        return self._make_request(self.prefix + path)


    # following requests could have a high cost in trial version,
    # for retreiving few informations or already known ones :
    # TO AVOID, or for exceptionnal use.
    # Not used yet
    def get_player_profile(self, player_id):
        """Provides all season teams of a player
        """
        path = "players/{player_id}/profile".format(
            player_id=player_id)
        return self._make_request(self.prefix + path)

    # Not used yet
    def get_player_summaries(self, player_id):
        """
        To be tested :
        Provides all game summaries where this player played ?
        """
        path = "players/{player_id}/summaries".format(
            player_id=player_id)
        return self._make_request(self.prefix + path)

    def get_season_information(self, season_id):
        """Provides information on a competition's season, as :
             - teams list
        """
        path = "seasons/{season_id}/info".format(
            season_id=season_id)
        return self._make_request(self.prefix + path)

    # Not used yet
    def get_event_summary(self, match_id):
        """Provides information on a specific game"""
        path = "sport_events/{match_id}/summary".format(
            match_id=match_id)
        return self._make_request(self.prefix + path)
    
    # Not used yet
    def get_daily_summaries(self, year, month, day):
        """Provides games summaries on a given date on all competitions, as :
             - short summaries 
        """
        path = "schedules/{year}-{month}-{day}/summaries".format(
            year=year, month=month, day=day)
        return self._make_request(self.prefix + path)

    # Can't be used correctly in trial version
    # def get_live_summaries(self):
    #     """Provides all games playing live
    #     """
    #     path = "schedules/live/summaries"
    #     return self._make_request(self.prefix + path)