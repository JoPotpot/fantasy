from django.urls import path
from . import views

urlpatterns = [
    path('teams/', views.teams_list, name='teams'),
    path('teams/<int:id>/detail/', views.team_detail, name='team detail'),
]