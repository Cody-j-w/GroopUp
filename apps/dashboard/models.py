from __future__ import unicode_literals
from django.db import models
from django.db.models import Count
from django.db.models import ImageField
from django.utils.dateparse import parse_date
from datetime import datetime, date
import pytz
import re
import bcrypt
from PIL import Image

USERNAME_REGEX = re.compile(r'^[a-zA-Z0-9]*$')
PASSWORD_REGEX = re.compile(r'^[a-zA-Z0-9!@#\$%\^&\*]*$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-z]+$')

class UserManager(models.Manager):
    def register_validator(self,postData):
        errors = {}
        if not re.match(USERNAME_REGEX, postData['username']):
            errors['username'] = 'A valid username is required! Alphanumeric characters only!'
        if len(postData['username'])>64:
            errors['username_length'] = 'Username must be below 64 characters!'
        if User.objects.filter(username=postData['username']).exists():
            errors['username_registration'] = 'This Username already exists!'
        if len(postData['password'])<8:
            errors['password'] = 'Password must be at least 8 characters!'
        if len(postData['password'])>64:
            errors['passlength'] = 'Password must be below 64 characters!'
        if not re.match(PASSWORD_REGEX, postData['password']):
            errors['passvalid'] = 'Invalid password!'
        if postData['password'] != postData['confirm_pass']:
            errors['passmatch'] = 'Passwords must match!'
        if not re.match(EMAIL_REGEX, postData['email']):
            errors['email'] = 'A valid email is required! Alphanumeric characters only!'
        if len(postData['email'])>64:
            errors['email_length'] = 'email must be below 64 characters!'
        if User.objects.filter(email=postData['email']).exists():
            errors['email_registration'] = 'This email already exists!'
        if len(postData['birthday'])>10:
            errors['age'] = 'a valid birthdays is required!'
        elif not postData['birthday']:
            errors['birthdate'] = 'a valid birthdays is required!'
        else:
            birthday = parse_date(postData['birthday'])
            formation = date(1808, 1, 1)
            if birthday > date.today():
                errors['birthday'] = "we're pretty sure you're not a time traveller. birthday must be before today."
            if birthday<formation:
                errors['company_date'] = 'Please pick a valid birthdate.'
        if len(errors)==0:
            password_hash = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            user = User.objects.create(username = postData['username'], password = password_hash, email = postData['email'], birthday = postData['birthday'], avatar='/static/images/default.png')

        return errors
    def login_validator(self,postData):
        errors = {}
        if User.objects.filter(username=postData['username']).exists():
            user = User.objects.get(username=postData['username'])
            if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                errors['passmatch'] = 'username and/or password is incorrect.'
        else:
            errors['usermatch'] = 'username and/or password is incorrect.'
        return errors

    def description_validator(self,postData):
        errors = {}
        if len(postData['description'])>250:
            errors['desc_length'] = 'Description must be 255 characters or less.'
        return errors

    def update_validator(self,postData):
        errors = {}
        if postData['form_id']=='username':
            if not re.match(USERNAME_REGEX, postData['username']):
                errors['username'] = 'A valid username is required! Alphanumeric characters only!'
            if len(postData['username'])>64:
                errors['username_length'] = 'Username must be below 64 characters!'
            if User.objects.filter(username=postData['username']).exists():
                errors['username_registration'] = 'This Username already exists!'
            if len(errors)==0:
                user = User.objects.get(id=int(postData['user_id']))
                user.username = postData['username']
                user.save()
        elif postData['form_id']=='email':
            if not re.match(EMAIL_REGEX, postData['email']):
                errors['email'] = 'A valid email is required! Alphanumeric characters only!'
            if len(postData['email'])>64:
                errors['email_length'] = 'email must be below 64 characters!'
            if User.objects.filter(email=postData['email']).exists():
                errors['email_registration'] = 'This email already exists!'
            if len(errors)==0:
                user = User.objects.get(id=int(postData['user_id']))
                user.email = postData['email']
                user.save()
        elif postData['form_id']=='password':
            if User.objects.filter(username=postData['username']).exists():
                user = User.objects.get(username=postData['username'])
                if bcrypt.checkpw(postData['current_pass'].encode(), user.password.encode()):
                    if len(postData['password'])>8:
                        if postData['password'] == postData['confirm_pass']:
                            password_hash = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
                            user.password = password_hash
                            user.save()
        
                

        return errors


class GameManager(models.Manager):
    def game_finder(self, postData):
        errors = {}
        if postData['game_type']=='Tabletop_RPG' or postData['game_type']=='Boardgame' or postData['game_type']=='Card_game' or postData['game_type']=='War_game':
            games = Game.objects.filter(game_type=postData['game_type'])
        elif postData['game_type']=='A_bit_of_variety':
            games = Game.objects.all()
        else:
            errors['game_finder'] = 'please select a valid game type.'
        if postData['game_location'] == 'physical' or postData['game_location'] == 'online':
            games = games.filter(status = postData['game_location'])
        return errors
    def game_creator(self, postData):
        errors = {}
        if len(postData['name'])<3:
            errors['short_name']='Game name must be three characters or longer.'
        if len(postData['name'])>64:
            errors['long_name']='name must be shorter than 64 characters.'
        if postData['game_type']!='Tabletop_RPG' and postData['game_type']!='Boardgame' and postData['game_type']!='Card_game' and postData['game_type']!='War_game' and postData['game_type']!='A-bit_of_variety':
            errors['game_creation']='Please select a valid game type.'
        if postData['game_location']!='Physical' and postData['game_location']!='Online':
            errors['game_status']='Please select either Physical or Online.'
        if postData['game_day']!='Mon' and postData['game_day']!='Tue' and postData['game_day']!='Wed' and postData['game_day']!='Thu' and postData['game_day']!='Fri' and postData['game_day']!='Sat' and postData['game_day']!='Sun':
             errors['game_day']='Please select a valid day.'
        if len(errors)==0:
            Game.objects.create(name=postData['name'], game_system=postData['system'], game_type=postData['game_type'], status=postData['game_location'], day=postData['game_day'], game_master=User.objects.get(id=int(postData['user_id'])))


class User(models.Model):
    username = models.CharField(default='', blank=True, max_length=64)
    email = models.CharField(default='', blank=True, max_length=64)
    password = models.CharField(default='', max_length=250)
    description = models.TextField(default='', blank=True)
    birthday = models.DateTimeField()
    avatar = models.ImageField(default='static/images/default.png', blank=True, )
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

    def __str__(self):
        return self.username

class Game(models.Model):
    name = models.CharField(max_length=255, blank=True, default='')
    description = models.TextField()
    game_system = models.CharField(max_length=64, default='', blank=True)
    game_type = models.CharField(max_length=64, blank=True, default='')
    players = models.ManyToManyField(User, related_name='games')
    game_master = models.ForeignKey(User, related_name='my_games')
    status = models.CharField(max_length=10, blank=True, default='')
    time = models.TimeField()
    day = models.CharField(max_length=10, default='', blank=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = GameManager()

    def __str__(self):
        return self.name


