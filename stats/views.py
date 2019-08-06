from django.shortcuts import render
from .models import Team
from django.http import HttpResponse

# import stats.models as models
import stats.fetch as fetch


def index(request):
    file = fetch.fetch_data_json()
    return HttpResponse("Not yet a dashboard")

def load(request):
    fetch.load_data_json()
    return HttpResponse("You're loading games into database")

def results(request, team):
    response = "You're looking at the dashboard of %s."
    return HttpResponse(response % team)

def teams_list(request):
    teams = Team.objects.all()
    return render(request, 'stats/teams_list.html', {'teams': teams})

def team_detail(request, id):
    team = Team.objects.get(id=id)
    return render(request, 'stats/team_detail.html', {'team': team})

