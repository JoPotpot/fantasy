from django.db import models
from django.utils import timezone


class SportEvent(models.Model):

    api_id = models.CharField(max_length=256, default='') 
    home_team = models.ForeignKey('Team', related_name='home_team', on_delete=models.SET_NULL, null=True)
    away_team = models.ForeignKey('Team', related_name='away_team', on_delete=models.SET_NULL, null=True)
    home_team_score = models.IntegerField(default=0)
    away_team_score = models.IntegerField(default=0)
    season = models.ForeignKey('Season', on_delete=models.SET_NULL, null=True)
    event_date = models.DateTimeField(null=True)
    start_time_confirmed = models.BooleanField(default='False')
    match_status = models.CharField(max_length=256, default='') 
    winner = models.ForeignKey('Team', related_name='winner', on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return self.home_team.name + ' ' + str(self.home_team_score) + ' - ' + str(self.away_team_score) + ' ' + self.away_team.name


class Competition(models.Model):
    
    api_id = models.CharField(max_length=256, default='') 
    name = models.CharField(max_length=256, default='')
        
    def __str__(self):
        return self.name


class Season(models.Model):
    
    api_id = models.CharField(max_length=256, default='') 
    name = models.CharField(max_length=256, default='')
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    year = models.CharField(max_length=10)
    competition = models.ForeignKey('Competition', on_delete=models.SET_NULL, null=True)
    teams = models.ManyToManyField('Team')

    def __str__(self):
        return self.name


class Team(models.Model):

    api_id = models.CharField(max_length=256, default='')
    name = models.CharField(max_length=256, default='')
    country = models.CharField(max_length=64, default='')
    country_code = models.CharField(max_length=4, default='')
    abbreviation = models.CharField(max_length=10, default='')
    manager = models.OneToOneField('Player', related_name = 'manager', on_delete=models.SET_NULL, null=True)
    venue = models.OneToOneField('Venue', on_delete=models.SET_NULL, null=True)
    seasons = models.ManyToManyField('Season')
    def __str__(self):
        return self.name


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
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class Statistic(models.Model):
    
    player = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True)
    game = models.ForeignKey(SportEvent, on_delete=models.SET_NULL, null=True)
    yellow_cards = models.IntegerField(null=True)
    red_cards = models.IntegerField(null=True)
    suspensions = models.IntegerField(null=True)
    goals_scored = models.IntegerField(null=True)
    seven_m_goals = models.IntegerField(null=True)
    field_goals = models.IntegerField(null=True)
    assists = models.IntegerField(null=True)
    technical_fouls = models.IntegerField(null=True)
    steals = models.IntegerField(null=True)
    blocks = models.IntegerField(null=True)
    saves = models.IntegerField(null=True)

    def __str__(self):
        return str(self.player) + ' (' + str(self.game) + ')'


class Venue(models.Model):
    api_id = models.CharField(max_length=256, default='')
    name = models.CharField(max_length=256, default='')
    city_name = models.CharField(max_length=256, default='')
    country_code = models.CharField(max_length=4, default='')
    country_name = models.CharField(max_length=256, default='')
    capacity = models.IntegerField(null=True)

    #TODO : cut it into 2 coordinates
    map_coordinates = models.CharField(max_length=256, default='')

    def __str__(self):
        return self.name

