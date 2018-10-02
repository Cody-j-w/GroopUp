from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.db.models import Q
from apps.dashboard.models import *

def index(request):
    if 'user_id' not in request.session:
        return render(request, 'dashboard/index.html')
    else:
        context = {
            'my_info':User.objects.get(id=request.session['user_id'])
        }
        return render(request, 'dashboard/index.html', context)

def register_user(request):
    return render(request, 'dashboard/login.html')

def register(request):
    errors = User.objects.register_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/login')
    else:
        user_name = User.objects.get(username = request.POST['username']).username
        user_id = User.objects.get(username = request.POST['username']).id
        request.session['user'] = user_name
        request.session['user_id'] = user_id
        return redirect('/')

def login(request):
    if request.method == 'POST':
        errors = User.objects.login_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            username = User.objects.get(username = request.POST['username']).username
            user_id = User.objects.get(username = request.POST['username']).id
            request.session['user_id'] = user_id
            request.session['user'] = username
            return redirect('/')
    else:
        return redirect('/')
def user(request, username):
    return render(request, 'dashboard/user.html', {'user': User.objects.get(username=username)})

def logout(request):
    request.session.clear()
    return redirect('/')

def settings(request):
    return render(request, 'dashboard/settings.html')

def game_finder(request):
    errors = Game.objects.game_finder(request.POST)
    games = Game.objects.all()
    if request.POST['game_type']=='Tabletop RPG' or request.POST['game_type']=='Boardgame' or request.POST['game_type']=='Card_game' or request.POST['game_type']=='War_game':
        games = games.filter(game_type=request.POST['game_type'])
    elif request.POST['game_type']=='A_bit_of_variety':
        games = Game.objects.all()
    if request.POST['game_location'] == 'physical' or request.POST['game_location'] == 'online':
        games = games.filter(status = request.POST['game_location'])
    return render(request, 'dashboard/game_finder.html', {'games':games[:6]})

def game(request, id):
    return render(request, 'dashboard/game.html', {'game':Game.objects.get(id=id)})

def user_edit(request):
    return render(request, 'dashboard/user_edit.html')

def email_edit(request):
    return render(request, 'dashboard/email_edit.html')

def pass_edit(request):
    return render(request, 'dashboard/pass_edit.html')

def avatar_edit(request):
    return render(request, 'dashboard/avatar_edit.html')
def avatar_change(request):
    if request.method=='POST':
        user = User.objects.get(id=int(request.POST['user_id']))
        user.avatar.delete(save=True)
        user.avatar = request.FILES['avatar']
        user.save()
    return redirect('/settings')

def desc_edit(request):
    return render(request, 'dashboard/desc_edit.html')