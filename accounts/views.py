from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

from .forms import ConnectionForm
from stats import views as stats_views

def deconnection(request):
    logout(request)
    return redirect(reverse(connection))

def connection(request):
    error = False

    if request.method == "POST":
        form = ConnectionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)  # Nous vérifions si les données sont correctes
            if user:  # Si l'objet renvoyé n'est pas None
                login(request, user)  # nous connectons l'utilisateur
                return redirect(stats_views.teams_list)
            else: # sinon une erreur sera affichée
                error = True
    else:
        form = ConnectionForm()

    return render(request, 'connection_form.html', locals())
