from django.db import models
from django.utils import timezone




class Sport_event(models.Model):
    
    home_team = models.CharField(max_length=256, default='<home team>') 
    away_team = models.CharField(max_length=256, default='<home team>')
    home_team_score = models.IntegerField(default=0)
    away_team_score = models.IntegerField(default=0)
    competition_name = models.CharField(max_length=256)
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
