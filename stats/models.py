from django.db import models
from django.utils import timezone



class SportEvent(models.Model):
    
    home_team = models.ForeignKey('Team', related_name='home_team', on_delete=models.SET_NULL, null=True)
    away_team = models.ForeignKey('Team', related_name='away_team', on_delete=models.SET_NULL, null=True)
    home_team_score = models.IntegerField(default=0)
    away_team_score = models.IntegerField(default=0)
    competition_name = models.ForeignKey('Competition', on_delete=models.SET_NULL, null=True)
    event_date = models.DateField(null=True)
    
    def __str__(self):
        return self.home_team + ' ' + str(self.home_team_score) + ' - ' + str(self.away_team_score) + ' ' + self.away_team

    # def __unicode__(self):
    #     return 

    def get_winner(self):
        if self.home_team_score > self.away_team_score:
            winner = self.home_team
        elif self.home_team_score < self.away_team_score:
            winner = self.away_team
        else:
            winner = 'Draw'
        return winner


class Competition(models.Model):
    
    api_id = models.CharField(max_length=256, default='') 
    name = models.CharField(max_length=256, default='')
        
    def __str__(self):
        return self.name + ' (' + self.api_id + ')'


class Season(models.Model):
    
    api_id = models.CharField(max_length=256, default='') 
    name = models.CharField(max_length=256, default='')
    start_date = models.DateField()
    end_date = models.DateField()
    year = models.CharField(max_length=10)
    competition_id = models.ForeignKey('Competition', on_delete=models.SET_NULL, null=True)
    team_ids = models.ManyToManyField('Team')

    def __str__(self):
        return self.name + ' (' + self.api_id + ')'


class Team(models.Model):

    api_id = models.CharField(max_length=256, default='')
    name = models.CharField(max_length=256, default='')
    country = models.CharField(max_length=64, default='')
    country_code = models.CharField(max_length=4, default='')
    abbreviation = models.CharField(max_length=10, default='')
    manager_id = models.ForeignKey('Player', on_delete=models.SET_NULL, null=True)
    competition_ids = models.ManyToManyField('Competition')
    def __str__(self):
        return self.name + ' (' + self.api_id + ')'


class Player(models.Model):

    LEFT_BACK = 'LB'
    RIGHT_BACK = 'RB'
    LEFT_WING = 'LW'
    RIGHT_WING = 'RW'
    GOALKEEPER = 'G'
    PIVOT = 'P'
    CENTER_BACK = 'CB'
    MANAGER = 'MG'
    UNKNOWN = 'UK'
    ROLE_CHOICES = (
        (LEFT_BACK, 'Left back'),
        (RIGHT_BACK, 'Right back'),
        (LEFT_WING, 'Left wing'),
        (RIGHT_WING, 'Right wing'),
        (GOALKEEPER, 'Goal keeper'),
        (PIVOT, 'Pivot'),
        (CENTER_BACK, 'Center back'),
        (MANAGER, 'Manager'),
        (UNKNOWN, 'Unknown'),
    )

    api_id = models.CharField(max_length=256, default='')
    name = models.CharField(max_length=256, default='')
    player_type = models.CharField(
        max_length=2,
        choices=ROLE_CHOICES,
        default=UNKNOWN,
    )
    gender = models.CharField(max_length=20, default='')
    birthdate = models.DateField(null=True)
    nationality = models.CharField(max_length=256, default='')
    country_code = models.CharField(max_length=4, default='')
    height = models.IntegerField(null=True)
    weight = models.IntegerField(null=True)
    jersey_number = models.IntegerField(null=True)
    team_id = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name + ' - ' + self.team_id.name + ' (' + self.api_id + ')'


class Statistic(models.Model):
    
    player_id = models.ForeignKey('Player', on_delete=models.SET_NULL, null=True)
    game_id = models.ForeignKey('SportEvent', on_delete=models.SET_NULL, null=True)
    yellow_cards = models.IntegerField()
    red_cards = models.IntegerField()
    suspensions = models.IntegerField()
    goals_scored = models.IntegerField()
    seven_m_goals = models.IntegerField()
    field_goals = models.IntegerField()
    assists = models.IntegerField()
    technical_fouls = models.IntegerField()
    steals = models.IntegerField()
    blocks = models.IntegerField()
    saves = models.IntegerField()

    def __str__(self):
        return self.player.name + ' (' + self.game.name + ')'

class Venue(models.Model):
    api_id = models.CharField(max_length=256, default='')
    name = models.CharField(max_length=256, default='')
    city_name = models.CharField(max_length=256, default='')
    country_code = models.CharField(max_length=4, default='')
    country_name = models.CharField(max_length=256, default='')
    capacity = models.IntegerField()
    team_id = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)

    #TODO : cut it into 2 coordinates
    map_coordinates = models.CharField(max_length=256, default='')
