from django.shortcuts import render
from .models import OfficialTeam as Team
from django.contrib.auth.decorators import login_required

@login_required
def teams_list(request):
    teams = Team.objects.all()
    return render(request, 'stats/teams_list.html', {'teams': teams})

@login_required
def team_detail(request, id):
    team = Team.objects.get(id=id)
    return render(request, 'stats/team_detail.html', {'team': team})

