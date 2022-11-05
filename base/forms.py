from dataclasses import fields
from pyexpat import model
from statistics import mode
from django.forms import ModelForm
from .models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Room, Media
# start making form here

class RoomForm(ModelForm):
 
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']
    
class UserForm(ModelForm):

    class Meta:
        model = User
        fields = ['avatar','username', 'email','bio', ]

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', ]

class MediaForm(ModelForm):
    class Meta:
        model = Media
        fields = ['file']