from django.contrib.auth.models import User
from .models import FantasyPlayer


BFF = [
    {
        'username': 'Bobo',
        'first_name': 'Boris',
        'last_name': 'Beillevaire',
        'favorite_player': 'Gurbindo',
        'email': 'bobo@popote.xyz' 
    },
    {
        'username': 'Zita',
        'first_name': 'Sarah',
        'last_name': 'Beauvais',
        'favorite_player': 'Tournat',
        'email': 'zita@popote.xyz' 
    },
    {
        'username': 'Pipouille',
        'first_name': 'Juliette',
        'last_name': 'LeMauff',
        'favorite_player': 'Guillo',
        'email': 'pipouille@popote.xyz' 
    },
    {
        'username': 'Xavzarov',
        'first_name': 'Xavier',
        'last_name': 'Guihéneuf',
        'favorite_player': 'Lazarov',
        'email': 'xavzarov@popote.xyz' 
    },
    {
        'username': 'Jojo',
        'first_name': 'Josselin',
        'last_name': 'Potiron',
        'favorite_player': 'Buric',
        'email': 'jojo@popote.xyz' 
    },
    {
        'username': 'Clara',
        'first_name': 'Clara',
        'last_name': 'Manceny',
        'favorite_player': 'ROCK',
        'email': 'clara@popote.xyz' 
    },

]

def add_default_users():
    for entry in BFF:
        user = User.objects.create_user(entry['username'], entry['email'], User.objects.make_random_password())
        player = FantasyPlayer(favorite_player=entry['favorite_player'], user=user)
        player.user.last_name = entry['last_name']
        player.user.first_name = entry['first_name']
        player.save()

add_default_users()