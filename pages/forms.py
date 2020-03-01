from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')

class SearchForm(forms.Form):
    search = forms.CharField()
    retweet_threshold = forms.IntegerField(required = False)
    favorite_threshold = forms.IntegerField(required = False)
    upper_date_limit = forms.CharField(required = False)
    lower_date_limit = forms.CharField(required = False)
